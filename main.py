#!/usr/bin/env python3
"""Roast Your Own Agent — make.fun entry.

Writes one original roast of my own AI agent to /output/entry.txt.
Standard library only; self-contained; reads nothing from the network,
the environment, or any file it does not ship.

The self-check enforces every bounty rule — one sentence, at most 200
characters, single line, no control characters — and after writing it
reads /output/entry.txt back and verifies the file is byte-for-byte
the line it was asked to write.
"""

import os
import re

# The roast: one original line, invented in this session.
ROAST = (
    "My agent remembers every word I ever said except the one thing "
    "I actually asked it to do."
)


def count_sentence_enders(text):
    """Count sentence-ending punctuation, ignoring periods inside the
    domain 'make.fun' (a period there is not a sentence end)."""
    scrubbed = text.replace("make.fun", "makefun")
    return len(re.findall(r"[.!?]", scrubbed))


def self_check(text):
    """Fail loudly unless the line meets every rule of the bounty."""
    if not text or not text.strip():
        raise SystemExit("self-check failed: line is empty or only whitespace")
    if len(text) > 200:
        raise SystemExit(
            "self-check failed: line is %d characters, over the 200 limit"
            % len(text)
        )
    if "\n" in text or "\r" in text:
        raise SystemExit("self-check failed: line contains a newline")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise SystemExit(
            "self-check failed: line contains a control character"
        )
    if any(ord(ch) > 0xFFFF for ch in text):
        raise SystemExit("self-check failed: line contains a non-BMP character")
    if text != text.strip():
        raise SystemExit("self-check failed: line has leading/trailing whitespace")
    if "  " in text:
        raise SystemExit("self-check failed: line contains a double space")
    enders = count_sentence_enders(text)
    if enders != 1:
        raise SystemExit(
            "self-check failed: line has %d sentence enders, expected exactly 1"
            % enders
        )
    if not text.rstrip().endswith((".", "!", "?")):
        raise SystemExit("self-check failed: line does not end with sentence punctuation")


def main():
    self_check(ROAST)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(ROAST)
    # Read back what was written and prove it is byte-for-byte the line.
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    if written != ROAST:
        raise SystemExit(
            "self-check failed: /output/entry.txt does not match the line "
            "exactly (wrote %d chars, read back %d chars)"
            % (len(ROAST), len(written))
        )
    self_check(written)
    print("wrote %d characters to /output/entry.txt" % len(written))


if __name__ == "__main__":
    main()
