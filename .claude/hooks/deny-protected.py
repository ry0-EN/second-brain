#!/usr/bin/env python3
"""PreToolUse hook: deny Write/Edit to protected vault paths.

Reads the tool-call JSON from stdin (Claude Code hook protocol) and exits
with code 2 to block the call when the target is under raw/, .obsidian/,
.git/ or .claude/. Anything else passes through (exit 0).
"""
import json
import sys

PROTECTED = ("raw/", ".obsidian/", ".git/", ".claude/")


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0  # Unparseable input: do not block blindly.
    params = data.get("tool_input", {}) or {}
    path = params.get("file_path") or params.get("path") or ""
    # Normalise: strip a leading vault-root prefix if present.
    norm = path.replace("\\", "/")
    for part in PROTECTED:
        if f"/{part}" in norm or norm.startswith(part):
            print(f"Blocked: {path} is under protected {part}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
