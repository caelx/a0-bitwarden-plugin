#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bitwarden Agent Zero plugin maintenance")
    parser.add_argument(
        "command", nargs="?", default="status", choices=["setup", "status", "repair", "uninstall"]
    )
    parser.add_argument("--noninteractive", action="store_true")
    parser.add_argument("--skip-system-deps", action="store_true")
    args = parser.parse_args(argv)

    from plugin_imports import plugin_import

    redact_data = plugin_import("helpers.redaction").redact_data

    if args.command == "status":
        collect_status = plugin_import("helpers.diagnostics").collect_status
        result = collect_status()
        print(json.dumps(redact_data(result), indent=2, sort_keys=True))
        return 0
    if args.command in {"setup", "repair"}:
        setup_plugin = plugin_import("helpers.setup").setup_plugin
        result = setup_plugin(
            noninteractive=args.noninteractive,
            skip_system_deps=args.skip_system_deps,
            repair=args.command == "repair",
        )
        print(json.dumps(redact_data(result), indent=2, sort_keys=True))
        return 0 if result.get("ok") else 1
    if args.command == "uninstall":
        uninstall = plugin_import("helpers.uninstall").uninstall
        result = uninstall()
        print(json.dumps(redact_data(result), indent=2, sort_keys=True))
        return 0 if result.get("ok") else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
