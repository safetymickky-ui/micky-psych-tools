#!/usr/bin/env python3
"""
Composites concept images or turnaround views (front, side, back) into a labelled
comparison sheet, and validates/normalizes turnaround images for Meshy (1:1, >=1024px, PNG).
"""
from __future__ import annotations

import argparse
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont


def load_font(size: int = 24) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in (
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if os.path.exists(candidate):
            try:
                return ImageFont.truetype(candidate, size)
            except OSError:
                pass
    return ImageFont.load_default()


def normalize_for_meshy(path: str, min_size: int = 1024) -> tuple[int, int]:
    """Ensure an image is a square 1:1 RGB/RGBA PNG of at least min_size x min_size."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    side = max(w, h, min_size)
    if w != h:
        # Pad with corner background colour to 1:1
        bg_px = img.getpixel((0, 0))
        square = Image.new("RGBA", ( max(w, h), max(w, h) ), bg_px)
        square.alpha_composite(img, ((max(w, h) - w) // 2, (max(w, h) - h) // 2))
        img = square
    if img.width < min_size:
        img = img.resize((side, side), Image.Resampling.LANCZOS)
    img.save(path, format="PNG")
    return img.size


def make_sheet(
    out_path: str,
    title: str,
    items: list[tuple[str, str]],
    tile_size: int = 420,
    cols: int = 4,
) -> str:
    if not items:
        raise ValueError("No images provided for sheet")
    cols = min(cols, len(items))
    rows = math.ceil(len(items) / cols)
    pad = 20
    header_h = 56
    label_h = 38

    width = pad + cols * (tile_size + pad)
    height = header_h + rows * (tile_size + label_h + pad)
    sheet = Image.new("RGBA", (width, height), (30, 31, 34, 255))
    draw = ImageDraw.Draw(sheet)
    title_font = load_font(24)
    label_font = load_font(18)

    draw.text((pad, 14), title, fill=(240, 242, 245, 255), font=title_font)

    for idx, (img_path, label) in enumerate(items):
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Missing image for sheet: {img_path}")
        r = idx // cols
        c = idx % cols
        x = pad + c * (tile_size + pad)
        y = header_h + r * (tile_size + label_h + pad)

        tile = Image.open(img_path).convert("RGBA")
        tile = tile.resize((tile_size, tile_size), Image.Resampling.LANCZOS)
        sheet.alpha_composite(tile, (x, y))
        draw.text((x + 6, y + tile_size + 6), label, fill=(220, 224, 230, 255), font=label_font)

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    sheet.convert("RGB").save(out_path, format="PNG")
    return os.path.abspath(out_path)


def _parse_item_spec(raw: str) -> tuple[str, str]:
    """Parse 'path=Label', 'Label=path', or 'path' into (path, label)."""
    if "=" not in raw:
        return raw, os.path.splitext(os.path.basename(raw))[0]
    left, right = raw.split("=", 1)
    left_s, right_s = left.strip(), right.strip()
    img_exts = (".png", ".jpg", ".jpeg", ".webp")
    if os.path.exists(left_s) or (left_s.lower().endswith(img_exts) and not os.path.exists(right_s)):
        return left_s, right_s
    if os.path.exists(right_s) or right_s.lower().endswith(img_exts):
        return right_s, left_s
    return left_s, right_s


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create concept or turnaround sheet and validate Meshy input images")
    parser.add_argument("--out", required=True, help="Output PNG sheet path")
    parser.add_argument("--title", default=None, help="Header title")
    parser.add_argument("--slug", default=None, help="Optional character slug for default header title")
    parser.add_argument("--normalize", action="store_true", help="Normalize input images to >=1024px 1:1 PNG")
    parser.add_argument("--labels", default=None, help="Optional comma-separated labels when using --images")
    parser.add_argument("--images", nargs="*", default=None, help="Optional list of image paths")
    parser.add_argument("items", nargs="*", help="Image specs as path, path=Label, or Label=path")
    args = parser.parse_args(argv)

    title = args.title
    if not title:
        title = f"{args.slug} — Concept Candidates (Checkpoint A)" if args.slug else "Concept Candidates (Checkpoint A)"

    raw_specs: list[tuple[str, str]] = []
    if args.images:
        explicit_labels = [lbl.strip() for lbl in args.labels.split(",") if lbl.strip()] if args.labels else []
        for idx, img_p in enumerate(args.images):
            lbl = explicit_labels[idx] if idx < len(explicit_labels) else os.path.splitext(os.path.basename(img_p))[0]
            raw_specs.append((img_p, lbl))
    for raw in args.items or []:
        raw_specs.append(_parse_item_spec(raw))

    if not raw_specs:
        parser.error("Provide at least one image via positional items or --images")

    parsed_items: list[tuple[str, str]] = []
    for p, lbl in raw_specs:
        if args.normalize:
            w, h = normalize_for_meshy(p)
            lbl = f"{lbl} ({w}x{h})"
        parsed_items.append((p, lbl))

    out = make_sheet(args.out, title, parsed_items)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

