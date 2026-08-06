from pathlib import Path
from PIL import Image

logo_path = Path(r"D:\Projects\E-Commerce\frontend\public\e-commerce-logo.png")
logo = Image.open(logo_path).convert("RGBA")
print("size", logo.size)
print("corner alpha", logo.getpixel((0, 0))[3], logo.getpixel((logo.width - 1, logo.height - 1))[3])
print("center", logo.getpixel((logo.width // 2, logo.height // 2)))

# Count opaque vs transparent
alpha = logo.getchannel("A")
opaque = sum(1 for p in alpha.getdata() if p > 10)
transparent = sum(1 for p in alpha.getdata() if p <= 10)
print("opaque", opaque, "transparent", transparent)

out_dir = Path(r"D:\Projects\E-Commerce\frontend\public")
for name, color in {
    "preview-white.png": (255, 255, 255, 255),
    "preview-hero.png": (37, 99, 235, 255),
    "preview-dark.png": (16, 24, 40, 255),
}.items():
    canvas = Image.new("RGBA", (640, 640), color)
    x = (canvas.width - logo.width) // 2
    y = (canvas.height - logo.height) // 2
    canvas.alpha_composite(logo, (x, y))
    canvas.convert("RGB").save(out_dir / name)
    print("wrote", name)
