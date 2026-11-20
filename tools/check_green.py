"""Meet het percentage zichtbare groene pixels in iedere beeldvariant."""
import argparse
from pathlib import Path
import numpy as np
from PIL import Image


def green_percentage(path):
    with Image.open(path) as image:
        rgba = np.asarray(image.convert("RGBA"))
    rgb = rgba[:, :, :3].astype(np.float32) / 255
    r, g, b = rgb.transpose(2, 0, 1)
    high = rgb.max(2)
    delta = high - rgb.min(2)
    # In the requested interval green is the largest channel.
    hue = 120 + 60 * (b - r) / np.maximum(delta, 1e-8)
    visible = rgba[:, :, 3] > 0
    green = ((g == high) & (hue >= 70) & (hue <= 170)
             & (delta > 0.18 * high) & (high > 0.15))
    return 100 * np.count_nonzero(green & visible) / max(1, visible.sum())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("map", type=Path, nargs="?",
                        default=Path(__file__).resolve().parents[1] / "images")
    args = parser.parse_args()
    failed = False
    paths = sorted(p for p in args.map.iterdir() if p.suffix.lower() in {".jpg", ".webp", ".avif"})
    if not paths:
        parser.error("Geen afbeeldingen gevonden")
    for path in paths:
        percentage = green_percentage(path)
        print(f"{path.name}\t{percentage:.4f}%")
        failed |= percentage >= 0.5
    raise SystemExit(int(failed))
