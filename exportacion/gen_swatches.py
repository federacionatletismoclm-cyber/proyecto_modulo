import numpy as np, random, os
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'presentacion_img')
S = 2                     # supermuestreo
W, H = 1632 * S, 520 * S
random.seed(7); np.random.seed(7)

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

# ---------------------------------------------------------------- TARTÁN
img = Image.new('RGB', (W, H), (18, 44, 120))
d = ImageDraw.Draw(img)
blues = [(26, 62, 150), (34, 78, 176), (22, 52, 130), (44, 92, 190), (16, 40, 108)]
for _ in range(95000):
    x, y = random.randint(-6, W + 6), random.randint(-6, H + 6)
    r = random.uniform(3.2, 6.8) * S / 2
    c = random.choice(blues)
    c = lerp(c, (255, 255, 255), random.uniform(0, 0.10))
    d.ellipse([x - r, y - r * 0.85, x + r, y + r * 0.85], fill=c)
    # reflejo del gránulo
    d.ellipse([x - r * 0.35, y - r * 0.55, x + r * 0.05, y - r * 0.2], fill=lerp(c, (255, 255, 255), 0.30))
# resina roja que liga el granulado (motas y vetas)
for _ in range(14000):
    x, y = random.randint(0, W), random.randint(0, H)
    r = random.uniform(1.6, 4.2) * S / 2
    c = random.choice([(206, 52, 46), (226, 78, 58), (178, 38, 38)])
    d.ellipse([x - r, y - r, x + r, y + r], fill=c)
# línea blanca pintada (con la misma textura granulada)
line = Image.new('L', (W, H), 0); ld = ImageDraw.Draw(line)
ld.polygon([(int(W * 0.30), H), (int(W * 0.36), H), (int(W * 0.80), 0), (int(W * 0.74), 0)], fill=255)
line = line.filter(ImageFilter.GaussianBlur(1.2 * S))
white = Image.new('RGB', (W, H), (240, 240, 244)); wd = ImageDraw.Draw(white)
for _ in range(60000):
    x, y = random.randint(0, W), random.randint(0, H); r = random.uniform(1.4, 3.2) * S / 2
    wd.ellipse([x - r, y - r, x + r, y + r], fill=lerp((236, 236, 240), (176, 176, 190), random.uniform(0, 0.8)))
img = Image.composite(white, img, line.point(lambda v: 255 if v > 127 else int(v * 2)))
# luz suave
yy, xx = np.mgrid[0:H, 0:W]
shade = 0.86 + 0.26 * (1 - yy / H) * 0.9 + 0.08 * np.sin(xx / W * 3.1)
arr = np.clip(np.asarray(img).astype(np.float32) * shade[..., None], 0, 255).astype(np.uint8)
Image.fromarray(arr).filter(ImageFilter.GaussianBlur(0.5 * S / 2)).resize((1632, 520), Image.LANCZOS).save(os.path.join(OUT, 'sup_tartan.jpg'), quality=90)

# ------------------------------------------------------------------- PVC
base = np.zeros((H, W, 3), np.float32); base[:] = (44, 142, 92)
noise = np.random.normal(0, 3.2, (H // 3 + 1, W // 3 + 1)).astype(np.float32)
noise = np.asarray(Image.fromarray(noise).resize((W, H), Image.BICUBIC))
base += noise[..., None]
# sutil gofrado del PVC (puntos pequeños y regulares)
dots = ((np.sin(xx / (7.0 * S / 2)) * np.sin(yy / (7.0 * S / 2))) > 0.55).astype(np.float32) * 4.0
base += dots[..., None]
# brillo (reflejo difuso) en diagonal
gl = np.exp(-(((xx - W * (0.20 + 0.65 * yy / H)) / (W * 0.20)) ** 2))
base += gl[..., None] * np.array([26, 30, 28], np.float32)
img2 = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
d2 = ImageDraw.Draw(img2)
# junta entre rollos de PVC
sx = int(W * 0.62)
d2.rectangle([sx, 0, sx + 2 * S, H], fill=(30, 108, 70)); d2.rectangle([sx + 2 * S, 0, sx + 3 * S, H], fill=(86, 176, 128))
# línea blanca de la pista (nítida, con ligero desgaste)
d2.polygon([(0, int(H * 0.60)), (0, int(H * 0.78)), (W, int(H * 0.40)), (W, int(H * 0.22))], fill=(246, 246, 244))
arr2 = np.asarray(img2).astype(np.float32)
arr2 *= (0.92 + 0.12 * (1 - yy / H))[..., None]
Image.fromarray(np.clip(arr2, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.4 * S / 2)).resize((1632, 520), Image.LANCZOS).save(os.path.join(OUT, 'sup_pvc.jpg'), quality=90)
print('ok')
