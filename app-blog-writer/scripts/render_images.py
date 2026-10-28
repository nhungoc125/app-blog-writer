#!/usr/bin/env python3
"""Render SVG images to WebP and/or PNG and report sizes.

Usage:
    python render_images.py <svg-file-or-directory> [--webp] [--png] [--scale 1.0]
                            [--quality 88] [--max-kb 200] [--out <dir>]

Defaults to --webp when neither format flag is given. Output files are written next
to each SVG (or into --out). Files over --max-kb are flagged so you can simplify or
lower quality. Requires: pip install cairosvg Pillow
"""
import argparse
import io
import sys
from pathlib import Path

try:
    import cairosvg
    from PIL import Image
except ImportError:
    print("Missing dependencies. Run: pip install cairosvg Pillow  (add --break-system-packages if needed)")
    sys.exit(1)


def render(svg: Path, out_dir: Path, fmt_webp: bool, fmt_png: bool, scale: float, quality: int, max_kb: int):
    png_bytes = cairosvg.svg2png(url=str(svg), scale=scale)
    img = Image.open(io.BytesIO(png_bytes))
    results = []
    if fmt_png:
        p = out_dir / (svg.stem + ".png")
        img.save(p, "PNG", optimize=True)
        results.append(p)
    if fmt_webp:
        p = out_dir / (svg.stem + ".webp")
        img.convert("RGB").save(p, "WEBP", quality=quality, method=6)
        results.append(p)
    for p in results:
        kb = p.stat().st_size / 1024
        flag = "  <-- over limit" if kb > max_kb else ""
        print(f"{p.name}: {img.width}x{img.height}, {kb:.0f} KB{flag}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--webp", action="store_true")
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--quality", type=int, default=88)
    ap.add_argument("--max-kb", type=int, default=200)
    ap.add_argument("--out")
    a = ap.parse_args()
    if not a.webp and not a.png:
        a.webp = True
    src = Path(a.path)
    svgs = [src] if src.is_file() else sorted(src.glob("*.svg"))
    if not svgs:
        print(f"No SVG files found at {src}")
        sys.exit(1)
    for svg in svgs:
        out_dir = Path(a.out) if a.out else svg.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        try:
            render(svg, out_dir, a.webp, a.png, a.scale, a.quality, a.max_kb)
        except Exception as e:  # keep going on one bad file
            print(f"{svg.name}: FAILED ({e})")


if __name__ == "__main__":
    main()
