# -*- coding: utf-8 -*-
"""把索引頁卡片輪播用的原圖轉成網站用的 WebP。

原圖放這裡（不進 git）：
  _src/_index/photos/<分享資料夾>/1.jpg、2.jpg、3.jpg
  依檔名排序決定輪播順序，每場最多 3 張。

產出（要進 git）：
  assets/talks/<分享資料夾>/01.webp、02.webp、03.webp

用法：
  python make_covers.py            → 轉全部
  python make_covers.py <分享資料夾> → 只轉一場

處理：依手機 EXIF 轉正 → 置中裁成 16:10 → 縮到 1200×750 → WebP。
存檔不帶 EXIF，照片裡的 GPS 位置等資訊會一併移除。
"""
import os
import sys

from PIL import Image, ImageFilter, ImageOps

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "photos")
OUT = os.path.join(BASE, "..", "..", "assets", "talks")

SIZE = (1200, 750)  # 16:10
QUALITY = 80
MAX_PER_TALK = 3
EXTS = (".jpg", ".jpeg", ".png", ".webp")

# 裁切焦點（0～1，預設置中）：照片主角不在正中間時指定，避免把頭裁掉
FOCUS = {
    "ai-coding-2026/1-classroom.jpg": (0.5, 0.12),
}


def contain_on_blur(img):
    """直式圖（海報）：完整放進 16:10，兩側補同一張圖的模糊放大版"""
    bg = ImageOps.fit(img, SIZE, Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
    fg = ImageOps.contain(img, SIZE, Image.LANCZOS)
    bg.paste(fg, ((SIZE[0] - fg.width) // 2, (SIZE[1] - fg.height) // 2))
    return bg


def convert(src, dst, key):
    img = ImageOps.exif_transpose(Image.open(src))
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    if img.height > img.width:
        img = contain_on_blur(img)
    else:
        img = ImageOps.fit(img, SIZE, Image.LANCZOS, centering=FOCUS.get(key, (0.5, 0.5)))
    img.save(dst, "WEBP", quality=QUALITY, method=6)
    return os.path.getsize(dst)


def build(slug):
    """轉一場；回傳 False 代表這場沒有原圖（索引頁卡片維持純文字）"""
    folder = os.path.join(SRC, slug)
    files = sorted(f for f in os.listdir(folder) if f.lower().endswith(EXTS)) if os.path.isdir(folder) else []
    if not files:
        return False
    if len(files) > MAX_PER_TALK:
        print(f"[警告] {slug}：有 {len(files)} 張，只取前 {MAX_PER_TALK} 張")
        files = files[:MAX_PER_TALK]

    out_dir = os.path.join(OUT, slug)
    os.makedirs(out_dir, exist_ok=True)
    # 清掉舊產出，避免換圖後殘留多的那張
    for old in os.listdir(out_dir):
        if old.endswith(".webp"):
            os.remove(os.path.join(out_dir, old))

    for i, name in enumerate(files, 1):
        dst = os.path.join(out_dir, f"{i:02d}.webp")
        size = convert(os.path.join(folder, name), dst, f"{slug}/{name}")
        print(f"{slug}/{i:02d}.webp ← {name}（{size / 1024:.0f} KB）")
    return True


def talk_slugs():
    """網站上所有分享 = 根目錄下有 index.html 的資料夾"""
    root = os.path.join(BASE, "..", "..")
    return sorted(
        d for d in os.listdir(root)
        if not d.startswith((".", "_")) and d != "assets"
        and os.path.isfile(os.path.join(root, d, "index.html"))
    )


def main():
    os.makedirs(SRC, exist_ok=True)
    slugs = sys.argv[1:] or talk_slugs()
    missing = [s for s in slugs if not build(s)]
    if missing:
        # 沒照片的場次：問使用者要不要用 Codex 生成，不要就維持純文字卡
        print("\n[沒有照片] " + "、".join(missing))


if __name__ == "__main__":
    main()
