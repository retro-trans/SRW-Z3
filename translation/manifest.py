"""Compatibility entry point; PS3 configuration lives in platforms/ps3."""
import runpy
from pathlib import Path

_config = runpy.run_path(str(Path(__file__).resolve().parents[1] /
                             "platforms/ps3/manifest.py"))
STAGES = _config["STAGES"]
LIBRARIES = _config["LIBRARIES"]
