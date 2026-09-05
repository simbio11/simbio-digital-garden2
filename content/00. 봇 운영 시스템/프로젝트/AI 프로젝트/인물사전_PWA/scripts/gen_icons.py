#!/usr/bin/env python3
"""인물 사전 PWA 아이콘 생성기 - PIL을 사용해 192/512/maskable PNG 생성"""
from PIL import Image, ImageDraw, ImageFilter
import math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "icons")
os.makedirs(OUT, exist_ok=True)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def make_icon(size, maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # 배경: 인디고 -> 바이올렛 그라데이션
    top = (79, 70, 229)     # indigo-600
    bottom = (139, 92, 246) # violet-500
    for y in range(size):
        t = y / size
        d.line([(0, y), (size, y)], fill=lerp(top, bottom, t) + (255,))

    # 모서리 둥글게 (maskable 아니면 전체, maskable이면 safe zone에 여백)
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    radius = int(size * (0.24 if not maskable else 0.28))
    md.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    img.putalpha(mask)

    # 안전 영역 계산 (maskable: 중앙 80%)
    cx, cy = size / 2, size / 2
    if maskable:
        scale = 0.62
    else:
        scale = 0.70
    base = size * scale

    # 사람 실루엣: 머리(원) + 어깨(반원형)
    head_r = base * 0.20
    head_cy = cy - base * 0.16
    shoulders_r = base * 0.42
    shoulders_cy = cy + base * 0.34

    d.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], fill=(255, 255, 255, 255))
    d.pieslice([cx - shoulders_r, shoulders_cy - shoulders_r, cx + shoulders_r, shoulders_cy + shoulders_r],
               start=0, end=180, fill=(255, 255, 255, 255))

    # 이름표 느낌의 작은 흰 점 3개 (주소록 느낌) - 하단
    dot_r = base * 0.035
    dot_y = cy + base * 0.56
    for i, dx in enumerate([-base * 0.16, 0, base * 0.16]):
        d.ellipse([cx + dx - dot_r, dot_y - dot_r, cx + dx + dot_r, dot_y + dot_r], fill=(255, 255, 255, 220))

    return img

for size in (192, 512):
    make_icon(size, maskable=False).save(os.path.join(OUT, f"icon-{size}.png"))
    make_icon(size, maskable=True).save(os.path.join(OUT, f"maskable-{size}.png"))

print("generated:", sorted(os.listdir(OUT)))
