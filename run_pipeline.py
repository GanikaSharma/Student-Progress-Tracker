#!/usr/bin/env python3
"""
run_pipeline.py

A lightweight, robust pipeline runner for the Student-Progress-Tracker project.
It tries to call functions from `src` modules if available, otherwise falls back
to running scripts in `scripts/`.

Usage examples:
  # run the whole pipeline
  python run_pipeline.py --all

  # run specific steps
  python run_pipeline.py --steps generate preprocess features train evaluate

  # see help
  python run_pipeline.py --help
"""

import argparse
import importlib
import subprocess
import sys
import os
from pathlib import Path
import logging

# ---- config ----
ROOT = Path(__file__).resolve().parent
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
MODELS_DIR = ROOT / "models"
REPORTS_DIR = ROOT / "reports" / "figures"
SCRIPTS_DIR = ROOT / "scripts"
SRC_DIR = ROOT / "src"

# Ensure directories exist
for d in (DATA_RAW, DATA_PROCESSED, MODELS_DIR, REPORTS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# ---- logging ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("run_pipeline")

# ---- helpers ----
def run_script(script_path, args=None):
    """Run an external Python script with subprocess in project root."""
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd += args
    log.info("Running script: %s", " ".join(cmd))
    res = subprocess.run(cmd, cwd=ROOT)
    if res.returncode != 0:
        raise RuntimeError(f"Script {script_path} failed (exit {res.returncode})")
    return res

def call_src_function(module_name, func_name="main", *args, **kwargs):
    """
    Try to import src.<module_name> and call func_name(...).
    If not present, return False.
    """
    try:
        mod = importlib.import_module(f"src.{module_name}")
        fn = getattr(mod, func_name, None)
        if fn is None:
            log.warning("Module src.%s has no function '%s'", module_name, func_name)
            return False
        log.info("Calling src.%s.%s()", module_name, func_name)
        fn(*args, **kwargs)
        return True
    except ModuleNotFoundError:
        log.info("Module src.%s not found, fallback to scripts if available", module_name)
        return False

# ---- pipeline steps ----
def step_generate():
    """
    Ensure raw dataset exists. Prefer src/data_generation.generate() else scripts/generate_data.py
    """
    # try src.data_generation.generate(n=100)
    if call_src_function("data_generation", "generate", n=100):
        return
    # fallback to scripts/generate_data.py
    script = SCRIPTS_DIR / "generate_data.py"
    if script.exists():
        run_script(script)
    else:
        log.warning("No data generation script found at %s — skipping generation", script)

def step_preprocess():
    """
    Run preprocessing that creates processed CSV in data/processed.
    Prefer src.data_preprocessing.main() else scripts/preprocess.py or notebooks approach.
    """
    if call_src_function("data_preprocessing", "main"):
        return
    # try scripts/preprocess.py or scripts/generate_processed.py
    for script_name in ("preprocess.py", "data_preprocessing.py", "generate_processed.py"):
        script = SCRIPTS_DIR / script_name
        if script.exists():
            run_script(script)
            return
    log.warning("No preprocessing script found in scripts/. Ensure data/processed exists.")

def step_features():
    """
    Optional feature engineering; prefer src.feature_engineering.main()
    """
    if call_src_function("feature_engineering", "main"):
        return
    script = SCRIPTS_DIR / "feature_engineering.py"
    if script.exists():
        run_script(script)
        return
    log.info("No feature engineering script; assuming processed data ready.")

def step_train():
    """
    Train baseline and improved models; prefer src.model_training.train_all()
    """
    if call_src_function("model_training", "train_all"):
        return
    # fallback to scripts/train_model.py
    script = SCRIPTS_DIR / "train_model.py"
    if script.exists():
        run_script(script)
        return
    log.warning("No training script found; ensure notebooks trained models and models/ contains artifacts.")

def step_evaluate():
    """
    Evaluate saved models and create summary CSV/figures.
    """
    if call_src_function("evaluate", "main"):
        return
    script = SCRIPTS_DIR / "evaluate_model.py"
    if script.exists():
        run_script(script)
        return
    log.info("No evaluation script found; you may have notebooks performing evaluation.")

def step_save_artifacts():
    """
    Ensure models/, reports/ contain relevant files (no-op here, placeholder for custom saves).
    """
    log.info("Models directory: %s", MODELS_DIR)
    log.info("Reports directory: %s", REPORTS_DIR)
    # create a small manifest
    manifest = {
        "models": [str(p.name) for p in MODELS_DIR.glob("*")],
        "reports": [str(p.name) for p in REPORTS_DIR.glob("*")],
    }
    manifest_path = MODELS_DIR / "artifacts_manifest.txt"
    with open(manifest_path, "w") as f:
        f.write("Models and reports generated by run_pipeline.py\n")
        for k, v in manifest.items():
            f.write(f"{k}:\n")
            for item in v:
                f.write(f"  - {item}\n")
    log.info("Artifacts manifest written to %s", manifest_path)

def step_dashboard():
    """
    Optional step — build static assets for dashboard or print instruction to run Streamlit.
    """
    streamlit_app = ROOT / "app" / "app.py"
    if streamlit_app.exists():
        log.info("Streamlit app found at %s. To run the dashboard:\n  (venv) python -m streamlit run %s", streamlit_app, streamlit_app)
    else:
        log.info("No Streamlit app found (app/app.py). Skipping dashboard step.")

# ---- main runner ----
ALL_STEPS = {
    "generate": step_generate,
    "preprocess": step_preprocess,
    "features": step_features,
    "train": step_train,
    "evaluate": step_evaluate,
    "save": step_save_artifacts,
    "dashboard": step_dashboard,
}

def parse_args():
    p = argparse.ArgumentParser(description="Run project pipeline steps.")
    p.add_argument("--all", action="store_true", help="Run all pipeline steps in order")
    p.add_argument("--steps", nargs="+", choices=list(ALL_STEPS.keys()), help="Steps to run (space separated)")
    return p.parse_args()

def main():
    args = parse_args()
    if args.all or not args.steps:
        # default: run sensible core pipeline
        steps_to_run = ["generate", "preprocess", "features", "train", "evaluate", "save"]
    else:
        steps_to_run = args.steps

    log.info("Pipeline start. Steps to run: %s", steps_to_run)
    for step in steps_to_run:
        try:
            log.info("=== STEP: %s ===", step)
            ALL_STEPS[step]()
        except Exception as e:
            log.exception("Step '%s' failed: %s", step, e)
            sys.exit(1)

    log.info("Pipeline finished successfully.")

if __name__ == "__main__":
    main()
