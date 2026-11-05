"""Copies of drawings for the engineering council, at most 1,400 px on the long side.

    python shrink.py <file> [<file> ...]

Prints one absolute path per input, in the same order: a scaled copy for an image larger than
1,400 px (written to a new temporary folder, never beside the original), otherwise the original
path (small images, PDFs, anything Pillow cannot open). Without Pillow it prints the originals.

Why: the council reads every image it is given, and image tokens grow with the pixel count. At
1,400 px drawing labels stay legible and five 2,000 px drawings cost 14.8k tokens instead of
22.8k (measured 5 Nov 2026).
"""
import os
import sys
import tempfile
import time

LIMIT = 1400


def main(paths):
    try:
        from PIL import Image
    except ImportError:
        print("Pillow is not installed: giving the council the originals", file=sys.stderr)
        for p in paths:
            print(os.path.abspath(p))
        return
    out = os.path.join(tempfile.gettempdir(), "eng-council", time.strftime("%Y%m%d-%H%M%S"))
    for i, p in enumerate(paths, 1):
        src = os.path.abspath(p)
        try:
            with Image.open(src) as im:
                w, h = im.size
                if max(w, h) <= LIMIT:
                    print(src)
                    continue
                s = LIMIT / max(w, h)
                img = im if im.mode in ("RGB", "RGBA", "L") else im.convert("RGB")
                os.makedirs(out, exist_ok=True)
                dst = os.path.join(out, f"{i:02d}-{os.path.splitext(os.path.basename(src))[0]}.png")
                img.resize((round(w * s), round(h * s)), Image.LANCZOS).save(dst)
                print(dst)
        except Exception:
            print(src)


if __name__ == "__main__":
    main(sys.argv[1:])
