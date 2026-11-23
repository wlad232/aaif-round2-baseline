#!/usr/bin/env bash
# Validate every case record and example in this repository.
# Same command a CI job would run; kept as a script because the maintainer's
# token here cannot push workflow files.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 schema/validate_records.py schema/examples/*.json
if compgen -G "records/*/*.json" > /dev/null; then
  python3 schema/validate_records.py records/*/*.json
fi
