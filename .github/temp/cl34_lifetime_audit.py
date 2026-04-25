import math
import re
import subprocess
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

ROOT = Path(r"d:\X\ND\ENSDF")
ADOPTED = ROOT / r"A34\Cl34\new\Cl34_adopted.ens"
JAVA_AVG = ROOT / r".github\scripts\Java_Average.py"
PYTHON = Path(r"C:/Users/sun/AppData/Local/Programs/Python/Python311/python.exe")

SOURCE_CONFIG = {
    "G": {
        "path": ROOT / r"A34\Cl34\new\Cl34_31p_a_ng.ens",
        "reaction": "{+31}P(|a,n|g)",
    },
    "I": {
        "path": ROOT / r"A34\Cl34\new\Cl34_32s_3he_pg.ens",
        "reaction": "{+32}S({+3}He,p|g)",
    },
    "K": {
        "path": ROOT / r"A34\Cl34\new\Cl34_33s_p_g.ens",
        "reaction": "{+33}S(p,|g)",
    },
    "F": {
        "path": ROOT / r"A34\Cl34\new\Cl34_27al_12c_ang.ens",
        "reaction": "{+27}Al({+12}C,|an|g)",
    },
}

UNIT_SCALE = {
    "FS": 1e-15,
    "PS": 1e-12,
    "NS": 1e-9,
    "US": 1e-6,
    "MS": 1e-3,
    "S": 1.0,
}
UNIT_ORDER = ["FS", "PS", "NS", "US", "MS", "S"]

MEAS_RE = re.compile(
    r"(?P<op>[<>]?)"
    r"(?P<value>\d+(?:\.\d+)?(?:E[+-]?\d+)?)\s*"
    r"(?P<unit>fs|ps|ns|us|ms|s|FS|PS|NS|US|MS|S)"
    r"(?:\s*(?P<unc>\{I[^}]+\}))?\s*"
    r"\((?P<nsr>\d{4}[A-Za-z0-9]{4}),\s*(?P<method>[^)]+)\)"
)

SUGGESTED_RE = re.compile(r"suggested adopted result:\s+(?P<value>\S+)\s*\n\s*\((?P<method>[^)]+)\)")
LREC_RE = re.compile(r"^ 34CL. L ")
XREF_RE = re.compile(r"^ 34CLX L XREF=(?P<xref>.*)$")


def join_t_block(lines):
    parts = []
    for line in lines:
        parts.append(line[9:].rstrip())
    return " ".join(part for part in parts).replace("  ", " ").strip()


def parse_uncertainty(value_text, unc_text):
    if not unc_text:
        return None
    unc_body = unc_text[2:-1]
    if unc_body.startswith("+"):
        match = re.fullmatch(r"\+(\d+)-(\d+)", unc_body)
        if not match:
            return None
        upper_digits, lower_digits = match.groups()
        if "E" in value_text.upper():
            mantissa, exp = value_text.upper().split("E")
            decimals = len(mantissa.split(".")[1]) if "." in mantissa else 0
            factor = (10 ** int(exp)) * (10 ** (-decimals))
        else:
            decimals = len(value_text.split(".")[1]) if "." in value_text else 0
            factor = 10 ** (-decimals)
        return float(upper_digits) * factor, float(lower_digits) * factor
    value_upper = value_text.upper()
    if "E" in value_upper:
        mantissa, exp = value_upper.split("E")
        decimals = len(mantissa.split(".")[1]) if "." in mantissa else 0
        abs_unc = float(unc_body) * (10 ** int(exp)) * (10 ** (-decimals))
        return abs_unc
    decimals = len(value_text.split(".")[1]) if "." in value_text else 0
    return float(unc_body) * (10 ** (-decimals))


def parse_items(text, reaction, dataset_letter):
    items = []
    for match in MEAS_RE.finditer(text):
        item = {
            "op": match.group("op") or "=",
            "value_text": match.group("value"),
            "unit": match.group("unit").upper(),
            "unc_text": match.group("unc"),
            "nsr": match.group("nsr"),
            "method": match.group("method"),
            "reaction": reaction,
            "dataset": dataset_letter,
        }
        item["value_abs"] = float(match.group("value")) * UNIT_SCALE[item["unit"]]
        if item["op"] != "=":
            item["unc_abs"] = None
        else:
            parsed_unc = parse_uncertainty(item["value_text"], item["unc_text"])
            if isinstance(parsed_unc, tuple):
                item["unc_abs"] = tuple(part * UNIT_SCALE[item["unit"]] for part in parsed_unc)
            elif parsed_unc is None:
                item["unc_abs"] = None
            else:
                item["unc_abs"] = parsed_unc * UNIT_SCALE[item["unit"]]
        items.append(item)
    return items


def parse_source_entries(path, reaction, dataset_letter):
    lines = path.read_text().splitlines()
    entries = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if len(line) >= 8 and line[5] == " " and line[6] == " " and line[7] == "L":
            energy = line[9:19].strip()
            energy_val = float(energy.replace(" ", "")) if energy else None
            j = i + 1
            blocks = []
            current = []
            while j < len(lines):
                nxt = lines[j]
                if len(nxt) >= 8 and nxt[5] == " " and nxt[6] == " " and nxt[7] == "L":
                    break
                if len(nxt) >= 9 and nxt[5] == " " and nxt[6:8] == "cL" and "T$" in nxt[9:]:
                    if current:
                        blocks.append(current)
                    current = [nxt]
                elif current and len(nxt) >= 9 and nxt[6:8] == "cL" and nxt[5].isdigit():
                    current.append(nxt)
                elif current:
                    blocks.append(current)
                    current = []
                j += 1
            if current:
                blocks.append(current)
            for block in blocks:
                text = join_t_block(block)
                if "|t" in text or "lifetime" in text:
                    entries.append({
                        "energy": energy_val,
                        "energy_text": energy,
                        "text": text,
                        "items": parse_items(text, reaction, dataset_letter),
                        "dataset": dataset_letter,
                        "reaction": reaction,
                    })
            i = j
        else:
            i += 1
    return entries


def parse_adopted_blocks(path):
    lines = path.read_text().splitlines()
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if len(line) >= 8 and line[5] == " " and line[6] == " " and line[7] == "L":
            level = {
                "l_line_no": i + 1,
                "l_line": line,
                "energy_text": line[9:19].strip(),
                "energy": float(line[9:19].strip()) if line[9:19].strip() else None,
                "t_field": line[39:49].strip(),
                "dt_field": line[49:55].strip(),
                "xref": "",
                "t_blocks": [],
            }
            j = i + 1
            current = []
            while j < len(lines):
                nxt = lines[j]
                if len(nxt) >= 8 and nxt[5] == " " and nxt[6] == " " and nxt[7] == "L":
                    break
                xref_match = XREF_RE.match(nxt)
                if xref_match:
                    level["xref"] = re.sub(r"[^A-Z]", "", xref_match.group("xref"))
                if len(nxt) >= 9 and nxt[5] == " " and nxt[6:8] == "cL" and "T$" in nxt[9:]:
                    if current:
                        level["t_blocks"].append(current)
                    current = [(j + 1, nxt)]
                elif current and len(nxt) >= 9 and nxt[6:8] == "cL" and nxt[5].isdigit():
                    current.append((j + 1, nxt))
                elif current:
                    level["t_blocks"].append(current)
                    current = []
                j += 1
            if current:
                level["t_blocks"].append(current)
            lifetime_blocks = []
            for block in level["t_blocks"]:
                text = join_t_block([line for _, line in block])
                if "|t" in text or "lifetime" in text:
                    lifetime_blocks.append({
                        "lines": block,
                        "text": text,
                    })
            if level["energy"] is not None and level["energy"] >= 1230 and lifetime_blocks:
                level["lifetime_blocks"] = lifetime_blocks
                blocks.append(level)
            i = j
        else:
            i += 1
    return blocks


def nearest_source_entry(entries, energy):
    best = None
    best_delta = None
    for entry in entries:
        delta = abs(entry["energy"] - energy)
        if best is None or delta < best_delta:
            best = entry
            best_delta = delta
    if best is None or best_delta is None or best_delta > 5.0:
        return None
    return best


def java_average(items, unit):
    args = [str(PYTHON), str(JAVA_AVG)]
    for item in items:
        value = item["value_abs"] / UNIT_SCALE[unit]
        unc = item["unc_abs"] / UNIT_SCALE[unit]
        args.extend([format_float(value), format_float(unc)])
    proc = subprocess.run(args, capture_output=True, text=True, cwd=ROOT, check=True)
    out = proc.stdout
    match = SUGGESTED_RE.search(out)
    if not match:
        raise RuntimeError(out)
    value_unc = match.group("value")
    method = match.group("method")
    if "(" not in value_unc or not value_unc.endswith(")"):
        raise RuntimeError(value_unc)
    value_text = value_unc[: value_unc.index("(")]
    paren_unc = value_unc[value_unc.index("(") + 1 : -1]
    return value_text, paren_unc, method, out


def format_float(val):
    if abs(val) >= 100:
        return f"{val:.6g}"
    return f"{val:.10g}"


def absolute_to_comment_unc(value_text, unc_abs, unit):
    value = float(value_text)
    unit_scale = UNIT_SCALE[unit]
    value_in_unit = value
    # derive decimal places from displayed value text
    if "E" in value_text.upper():
        mantissa, exp = value_text.upper().split("E")
        decimals = len(mantissa.split(".")[1]) if "." in mantissa else 0
        digits = round(unc_abs / (unit_scale * (10 ** int(exp)) * (10 ** (-decimals))))
        return f"{{I{digits}}}"
    decimals = len(value_text.split(".")[1]) if "." in value_text else 0
    digits = round((unc_abs / unit_scale) * (10 ** decimals))
    return f"{{I{digits}}}"


def choose_t_unit(seconds):
    for idx, unit in enumerate(UNIT_ORDER):
        value = seconds / UNIT_SCALE[unit]
        if value <= 200:
            if value < 0.2 and idx > 0:
                smaller = UNIT_ORDER[idx - 1]
                smaller_val = seconds / UNIT_SCALE[smaller]
                if smaller_val <= 200:
                    return smaller
            return unit
    return "S"


def round_half_up(value, decimals):
    q = Decimal("1").scaleb(-decimals)
    return float(Decimal(str(value)).quantize(q, rounding=ROUND_HALF_UP))


def round_unc_4up(value, decimals):
    scaled = Decimal(str(value)) * (Decimal(10) ** decimals)
    if scaled >= 0:
        adjusted = (scaled + Decimal("0.0000000001"))
    else:
        adjusted = (scaled - Decimal("0.0000000001"))
    rounded_int = int(adjusted.to_integral_value(rounding=ROUND_HALF_UP))
    return rounded_int / (10 ** decimals)


def sig_digits_for_unc(unc):
    if unc == 0:
        return 1
    exponent = math.floor(math.log10(abs(unc)))
    scaled = unc / (10 ** exponent)
    first_two = int(scaled * 10 + 1e-9)
    return 2 if 10 <= first_two <= 34 else 1


def format_data_field(value_sec, unc_sec=None, op="="):
    unit = choose_t_unit(value_sec)
    value = value_sec / UNIT_SCALE[unit]
    if op in ("<", ">"):
        # preserve one decimal when integer rounding would distort the bound.
        for decimals in range(3, -1, -1):
            rounded = round_half_up(value, decimals)
            if decimals == 0:
                if abs(rounded - value) / value > 0.1 and value < 10:
                    continue
            text = f"{rounded:.{decimals}f}" if decimals else f"{rounded:.0f}"
            if "." in text:
                text = text.rstrip("0").rstrip(".") if decimals > 0 else text
            return f"{text} {unit}", "GT" if op == ">" else "LT"
    if isinstance(unc_sec, tuple):
        upper_unit = unc_sec[0] / UNIT_SCALE[unit]
        lower_unit = unc_sec[1] / UNIT_SCALE[unit]
        ref_unc = max(upper_unit, lower_unit)
        sig = sig_digits_for_unc(ref_unc)
        exponent = math.floor(math.log10(abs(ref_unc))) if ref_unc else 0
        decimals = max(0, sig - 1 - exponent)
        upper_rounded = round_unc_4up(upper_unit, decimals)
        lower_rounded = round_unc_4up(lower_unit, decimals)
        value_rounded = round_half_up(value, decimals)
        upper_digits = int(round(upper_rounded * (10 ** decimals))) if decimals else int(round(upper_rounded))
        lower_digits = int(round(lower_rounded * (10 ** decimals))) if decimals else int(round(lower_rounded))
        if decimals:
            value_text = f"{value_rounded:.{decimals}f}"
        else:
            value_text = f"{value_rounded:.0f}"
        return f"{value_text} {unit}", f"+{upper_digits}-{lower_digits}"
    value_unit = value
    unc_unit = unc_sec / UNIT_SCALE[unit]
    sig = sig_digits_for_unc(unc_unit)
    exponent = math.floor(math.log10(abs(unc_unit))) if unc_unit else 0
    decimals = max(0, sig - 1 - exponent)
    unc_rounded = round_unc_4up(unc_unit, decimals)
    value_rounded = round_half_up(value_unit, decimals)
    unc_digits = int(round(unc_rounded * (10 ** decimals))) if decimals else int(round(unc_rounded))
    if decimals:
        value_text = f"{value_rounded:.{decimals}f}"
    else:
        value_text = f"{value_rounded:.0f}"
    return f"{value_text} {unit}", str(unc_digits)


def item_phrase(item):
    if item["op"] == "=":
        return f"{item['value_text']} {item['unit'].lower()} {item['unc_text']} in {item['reaction']} from {item['nsr']} with {item['method']}"
    return f"{item['op']}{item['value_text']} {item['unit'].lower()} in {item['reaction']} from {item['nsr']} with {item['method']}"


def oxford_join(parts):
    if len(parts) == 1:
        return parts[0]
    if len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    return ", ".join(parts[:-1]) + f", and {parts[-1]}"


def wrap_cl(text):
    width = 71
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        tentative = word if not current else current + " " + word
        if len(tentative) <= width:
            current = tentative
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    out = []
    for idx, payload in enumerate(lines, start=1):
        prefix = " 34CL cL " if idx == 1 else f" 34CL{idx}cL "
        out.append((prefix + payload).ljust(80))
    return out


def proposed_comment(level, matched_entries):
    current_text = " ".join(block["text"] for block in level["lifetime_blocks"])
    current_style = "limit" if "|t<" in current_text or "|t>" in current_text else "value"
    finite = []
    limits = []
    for entry in matched_entries:
        for item in entry["items"]:
            if item["op"] == "=":
                finite.append(item)
            else:
                limits.append(item)
    finite.sort(key=lambda item: (level["xref"].find(item["dataset"]), item["nsr"], item["value_abs"]))
    limits.sort(key=lambda item: (level["xref"].find(item["dataset"]), item["nsr"], item["value_abs"]))

    if len(finite) >= 2:
        result_unit = finite[0]["unit"]
        value_text, paren_unc, method, raw_out = java_average(finite, result_unit)
        phrase = "weighted average" if "Weighted" in method else "unweighted average"
        lead = f"T$lifetime |t={value_text} {result_unit.lower()} {{I{paren_unc}}}: {phrase} of "
        lead += oxford_join([item_phrase(item) for item in finite]) + "."
        if limits:
            tag = "Other" if len(limits) == 1 else "Others"
            lead += f" {tag}: {oxford_join([item_phrase(item) for item in limits])}."
        value_sec = float(value_text) * UNIT_SCALE[result_unit]
        unc_sec = parse_uncertainty(value_text, f"{{I{paren_unc}}}") * UNIT_SCALE[result_unit]
        t_field, dt_field = format_data_field(value_sec * math.log(2), unc_sec * math.log(2), op="=")
        return lead, t_field, dt_field, raw_out

    if len(finite) == 1:
        finite_item = finite[0]
        use_limit = current_style == "limit" and limits
        if not use_limit:
            text = f"T$lifetime |t={finite_item['value_text']} {finite_item['unit'].lower()} {finite_item['unc_text']} in {finite_item['reaction']} from {finite_item['nsr']} with {finite_item['method']}."
            if limits:
                tag = "Other" if len(limits) == 1 else "Others"
                text += f" {tag}: {oxford_join([item_phrase(item) for item in limits])}."
            value_sec = finite_item["value_abs"]
            unc_sec = finite_item["unc_abs"]
            if isinstance(unc_sec, tuple):
                unc_sec = tuple(part * math.log(2) for part in unc_sec)
            else:
                unc_sec = unc_sec * math.log(2)
            t_field, dt_field = format_data_field(value_sec * math.log(2), unc_sec, op="=")
            return text, t_field, dt_field, None

    if limits:
        if any(item["op"] == ">" for item in limits):
            primary = max((item for item in limits if item["op"] == ">"), key=lambda item: item["value_abs"])
            others = [item for item in limits if item is not primary]
        else:
            primary = min((item for item in limits if item["op"] == "<"), key=lambda item: item["value_abs"])
            others = [item for item in limits if item is not primary]
        extras = []
        if finite:
            extras.extend(finite)
        extras.extend(others)
        text = f"T$lifetime |t{primary['op']}{primary['value_text']} {primary['unit'].lower()} in {primary['reaction']} from {primary['nsr']} with {primary['method']}."
        if extras:
            tag = "Other" if len(extras) == 1 else "Others"
            text += f" {tag}: {oxford_join([item_phrase(item) for item in extras])}."
        t_field, dt_field = format_data_field(primary["value_abs"] * math.log(2), None, op=primary["op"])
        return text, t_field, dt_field, None

    return None, None, None, None


def main():
    sources = {letter: parse_source_entries(cfg["path"], cfg["reaction"], letter) for letter, cfg in SOURCE_CONFIG.items()}
    adopted_blocks = parse_adopted_blocks(ADOPTED)
    for level in adopted_blocks:
        matched = []
        for letter in level["xref"]:
            if letter in sources:
                entry = nearest_source_entry(sources[letter], level["energy"])
                if entry:
                    matched.append(entry)
        if not matched:
            continue
        comment, t_field, dt_field, avg_out = proposed_comment(level, matched)
        if comment is None:
            continue
        new_l = level["l_line"][:39] + t_field.ljust(10) + dt_field.ljust(6) + level["l_line"][55:]
        print(f"LEVEL {level['energy_text']} line {level['l_line_no']} xref={level['xref']}")
        print(f"CURRENT T/DT: {level['t_field']} / {level['dt_field']}")
        print(f"PROPOSED T/DT: {t_field} / {dt_field}")
        print(f"PROPOSED L: {new_l}")
        for line in wrap_cl(comment):
            print(line)
        if avg_out:
            print("JAVA:")
            print(avg_out.rstrip())
        print("---")


if __name__ == "__main__":
    main()
