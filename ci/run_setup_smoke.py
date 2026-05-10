#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path


def main() -> int:
    status = json.loads(Path("/artifacts/plugin-status.json").read_text(encoding="utf-8"))
    assert status["dependencies"]["ok"] is True
    assert shutil.which("bw")
    assert shutil.which("mcp-server-bitwarden")
    assert status["auth"]["env"]["BW_CLIENT_SECRET"]["present"] in {True, False}
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
