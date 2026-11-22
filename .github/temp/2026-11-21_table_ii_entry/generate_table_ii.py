from __future__ import annotations

import re
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "FRIENDS" / "2027GOAA_Table_II.md"
OUTPUT = Path(__file__).with_name("expected_records.txt")


def cells(line: str) -> list[str]:
    return [cell.strip().replace("\\\\", "\\") for cell in line.strip().strip("|").split("|")]


def parts(text: str) -> list[str]:
    return [item.strip() for item in text.split("<br>")]


def number(text: str) -> tuple[str, str | None]:
    match = re.search(r"(?<![A-Za-z])([+-]?\d+(?:\.\d+)?)(?:\((\d+)\))?", text)
    if not match:
        raise ValueError(f"No numeric value found: {text!r}")
    return match.group(1), match.group(2)


def field(value: str, width: int, name: str) -> str:
    if len(value) > width:
        raise ValueError(f"{name} does not fit ({width}): {value!r}")
    return value.ljust(width)


def uncertainty_digits(value: Decimal) -> tuple[Decimal, int]:
    if value <= 0:
        raise ValueError(f"Uncertainty must be positive: {value}")
    exponent = value.adjusted()
    leading_two = int(value.scaleb(1 - exponent))
    significant = 2 if 10 <= leading_two <= 34 else 1
    target_exponent = exponent - significant + 1
    rounded = value
    for quantum_exponent in range(value.as_tuple().exponent + 1, target_exponent + 1):
        quantum = Decimal(1).scaleb(quantum_exponent)
        scaled = rounded / quantum
        whole = int(scaled)
        first_discarded = int((scaled - whole) * 10)
        if first_discarded >= 4:
            whole += 1
        rounded = Decimal(whole) * quantum
    quantum = Decimal(1).scaleb(target_exponent)
    rounded = rounded.quantize(quantum)
    if rounded.adjusted() > exponent:
        target_exponent = rounded.adjusted() - significant + 1
        quantum = Decimal(1).scaleb(target_exponent)
        rounded = rounded.quantize(quantum)
    return rounded, int(rounded / quantum)


def measurement_fields(value_text: str, uncertainty_text: str | None) -> tuple[str, str]:
    if uncertainty_text is None:
        return value_text, ""
    if len(uncertainty_text) <= 2:
        return value_text, uncertainty_text
    decimals = max(0, -Decimal(value_text).as_tuple().exponent)
    exact_uncertainty = Decimal(uncertainty_text).scaleb(-decimals)
    rounded_uncertainty, uncertainty = uncertainty_digits(exact_uncertainty)
    places = max(0, -rounded_uncertainty.as_tuple().exponent)
    quantum = Decimal(1).scaleb(-places)
    rounded_value = Decimal(value_text).quantize(quantum, rounding=ROUND_HALF_UP)
    return f"{rounded_value:.{places}f}", str(uncertainty)


def round_uncertainty_digits(digits: str, decimals: int) -> tuple[Decimal, int]:
    exact = Decimal(digits).scaleb(-decimals)
    rounded, _ = uncertainty_digits(exact)
    return rounded, max(0, -rounded.as_tuple().exponent)


def logft_fields(text: str) -> tuple[str, str]:
    match = re.search(r"(\d+\.\d+)_\{-([0-9]+)\}\^\{\+([0-9]+)\}", text)
    if not match:
        raise ValueError(f"Malformed log ft: {text!r}")
    value, lower, upper = match.groups()
    exact_uncertainty = f"+{upper}-{lower}"
    if len(exact_uncertainty) <= 6:
        return value, exact_uncertainty
    decimals = len(value.split(".", 1)[1])
    lower_value, lower_places = round_uncertainty_digits(lower, decimals)
    upper_value, upper_places = round_uncertainty_digits(upper, decimals)
    places = max(lower_places, upper_places)
    rounded_value = Decimal(value).quantize(
        Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP
    )
    lower_out = str(int(lower_value.scaleb(places)))
    upper_out = str(int(upper_value.scaleb(places)))
    return f"{rounded_value:.{places}f}", f"+{upper_out}-{lower_out}"


def spin(text: str) -> str:
    value = text.replace("\\(", "").replace("\\)", "").strip()
    tentative = r"\text{a}" in value or r"\text{c}" in value
    value = re.sub(r"\^\{([+-]?)\s*\\text\{[ac]\}\}", r"\1", value)
    value = re.sub(r"\s*\(IAS\)", "", value)
    value = value.replace(r"\text{ to }", "TO")
    value = value.replace("^+", "+").replace("^-", "-")
    value = value.replace(" ", "")
    value = value.replace(r"\text{", "").replace("}", "")
    if tentative and not (value.startswith("(") and value.endswith(")")):
        value = f"({value})"
    return value


def base_record(kind: str) -> list[str]:
    line = [" "] * 80
    line[:5] = list(" 23MG")
    line[7] = kind
    return line


def ensdf_line(kind: str, energy: str = "", de: str = "") -> list[str]:
    line = base_record(kind)
    line[9:19] = list(field(energy, 10, "energy"))
    line[19:21] = list(field(de, 2, "energy uncertainty"))
    return line


def record_from_row(row: list[str], output: list[str]) -> None:
    if len(row) == 10:
        jtext, etext, ti_text, logtext, final_text, gamma_text, ri_text, p_final, p_energy, p_intensity = row
    elif len(row) == 7:
        jtext, etext, ti_text, logtext, final_text, eptext, iptext = row
        gamma_text = ri_text = ""
        p_final, p_energy, p_intensity = final_text, eptext, iptext
    else:
        raise ValueError(f"Unexpected Table II row width {len(row)}: {row!r}")

    level_e, level_de = number(etext)
    level_e, level_de = measurement_fields(level_e, level_de)
    level = ensdf_line("L", level_e, level_de or "")
    spin_value = spin(jtext)
    level[22:39] = list(field(spin_value, 17, "Jπ"))
    output.append("".join(level))
    if r"\text{c}" in jtext:
        output.append(
            " 23MG cL J$Tentative assignment based on assumed allowed |b decay (2027GoAA)."
        )
    if Decimal(level_e) == Decimal("7801.45"):
        output.append(" 23MG cL J$IAS of {+23}Al g.s.")

    proton_comment: str | None = None
    proton_intensity_comment: str | None = None
    if p_energy not in {"—", "-", ""}:
        p_e, p_de = number(p_energy)
        p_final_e, _ = number(p_final)
        final_state = {
            "0": (0, "to {+22}Na g.s."),
            "583": (1, "to {+22}Na 1st excited state"),
            "891": (2, "to {+22}Na 2nd excited state"),
        }
        try:
            p_index, final_clause = final_state[p_final_e]
        except KeyError as error:
            raise ValueError(f"Unknown proton final level: {p_final_e}") from error
        p_uncertainty = f" {{I{p_de}}}" if p_de else ""
        proton_comment = (
            f" 23MG cL $E(p{p_index}){{-c.m.}}={p_e}{p_uncertainty} "
            f"{final_clause} (2027GoAA)."
        )
        if p_intensity not in {"—", "-", ""}:
            if "<" in p_intensity:
                p_value = number(p_intensity)[0]
                proton_intensity_comment = f" 23MG cE $Ip<{p_value} (2027GoAA)."
            else:
                p_value, p_uncertainty_digits = number(p_intensity)
                proton_intensity_comment = (
                    f" 23MG cE $Ip={p_value} {{I{p_uncertainty_digits}}} (2027GoAA)."
                )
    if proton_comment:
        output.append(proton_comment)

    e_record = base_record("E")
    if logtext not in {"—", "-", ""}:
        logft, dft = logft_fields(logtext)
        e_record[42:49] = list(field(logft, 7, "log ft"))
        e_record[49:55] = list(field(dft, 6, "log ft uncertainty"))
    intensity, dintensity = number(ti_text)
    e_record[64:74] = list(field(intensity, 10, "TI"))
    e_record[74:76] = list(field(dintensity or "", 2, "DTI"))
    output.append("".join(e_record))
    asymmetric = re.search(r"(\d+\.\d+)_\{-([0-9]+)\}\^\{\+([0-9]+)\}", logtext)
    if asymmetric:
        original, lower, upper = asymmetric.groups()
        if (len(lower) > 2) != (len(upper) > 2):
            output.append(f" 23MG cE LOGFT${original} {{I+{upper}-{lower}}} (2027GoAA).")
    if proton_intensity_comment:
        output.append(proton_intensity_comment)
    if Decimal(level_e) == Decimal("7785.32"):
        output.append(
            " 23MG cE $%Ip=0.0255 {I33} (2027GoAA), Ip=0.0257 {I17} (2020FR04)."
        )
    elif Decimal(level_e) == Decimal("7853.74"):
        output.append(" 23MG cE $%Ip=0.119 {I8} (2027GoAA).")

    if gamma_text not in {"—", "-", ""}:
        ef = parts(final_text)
        eg = parts(gamma_text)
        ri = parts(ri_text)
        if not (len(ef) == len(eg) == len(ri)):
            raise ValueError(f"Gamma columns differ in length at Ei={level_e}: {ef}, {eg}, {ri}")
        gammas: list[list[str]] = []
        for energy_text, ri_text_item in zip(eg, ri):
            gamma_e, gamma_de = number(energy_text)
            gamma_e, gamma_de = measurement_fields(gamma_e, gamma_de)
            rel_i, drel_i = number(ri_text_item)
            gamma = ensdf_line("G", gamma_e, gamma_de or "")
            gamma[22:29] = list(field(rel_i, 7, "RI"))
            gamma[29:31] = list(field(drel_i or "", 2, "DRI"))
            if r"\text{b}" in energy_text:
                gamma[76] = "B"
            gammas.append(gamma)
        gammas.sort(key=lambda line: Decimal("".join(line[9:19]).strip()))
        for gamma in gammas:
            output.append("".join(gamma))
            if gamma[76] == "B":
                output.append(" 23MG cG E(B)$Newly observed |g transition (2027GoAA).")


def main() -> None:
    output: list[str] = []
    section = 0
    for line in SOURCE.read_text(encoding="utf-8").splitlines():
        if line.startswith("#### **1."):
            section = 1
            continue
        if line.startswith("#### **2."):
            section = 2
            continue
        if not line.startswith("|") or "---" in line:
            continue
        row = cells(line)
        if row[0].startswith(r"\("):
            if len(row) in {7, 10} and "J_i" not in row[0]:
                record_from_row(row, output)
    output.insert(
        0,
        " 23MG c  Table II I(p) normalized to I(p)(869)+I(p)(898)=1.",
    )
    output.insert(
        1,
        " 23MG2c  Corresponding absolute I(p) intensity is 0.41(1)% (2027GoAA).",
    )
    for index, record in enumerate(output):
        if len(record) > 80:
            raise ValueError(f"ENSDF line exceeds 80 columns: {record!r}")
        output[index] = record.ljust(80)
    OUTPUT.write_text("\n".join(output) + "\n", encoding="ascii", newline="\n")
    levels = sum(len(line) == 80 and line[6] == " " and line[7] == "L" for line in output)
    gammas = sum(len(line) == 80 and line[6] == " " and line[7] == "G" for line in output)
    print(
        f"Wrote {len(output)} expected data/comment lines "
        f"({levels} L, {levels} E, {gammas} G) to {OUTPUT}"
    )


if __name__ == "__main__":
    main()
