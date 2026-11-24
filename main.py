#!/usr/bin/env python3
"""Entry for make.fun: 'Say What Actually Broke'.

Writes one line of software error copy — the brutal truth about what
went wrong, in plain words, with the fix the user should try — to the
output entry file. Stdlib only, deterministic.
"""

import os
import sys

# The error line itself. It names the real failure (a DNS record that
# was deleted months ago finally took the site down), says what the
# team is doing about it, and tells the user what to do next.
LINE = (
    "It was DNS. It is always DNS. One record deleted in March "
    "waited until today to take the whole site down. We're putting "
    "it back \u2014 refresh in five minutes."
)

MAX_CHARS = 200


def output_path() -> str:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def verify(path: str) -> None:
    """Read the written file back and check it against the gate:
    UTF-8, 1-200 chars, not only whitespace, exactly one line,
    and byte-for-byte the intended line.
    """
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if text != LINE:
        raise SystemExit("verify failed: file content differs from LINE")
    if not (1 <= len(text) <= MAX_CHARS):
        raise SystemExit(f"verify failed: {len(text)} chars, gate is 1-{MAX_CHARS}")
    if not text.strip():
        raise SystemExit("verify failed: entry is only whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("verify failed: entry is not a single line")


def main() -> int:
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    verify(path)
    print(f"wrote {path} ({len(LINE)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
