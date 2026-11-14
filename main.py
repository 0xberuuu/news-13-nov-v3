#!/usr/bin/env python3
"""Entrypoint for the news-image-01 V3 entry.

Copies the pre-rendered entry.png (drawn by render.py, kept beside this
file) to the output directory as entry.png. Standard library only.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("missing entry.png next to main.py", file=sys.stderr)
        return 1
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        print("copy size mismatch", file=sys.stderr)
        return 1
    print("wrote", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
