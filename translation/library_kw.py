# -*- coding: utf-8 -*-
"""KW library descriptions, assembled from the per-batch JSON files.

A thin shim so build_project.py can keep loading this by path. All the real
logic is tools/trdata.py; nothing here executes a translation file.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import trdata  # noqa: E402

_here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library")
_glossary = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                         "analysis", "glossary.json")
ENTRIES, NAMES = trdata.assemble(_here, "kw", trdata.ambiguous_terms(_glossary))
