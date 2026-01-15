import argparse
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser(description="Resume Agent (MVP)")
    parser.add_argument("--jd", required=True, help="Path to job description (txt or pdf)")
    parser.add_argument("--inventory", default="resume_inventory/master.yaml", help="Path to master inventory YAML")
    parser.add_argument("--out", default="outputs/tailored.tex", help="Output LaTeX file path")
    args = parser.parse_args()

    jd_path = Path(args.jd)
    inv_path = Path(args.inventory)
    out_path = Path(args.out)

    if not jd_path.exists():
        raise SystemExit(f"JD file not found: {jd_path}")
    if not inv_path.exists():
        raise SystemExit(f"Inventory file not found: {inv_path}")

    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Placeholder pipeline output for now (next commit will implement parse/analyze)
    out_path.write_text(
        "% Tailored LaTeX will be generated here.\n"
        f"% JD: {jd_path}\n"
        f"% Inventory: {inv_path}\n",
        encoding="utf-8"
    )

    print(f"Generated: {out_path}")

if __name__ == "__main__":
    main()