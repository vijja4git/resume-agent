import argparse
from pathlib import Path

from agent.parse_jd import parse_jd
from agent.analyze import analyze_jd, analysis_to_json
from agent.strategy import build_strategy_plan, plan_to_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Resume Agent (MVP)")
    parser.add_argument("--jd", required=True, help="Path to job description (txt or pdf)")
    parser.add_argument("--inventory", default="resume_inventory/master.yaml", help="Path to master inventory YAML")
    parser.add_argument("--outdir", default="outputs", help="Output directory")
    parser.add_argument("--run", default="analysis", choices=["analysis", "strategy"], help="Pipeline stage to run")
    args = parser.parse_args()

    jd_path = Path(args.jd)
    inv_path = Path(args.inventory)
    outdir = Path(args.outdir)

    if not jd_path.exists():
        raise SystemExit(f"JD file not found: {jd_path}")
    if not inv_path.exists():
        raise SystemExit(f"Inventory file not found: {inv_path}")

    outdir.mkdir(parents=True, exist_ok=True)

    # Always parse + save cleaned JD (useful for debugging)
    parsed = parse_jd(jd_path)
    cleaned_path = outdir / "jd.cleaned.txt"
    cleaned_path.write_text(parsed.cleaned_text, encoding="utf-8")

    # Always produce analysis when running strategy (strategy depends on it)
    analysis = analyze_jd(parsed.cleaned_text)
    analysis_path = outdir / "jd.analysis.json"
    analysis_path.write_text(analysis_to_json(analysis), encoding="utf-8")

    if args.run == "analysis":
        print(f"Saved cleaned JD: {cleaned_path}")
        print(f"Saved analysis JSON: {analysis_path}")
        return

    if args.run == "strategy":
        plan = build_strategy_plan(inv_path, analysis_path, top_k_exp=3, top_k_proj=3)
        plan_path = outdir / "strategy.plan.json"
        plan_path.write_text(plan_to_json(plan), encoding="utf-8")
        print(f"Saved cleaned JD: {cleaned_path}")
        print(f"Saved analysis JSON: {analysis_path}")
        print(f"Saved strategy plan: {plan_path}")
        return


if __name__ == "__main__":
    main()