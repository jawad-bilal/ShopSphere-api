"""Make the dull solid background of the ShopSphere logo transparent."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL = ROOT / "frontend" / "public" / "e-commerce-logo.original.png"
TARGETS = [
    ROOT / "frontend" / "public" / "e-commerce-logo.png",
    ROOT / "e-commerce-logo.png",
]


def process(src: Path, dest: Path) -> None:
    img = Image.open(src).convert("RGBA")
    pixels = img.load()
    w, h = img.size
    cleared = 0

    for x in range(w):
        for y in range(h):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue

            max_c = max(r, g, b)
            min_c = min(r, g, b)
            chroma = max_c - min_c
            brightness = (r + g + b) / 3

            # Keep vivid logo strokes (teal/blue/violet/red)
            if chroma >= 28:
                # Soften very pale wash around colored edges
                if brightness > 230 and chroma < 45:
                    alpha = max(0, min(255, int((chroma - 10) * 8)))
                    pixels[x, y] = (r, g, b, alpha)
                    if alpha == 0:
                        cleared += 1
                continue

            # Neutral dull/light fill -> transparent
            # Also clear soft gray shadow plate behind the mark
            if brightness >= 170 or (brightness >= 140 and chroma < 18):
                pixels[x, y] = (r, g, b, 0)
                cleared += 1
                continue

            # Mid gray fringe: fade instead of hard cut
            if chroma < 20 and brightness >= 110:
                alpha = max(0, min(255, int((170 - brightness) * 3)))
                pixels[x, y] = (r, g, b, alpha)
                if alpha == 0:
                    cleared += 1

    bbox = img.getbbox()
    if bbox:
        left, top, right, bottom = bbox
        pad = 16
        img = img.crop(
            (
                max(0, left - pad),
                max(0, top - pad),
                min(w, right + pad),
                min(h, bottom + pad),
            )
        )

    max_side = 512
    if max(img.size) > max_side:
        img.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)

    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, format="PNG", optimize=True)
    print(f"wrote {dest} cleared={cleared} size={img.size}")


def main() -> None:
    src = ORIGINAL if ORIGINAL.exists() else TARGETS[0]
    print(f"source={src}")
    for dest in TARGETS:
        process(src, dest)


if __name__ == "__main__":
    main()
