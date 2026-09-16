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

PostToolUse validation stays with verify_ens_edit.py (ASCII + 80-column ruler).
"""
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STATE = os.path.join(ROOT, ".github", "temp", "ens_guard", "state.json")
SPAN = 8  # max lines in one oldString
ENS_PATH_RE = re.compile(r"[^\s\"']+\.ens", re.IGNORECASE)
MUTATING_RE = re.compile(r"--fix\b|>>?\s|Set-Content|Out-File|Add-Content|\.write_text\(|WriteAllText", re.IGNORECASE)


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}}))
    sys.exit(0)


def key_of(path):
    return os.path.realpath(os.path.join(ROOT, path))


def read(path):
    try:
        with open(path, encoding="utf-8", newline="") as fh:
            return fh.read().replace("\r\n", "\n")
    except OSError:
        return None


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def state_load():
    try:
        with open(STATE, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def state_save(state):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump(state, fh)


def guard_edits(data, state):
    """replace_string_in_file / multi_replace_string_in_file: byte-exact anchors,
    applied in order per file so a multi-edit call is checked against the text
    each earlier edit in the SAME call actually produces."""
    by_file = {}
    for edit in data.get("replacements") or [data]:
        path = edit.get("filePath", "") or edit.get("file_path", "")
        if not path.lower().endswith(".ens"):
            continue
        old = (edit.get("oldString") or "").replace("\r\n", "\n")
        new = (edit.get("newString") or "").replace("\r\n", "\n")
        by_file.setdefault(key_of(path), []).append((old, new))

    touched = False
    for key, ops in by_file.items():
        text = read(key)
        if text is None:
            deny(f"Cannot read {os.path.basename(key)}.")
        if state.get(key) != digest(text):
            deny(f"{os.path.basename(key)} changed since your last read/edit (concurrent edit). "
                 f"Re-read the surrounding block, rebuild the anchor, retry. Never overwrite a concurrent edit.")
        for old, new in ops:
            hits = text.count(old)
            if hits != 1:
                deny(f"Anchor matches {hits} time(s) in {os.path.basename(key)}; must match byte-exactly once. "
                     f"Rebuild oldString from the current 80-column text — short or repeated anchors are forbidden.")
            if len(old.split("\n")) > SPAN:
                deny(f"Edit spans more than {SPAN} lines. Split it into record-group edits.")
            text = text.replace(old, new, 1)  # simulate so state matches the file the tool is about to write
        state[key] = digest(text)
        touched = True
    return touched


def guard_terminal(command, state):
    """run_in_terminal / send_to_terminal: a command that rewrites a whole .ens
    file (e.g. column_calibrate.py --fix) bypasses anchor matching entirely, so
    it gets the same freshness gate, then invalidates state for that file."""
    if "--dry-run" in command or not MUTATING_RE.search(command):
        return False
    touched = False
    for match in ENS_PATH_RE.finditer(command):
        key = key_of(match.group(0).strip("\"'"))
        text = read(key)
        if text is None:
            continue
        if state.get(key) != digest(text):
            deny(f"{os.path.basename(key)} changed since your last read (concurrent edit). "
                 f"Re-read before running a command that rewrites this file.")
        state.pop(key, None)
        touched = True
    return touched


def main():
    event = json.load(sys.stdin)
    tool = event.get("tool_name", "")
    data = event.get("tool_input") or {}
    state = state_load()

    if tool == "read_file":  # a read refreshes freshness
        path = data.get("filePath", "")
        if path.lower().endswith(".ens"):
            text = read(key_of(path))
            if text is not None:
                state[key_of(path)] = digest(text)
                state_save(state)
        return

    if tool == "apply_patch":
        if re.search(r"\*\*\* (?:Update|Add|Delete) File: .*\.ens", data.get("input", "") or "", re.IGNORECASE):
            deny("apply_patch on .ens files is refused — use replace_string_in_file/"
                 "multi_replace_string_in_file so anchors can be verified.")
        return

    if tool in ("run_in_terminal", "send_to_terminal"):
        if guard_terminal(data.get("command", "") or "", state):
            state_save(state)
        return

    if tool not in ("replace_string_in_file", "multi_replace_string_in_file"):
        return

    if guard_edits(data, state):
        state_save(state)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # fail closed
        deny(f"guard_ens_edit.py error: {exc}")
