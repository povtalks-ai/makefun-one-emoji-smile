#!/usr/bin/env python3
"""One Emoji, One Smile — make.fun bounty entry.

The program writes exactly one emoji to ``entry.txt`` in the output
directory: the single emoji most likely to make a stranger smile.

The emoji was chosen against the judge's brief. It must read as warm
and friendly at first glance, need no context, and mean the same
thing to a stranger of any age or background. Heart hands say
"thank you, I appreciate you" in every language, with no irony and
no in-joke that could land wrong.

Run locally with:
    MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
The grader runs it with the output directory mounted at ``/output``.
"""

from __future__ import annotations

import os
import sys

# The entry: exactly one emoji, nothing else. One character, inside
# the competition gate of 1 to 8 characters.
EMOJI = "\U0001faf6"  # 🫶 heart hands

# The competition gate, mirrored here so a bad entry fails loudly
# during the build instead of silently at grading time.
MIN_CHARS = 1
MAX_CHARS = 8


def output_dir() -> str:
    """Return the directory the entry file goes in.

    The grader mounts a writable ``/output``; a local run may point
    somewhere else with MAKEFUN_OUTPUT_DIR. An empty value counts
    as unset.
    """
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def validate(emoji: str) -> None:
    """Reject anything that is not exactly one emoji in the gate."""
    if not emoji or emoji != emoji.strip():
        raise ValueError("entry must not be empty or padded with space")
    if len(emoji) < MIN_CHARS or len(emoji) > MAX_CHARS:
        raise ValueError(
            f"entry must be {MIN_CHARS}-{MAX_CHARS} characters, "
            f"got {len(emoji)}"
        )
    if len(emoji.split()) != 1:
        raise ValueError("entry must be exactly one emoji, nothing else")


def main() -> int:
    validate(EMOJI)
    directory = output_dir()
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(EMOJI)
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != EMOJI:
        raise ValueError("read-back mismatch: entry.txt does not hold the emoji")
    if len(written.encode("utf-8")) != len(EMOJI.encode("utf-8")):
        raise ValueError("read-back mismatch: entry.txt bytes differ")
    print(f"wrote {path}: {EMOJI!r} ({len(EMOJI)} character)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
