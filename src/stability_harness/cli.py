import argparse,json
from pathlib import Path
from .core import run_sweep

def main()->None:
    p=argparse.ArgumentParser(); p.add_argument("config"); p.add_argument("--output",default="output/report.json"); a=p.parse_args(); result=run_sweep(json.loads(Path(a.config).read_text())); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2)); print(json.dumps(result,indent=2)); raise SystemExit(0 if result["passed"] else 2)
