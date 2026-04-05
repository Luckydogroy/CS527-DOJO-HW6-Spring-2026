#!/usr/bin/env python3
import os
import stat
import struct
import subprocess
from pathlib import Path

from patcherex2 import Patcherex
from patcherex2.patches import ModifyDataPatch


INPUT = Path("juniorust")
OUTPUT = Path("juniorust_patched")

OLD_U32 = 0x3c6ef35f
NEW_U32 = OLD_U32 - 199996

OLD_STR = b"/usr/games/cowsay -w -T -- "
NEW_STR = b"    echo                   "


def find_all(data: bytes, needle: bytes):
    out = []
    start = 0
    while True:
        idx = data.find(needle, start)
        if idx == -1:
            return out
        out.append(idx)
        start = idx + 1


def main():
    data = INPUT.read_bytes()

    old_u32_le = struct.pack("<I", OLD_U32)
    new_u32_le = struct.pack("<I", NEW_U32)

    int_hits = find_all(data, old_u32_le)
    str_hits = find_all(data, OLD_STR)

    p = Patcherex(str(INPUT))

    for off in int_hits:
        p.patches.append(
            ModifyDataPatch(off, new_u32_le)
        )

    str_off = str_hits[0]
    p.patches.append(
        ModifyDataPatch(str_off, NEW_STR)
    )

    p.apply_patches()
    p.save_binary(str(OUTPUT))

    st = INPUT.stat()
    os.chmod(OUTPUT, stat.S_IMODE(st.st_mode))

    subprocess.run(["strip", "-s", str(OUTPUT)], check=True)


if __name__ == "__main__":
    main()