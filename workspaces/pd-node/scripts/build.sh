#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")"
cd $SCRIPT_DIR/../


uv sync

uv pip install -e .

#uv run pyinstaller --onedir --noconfirm -n pd-node pd_node/__main__.py
uv run pyinstaller --noconfirm pd-node.spec
