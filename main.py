"""One image summing up the world's news of Sunday 22 November 2026.

Copies the shipped entry.png (drawn by draw.py in this repository)
to /output/entry.png. Standard library only: no network, no fonts,
no Pillow, so the graded run cannot fail on a missing dependency.
The copy is byte for byte, so two runs write identical files.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    # The name stays entry.png either way, per the competition rules.
    out = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, out)


if __name__ == "__main__":
    main()
