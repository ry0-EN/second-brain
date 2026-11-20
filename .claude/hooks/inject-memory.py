#!/usr/bin/env python3
"""SessionStart hook: inject the vault's memory into every session.

Outputs index.md (catalog), DECISIONS.md, the tail of log.md (recent
work) and mistake.md (past mistakes + prevention rules) as additional
context, so a headless or interactive run physically starts with the
accumulated memory in context instead of relying on the model to
remember to read the files.
"""
import json
import os
import sys

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", ".")
MAX_CHARS = 12000


def read(rel, tail_lines=None):
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            text = f.read()
    except Exception:
        return ""
    if tail_lines:
        text = "\n".join(text.splitlines()[-tail_lines:])
    return text.strip()


def main() -> int:
    parts = []
    for rel, tail in (
        ("wiki/index.md", None),
        ("DECISIONS.md", None),
        ("wiki/log.md", 30),
        ("Knowledge/mistakes.md", None),
    ):
        body = read(rel, tail)
        if body:
            parts.append(f"===== {rel} =====\n{body}")
    import glob as _glob

    for path in sorted(_glob.glob(os.path.join(ROOT, "Preferences", "*.md"))):
        try:
            with open(path, encoding="utf-8") as f:
                body = f.read().strip()
        except Exception:
            body = ""
        if body:
            rel = os.path.relpath(path, ROOT)
            parts.append(f"===== {rel} =====\n{body}")
    context = "\n\n".join(parts)[:MAX_CHARS]
    if not context:
        return 0
    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": (
                "以下はこのVaultに蓄積された記憶（カタログ・決定事項・最近の作業記録・"
                "過去のミスと再発防止ルール）です。作業前に必ず内容を踏まえること。\n\n"
                + context
            ),
        }
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
