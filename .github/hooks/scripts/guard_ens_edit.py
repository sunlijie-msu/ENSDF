#!/usr/bin/env python3
"""PreToolUse guard for .ens edits: reload-before-edit and byte-exact unique anchors.

Rules (apply to edit tools AND any terminal command that rewrites a .ens file):
  1. Freshness - the file must be unchanged since the last read_file/edit/mutating
     command, so a concurrent human edit can never be overwritten silently.
  2. Anchor    - oldString must match byte-exactly once (the editor matches
     loosely, so short/repeated anchors can swallow whole blocks).
  3. Span cap  - one edit cannot restructure more than SPAN lines at once.
Terminal commands that rewrite a whole file (e.g. "--fix" scripts, redirection,
Set-Content) bypass anchor matching entirely, so they get the same freshness
gate and then invalidate state — the write outcome is unverifiable until the
next read_file.

oldText is the anchor.
Safe anchor requirements:
Exists in current file.
Matches exactly once.
Includes enough surrounding text to identify the correct comment.
Comes from a freshly read file.
Does not use short, repeated text.
If text changed or matches zero/multiple times, hook denies edit.

PostToolUse validation stays with verify_ens_edit.py (ASCII + 80-column ruler).

Token lifecycle (state.json, one-shot):
issued by   read_file
consumed by each verified edit / mutating terminal command
preserved   by read-only tools (a read never consumes its own token)

Normal edit flow:
AI reads current file          (token issued)
AI builds exact oldText → newText edit
Hook hash matches → edit allowed (token consumed after PostToolUse verify)

Concurrent edit flow:
AI reads file
Human edits file
AI attempts edit
Hook detects hash mismatch → deny
AI rereads current file
AI rebuilds anchor
AI retries → edit allowed

Approved .ens edit tools: editFiles and replacement tools with exact oldText/newText.
apply_patch on .ens is refused. PostToolUse compares actual content with this hook's
predicted result, catching editor-side block collapse or unexpected rewrites.

"""
import hashlib
import json
import os
import re
import sys
from urllib.parse import unquote, urlparse

SPAN = 8  # max lines in one oldString
ENS_PATH_RE = re.compile(r"[^\s\"']+\.ens", re.IGNORECASE)
MUTATING_RE = re.compile(r"--fix\b|>>?\s|Set-Content|Out-File|Add-Content|\.write_text\(|WriteAllText", re.IGNORECASE)
EDIT_TOOLS = {"replace_string_in_file", "multi_replace_string_in_file", "editFiles", "edit/editFiles"}
READ_TOOLS = {"read_file", "readFile", "read/readFile"}


def deny(reason):
    payload = json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}})
    write_stdout(payload)
    sys.exit(0)


def write_stdout(text):
    """Emit UTF-8 bytes regardless of the console code page."""
    data = (text + "\n").encode("utf-8")
    try:
        sys.stdout.buffer.write(data)
        sys.stdout.buffer.flush()
    except AttributeError:
        sys.stdout.write(text + "\n")


def load_event():
    """Parse the hook payload from stdin as UTF-8.

    sys.stdin decodes with the console code page (e.g. cp936), which corrupts
    non-ASCII characters in anchors so they never match the UTF-8 file text.
    """
    try:
        raw = sys.stdin.buffer.read()
    except AttributeError:
        raw = sys.stdin.read().encode("utf-8", "replace")
    if not raw.strip():
        return {}
    for enc in ("utf-8-sig", "utf-8"):
        try:
            return json.loads(raw.decode(enc))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
    try:
        return json.loads(raw.decode(sys.stdin.encoding or "utf-8", "replace"))
    except json.JSONDecodeError:
        return {}


def workspace_root(data):
    cwd = data.get("cwd")
    if isinstance(cwd, str) and cwd.strip():
        return os.path.realpath(os.path.normpath(cwd))
    return os.path.realpath(os.getcwd())


def key_of(path, root):
    if path.startswith("file://"):
        parsed = urlparse(path)
        path = unquote(parsed.path)
        if re.match(r"^/[A-Za-z]:/", path):
            path = path[1:]
    if os.path.isabs(path):
        return os.path.realpath(path)
    return os.path.realpath(os.path.join(root, path))


def read(path):
    try:
        with open(path, encoding="utf-8", newline="") as fh:
            return fh.read().replace("\r\n", "\n")
    except OSError:
        return None


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def state_load(state_path):
    try:
        with open(state_path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def state_save(state, state_path):
    os.makedirs(os.path.dirname(state_path), exist_ok=True)
    with open(state_path, "w", encoding="utf-8") as fh:
        json.dump(state, fh)


def path_value(item):
    for field in ("filePath", "file_path", "path", "uri"):
        value = item.get(field)
        if isinstance(value, str) and value:
            return value
    return ""


def text_value(item, *fields):
    for field in fields:
        value = item.get(field)
        if isinstance(value, str):
            return value
    return None


def edit_operations(data):
    """Return (path, old, new) operations and every .ens path in an edit payload."""
    operations = []
    paths = set()

    def add(path, item):
        if not isinstance(path, str) or not path.lower().endswith(".ens"):
            return
        paths.add(path)
        old = text_value(item, "oldString", "old_string", "oldText", "old_text")
        new = text_value(item, "newString", "new_string", "newText", "new_text")
        if old is not None and new is not None:
            operations.append((path, old.replace("\r\n", "\n"), new.replace("\r\n", "\n")))

    direct_path = path_value(data)
    if direct_path:
        add(direct_path, data)

    for item in data.get("replacements") or []:
        if isinstance(item, dict):
            add(path_value(item) or direct_path, item)

    for file_item in data.get("files") or []:
        if not isinstance(file_item, dict):
            continue
        path = path_value(file_item)
        if path.lower().endswith(".ens"):
            paths.add(path)
        edits = file_item.get("edits") or file_item.get("operations") or []
        for item in edits:
            if isinstance(item, dict):
                add(path_value(item) or path, item)

    for item in data.get("edits") or data.get("operations") or []:
        if isinstance(item, dict):
            add(path_value(item) or direct_path, item)

    return operations, paths


def guard_operations(operations, state, root):
    """Check exact anchors for ordered operations and predict resulting hashes."""
    by_file = {}
    for path, old, new in operations:
        if not path.lower().endswith(".ens"):
            continue
        by_file.setdefault(key_of(path, root), []).append((old.replace("\r\n", "\n"),
                                                            new.replace("\r\n", "\n")))

    touched = False
    for key, ops in by_file.items():
        text = read(key)
        if text is None:
            deny(f"Cannot read {os.path.basename(key)}.")
        expected = state.get(key)
        if expected is None:
            deny(f"No fresh-read token for {os.path.basename(key)} (tokens are one-shot: issued by read_file, "
                 f"consumed by each verified edit) — this is not a concurrent-edit warning. "
                 f"Re-read the file, then retry the edit.")
        if expected != digest(text):
            deny(f"{os.path.basename(key)} changed on disk since your last read/edit (concurrent edit). "
                 f"Re-read the surrounding block, rebuild the anchor, retry. Never overwrite a concurrent edit.")
        for old, new in ops:
            hits = text.count(old)
            if hits != 1:
                deny(f"Anchor matches {hits} time(s) in {os.path.basename(key)}; must match byte-exactly once. "
                     f"Rebuild the current patch hunk from the file — short or repeated anchors are forbidden.")
            if len(old.split("\n")) > SPAN:
                deny(f"Edit spans more than {SPAN} lines. Split it into record-group edits.")
            text = text.replace(old, new, 1)
        state[key] = digest(text)
        touched = True
    return touched


def comment_patch_operations(patch_text, root):
    """Extract one-line c-record replacements with optional unique context."""
    operations = []
    current_path = None
    hunk = None

    def flush():
        nonlocal hunk
        if current_path and hunk is not None:
            old_lines = []
            new_lines = []
            old_indexes = []
            new_indexes = []
            for line in hunk:
                if line.startswith("-"):
                    old_indexes.append(len(old_lines))
                    old_lines.append(line[1:])
                elif line.startswith("+"):
                    new_indexes.append(len(new_lines))
                    new_lines.append(line[1:])
                elif line.startswith(" "):
                    old_lines.append(line[1:])
                    new_lines.append(line[1:])
            if len(old_indexes) != 1 or len(new_indexes) != 1:
                deny("Only one anchored cL/cG replacement is allowed per .ens apply_patch hunk.")
            old_line = old_lines[old_indexes[0]]
            new_line = new_lines[new_indexes[0]]
            if old_line[6:7] != "c" or new_line[6:7] != "c":
                deny("Only single anchored cL/cG apply_patch replacements are allowed for .ens files.")
            text = read(key_of(current_path, root))
            if text is None:
                deny(f"Cannot read {os.path.basename(key_of(current_path, root))}.")
            file_lines = text.split("\n")
            matches = []
            for index in range(len(file_lines) - len(old_lines) + 1):
                if all(file_lines[index + offset].rstrip() == source.rstrip()
                       for offset, source in enumerate(old_lines)):
                    matches.append(index)
            if len(matches) != 1:
                deny(f"Comment anchor/context matches {len(matches)} time(s); rebuild it from the current file.")
            comment_index = matches[0] + old_indexes[0]
            operations.append((current_path, text, comment_index, new_line.rstrip()))
        hunk = None

    for line in patch_text.splitlines():
        if line.startswith("*** Update File: "):
            flush()
            current_path = line.split(": ", 1)[1].strip()
            continue
        if line.startswith("*** "):
            flush()
            current_path = None
            continue
        if line.startswith("@@"):
            flush()
            hunk = []
            continue
        if hunk is not None:
            hunk.append(line)
    flush()
    if not operations:
        deny(".ens apply_patch requires one exact single-line cL/cG replacement.")
    return operations


def guard_comment_operations(operations, state, root):
    """Guard comment replacements while preserving exact current file context."""
    touched = False
    for path, original, comment_index, new_line in operations:
        key = key_of(path, root)
        text = read(key)
        if text is None:
            deny(f"Cannot read {os.path.basename(key)}.")
        expected = state.get(key)
        if expected is None:
            deny(f"No fresh-read token for {os.path.basename(key)} (tokens are one-shot: issued by read_file, "
                 f"consumed by each verified edit) — this is not a concurrent-edit warning. "
                 f"Re-read the file, then retry the edit.")
        if expected != digest(text):
            deny(f"{os.path.basename(key)} changed on disk since your last read/edit (concurrent edit). "
                 f"Re-read the surrounding block, rebuild the anchor, retry. Never overwrite a concurrent edit.")
        lines = text.split("\n")
        if comment_index >= len(lines) or lines[comment_index][6:7] != "c":
            deny("Comment anchor no longer identifies a cL/cG record; reread and rebuild the edit.")
        lines[comment_index] = new_line
        state[key] = digest("\n".join(lines))
        touched = True
    return touched


def guard_edits(data, state, root):
    """Check exact anchors for all supported edit payload shapes."""
    operations, paths = edit_operations(data)
    if paths and not operations:
            deny(".ens edit has no exact old/new text anchor. Use editFiles with files[].edits[].oldText/newText.")
    return guard_operations(operations, state, root)


def guard_terminal(command, state, root):
    """run_in_terminal / send_to_terminal: a command that rewrites a whole .ens
    file (e.g. column_calibrate.py --fix) bypasses anchor matching entirely, so
    it gets the same freshness gate, then invalidates state for that file."""
    if "--dry-run" in command or not MUTATING_RE.search(command):
        return False
    touched = False
    for match in ENS_PATH_RE.finditer(command):
        key = key_of(match.group(0).strip("\"'"), root)
        text = read(key)
        if text is None:
            continue
        expected = state.get(key)
        if expected is None:
            deny(f"No fresh-read token for {os.path.basename(key)} — re-read the file before running "
                 f"a command that rewrites it (this is not a concurrent-edit warning).")
        if expected != digest(text):
            deny(f"{os.path.basename(key)} changed on disk since your last read (concurrent edit). "
                 f"Re-read before running a command that rewrites this file.")
        state.pop(key, None)
        touched = True
    return touched


def main():
    event = load_event()
    tool = event.get("tool_name", "")
    data = event.get("tool_input") or {}
    root = workspace_root(event)
    state_path = os.path.join(root, ".github", "temp", "ens_guard", "state.json")
    state = state_load(state_path)

    if tool in READ_TOOLS:  # a read refreshes freshness; verify skips reads so it is not consumed
        path = data.get("filePath", "")
        if path.lower().endswith(".ens"):
            text = read(key_of(path, root))
            if text is not None:
                state[key_of(path, root)] = digest(text)
                state_save(state, state_path)
        return

    if tool == "apply_patch":
        patch_text = data.get("input", "") or ""
        if re.search(r"^\*\*\* (?:Update|Add|Delete) File: .*\.ens", patch_text, re.IGNORECASE | re.MULTILINE):
            operations = comment_patch_operations(patch_text, root)
            if guard_comment_operations(operations, state, root):
                state_save(state, state_path)
        return

    if tool in ("run_in_terminal", "send_to_terminal"):
        if guard_terminal(data.get("command", "") or "", state, root):
            state_save(state, state_path)
        return

    if tool not in EDIT_TOOLS:
        return

    if guard_edits(data, state, root):
        state_save(state, state_path)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # fail closed
        deny(f"guard_ens_edit.py error: {exc}")
