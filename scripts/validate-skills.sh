#!/usr/bin/env bash
set -euo pipefail

export PYTHONUTF8=1
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPOSITORY_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN=python3
else
  PYTHON_BIN=python
fi

exec "${PYTHON_BIN}" "${SCRIPT_DIR}/validate-skills.py" --root "${REPOSITORY_ROOT}" "$@"
