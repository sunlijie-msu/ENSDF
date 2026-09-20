---
name: ensdf-header-setup
description: "Use when setting up or updating ENSDF headers for a new mass-chain evaluation cycle: creating new/old/raw/pdf folders, converting remaining .old/.xundl sources to new/*.ens, stamping the IDENTIFICATION record cols 66-80, and inserting the new History (H) record. Triggers: header update, mass chain setup, ENSDF 202609, H record, unconverted XUNDL file."
argument-hint: [mass number | element symbol | file path]
---

# ENSDF Header Setup

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

1. Folders: `new/` holds working `.ens` files only, sources live in `old/`; create `raw/` and `pdf/`.
2. Convert first: rename every remaining `.old`/`.xundl` in `new/` to a `.ens` dataset (evaluation file name, `:XUNDL-N` title suffix dropped), then stamp the header.
3. Header: IDENTIFICATION record cols 66-80 → `ENSDF    YYYYMM`; insert the new `H` record directly after the IDENTIFICATION record.
4. Run `python .github/scripts/update_headers.py <chain|isotope|file> [--check]`; it also flags unconverted `.old`/`.xundl` sources left in `new/`.
5. Validate with `.github/scripts/ensdf_1line_ruler.py --file <f> --show-only-wrong` and `.github/scripts/column_calibrate.py <f>`, then confirm via `git diff` that only header lines changed.
6. Never edit `old/` sources; only INSERT the new `H` record, keeping legacy `H` records unchanged; every record exactly 80 characters.
