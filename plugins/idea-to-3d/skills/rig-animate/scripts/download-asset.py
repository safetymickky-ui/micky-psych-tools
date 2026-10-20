#!/usr/bin/env python3
"""
Downloads a GLB file from a Meshy rigging or animation URL into work/<slug>/meshy/,
verifies the glTF binary header (magic 'glTF'), and writes atomically.
"""
from __future__ import annotations

import argparse
import os
import struct
import sys
import urllib.parse
import urllib.request


def download_glb(url: str, dest_path: str, timeout: int = 120) -> int:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Only HTTP/HTTPS URLs are allowed, got: {parsed.scheme}")

    abs_dest = os.path.abspath(dest_path)
    os.makedirs(os.path.dirname(abs_dest), exist_ok=True)
    tmp_dest = abs_dest + ".tmp"

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "idea-to-3d-plugin/1.0"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()

    if len(data) < 20:
        raise ValueError(f"Downloaded file is too small ({len(data)} bytes) to be a valid GLB")
    magic, version, total_len = struct.unpack_from("<4sII", data, 0)
    if magic != b"glTF":
        raise ValueError(f"Downloaded file does not have glTF magic header (got {magic!r})")

    with open(tmp_dest, "wb") as f:
        f.write(data)
    os.replace(tmp_dest, abs_dest)
    return len(data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Download a Meshy rigging/animation GLB URL")
    parser.add_argument("url", help="HTTPS URL to the .glb asset")
    parser.add_argument("dest", help="Destination .glb file path")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args(argv)

    size = download_glb(args.url, args.dest, timeout=args.timeout)
    print(f"Downloaded {os.path.abspath(args.dest)} ({size / 1048576:.2f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
