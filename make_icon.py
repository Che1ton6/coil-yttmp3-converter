from PIL import Image, ImageDraw, ImageFont
import os

def draw_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    pad = int(size * 0.04)
    rh = int(size * 0.70)
    ry = (size - rh) // 2
    radius = int(size * 0.18)
    green = (34, 180, 80)
    draw.rounded_rectangle([pad, ry, size - pad, ry + rh], radius=radius, fill=green)

    # Draw music note manually (reliable across all sizes)
    # Note head (filled ellipse, slightly tilted)
    cx = int(size * 0.42)
    cy = int(ry + rh * 0.72)
    hw = int(size * 0.15)  # head width
    hh = int(size * 0.12)  # head height
    draw.ellipse([cx - hw, cy - hh, cx + hw, cy + hh], fill="white")

    # Stem (vertical line up from right side of head)
    sx = cx + hw - int(size * 0.03)
    stem_top = int(ry + rh * 0.28)
    stem_bottom = cy
    sw = max(2, int(size * 0.05))
    draw.rectangle([sx, stem_top, sx + sw, stem_bottom], fill="white")

    # Flag (curved tail from top of stem)
    fx = sx + sw
    fy = stem_top
    fw = int(size * 0.18)
    fh = int(size * 0.22)
    draw.arc([fx, fy, fx + fw, fy + fh], start=270, end=90, fill="white", width=max(2, int(size * 0.05)))

    return img


sizes = [256, 128, 64, 48, 32, 16]
images = [draw_icon(s) for s in sizes]
out = os.path.join(os.path.dirname(__file__), "icon.ico")
images[0].save(out, format="ICO", sizes=[(s, s) for s in sizes], append_images=images[1:])
print(f"Saved: {out}")
