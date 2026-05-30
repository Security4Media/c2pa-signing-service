#!/usr/bin/env python3
import json
import sys
from pathlib import Path

spec_path = Path(sys.argv[1])
spec = json.loads(spec_path.read_text(encoding="utf-8"))
paths = spec.get("paths")
if not isinstance(paths, dict) or not paths:
    raise SystemExit(f"{spec_path}: OpenAPI paths must not be empty")
print(f"{spec_path}: {len(paths)} paths")
