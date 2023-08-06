# ******************************************************************************
#
# pdflatex2, a Python/PDFLaTeX interface.
#
# Copyright 2022 Jeremy A Gray <gray@flyquackswim.com>.  All rights
# reserved.
# Copyright 2019 Marcelo Bello.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""Sphinx documentation configuration."""

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "pdflatex2"
copyright = "2022, Jeremy A Gray; 2019 Marcelo Belo"
author = "Jeremy A Gray, Marcelo Belo"
release = "0.1.4"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
]

autosummary_generate = True

# All paths relative to this directory.
templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]
html_static_path = ["_static"]

html_theme = "alabaster"
