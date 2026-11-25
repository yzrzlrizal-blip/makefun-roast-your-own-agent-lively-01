#!/usr/bin/env python3
"""Roast Your Own Agent — make.fun entry (program/v1).

Writes one original roast of the entrant's own AI agent to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt), where the
competition's gate scorer reads it.

Pure standard library, deterministic: every run writes the same bytes.
The roast is fixed text, no trailing newline.
"""

import os
import sys
import tempfile

# The roast. Fresh angle, no stock hallucination / toaster jokes:
# the agent's confident post-mortem habit — apologise, explain the bug
# with total confidence, then reproduce it with prettier formatting.
# Setup short, punchline at the end.
ROAST = (
    "My agent apologized for the mistake, confidently explained why it "
    "happened, then made it again with better formatting."
)

MAX_CHARS = 140


def main() -> int:
    if not 1 <= len(ROAST) <= MAX_CHARS:
        print(f"roast must be 1-{MAX_CHARS} characters, got {len(ROAST)}",
              file=sys.stderr)
        return 1
    if not ROAST.strip():
        print("roast must not be only whitespace", file=sys.stderr)
        return 1
    if "\n" in ROAST or "\r" in ROAST:
        print("roast must be a single line", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = ROAST.encode("utf-8")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    # Self-check: re-read and verify the gate (1-140 chars, one line,
    # not only whitespace, no trailing newline).
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if text != ROAST:
        print("verification failed: bytes on disk differ", file=sys.stderr)
        return 1
    if text.count("\n") != 0 or text.count("\r") != 0:
        print("verification failed: entry is not a single line",
              file=sys.stderr)
        return 1
    if not 1 <= len(text) <= MAX_CHARS or not text.strip():
        print("verification failed: entry outside the 1-140 gate",
              file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(ROAST)} chars)")
    print(ROAST)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
