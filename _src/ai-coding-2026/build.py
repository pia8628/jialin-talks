# -*- coding: utf-8 -*-
"""把 template.html 的圖片佔位符換成 base64 data URI，產出自包含的 index.html。

用法：
  python build.py                  → 產出 artifact.html（HTML 片段，給 Claude Artifact 用）
  python build.py --site <輸出路徑> → 額外產出完整 HTML 文件（含 doctype/head/SEO meta），給自架網站用
  python build.py --vault <路徑>   → 指定 Obsidian vault 位置（圖片素材來源），預設 D:/JL_Obsidian_Vault

改內容時只改 template.html，改完重跑本檔。
圖片會先等比縮到 MAX_W 寬並轉成 JPEG，避免單檔過大。
"""
import base64
import io
import os
import sys

from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))

# 圖片素材仍放在 Obsidian vault，用 --vault 可覆寫
VAULT = os.environ.get("JL_VAULT", r"D:\JL_Obsidian_Vault")

MAX_W = 1500
QUALITY = 85

# --site 模式的網頁 meta（給搜尋引擎與社群分享卡片）
SITE_URL = "https://talks.iterlab.dev/ai-coding-2026/"
SITE_TITLE = "AI 當工程師，我當主管"
SITE_DESC = "一個非工程師，如何把 Vibe Coding 變成可管理、可驗收的開發流程。"
SITE_AUTHOR = "佳臨"

ART = "Z. 結案資料/文章作品集/assets"
JJOY = ART + "/打造家庭娛樂記帳 APP — Vibe Coding 從零到上線的實踐心得"
DAY1 = ART + "/為什麼你的 AI 比較聰明？關鍵不在模型 ｜Google AI Agents 課程 Day 1 筆記"
SHOT = "00. Inbox/assets/AI程式開發讀書會分享"
MINE = "_ai_output/assets"

IMAGES = {
    # 第一部
    "IMG_SPECTRUM":  DAY1 + "/file-20260618215337103.png",
    "IMG_JJOY":      JJOY + "/file-20260510131237850.png",
    "IMG_PLAN":      JJOY + "/file-20260510131237709.png",
    "IMG_ASSET":     DAY1 + "/file-20260618215337097.png",
    "IMG_RPG_STATUS": MINE + "/讀書會-運動RPG狀態總覽.jpg",
    "IMG_RPG_TURN":   MINE + "/讀書會-運動RPG回合抽卡.jpg",
    # 第二部
    "IMG_GRILL7":    MINE + "/讀書會-grill第7題登入時效.jpg",
    "IMG_GRILL9":    MINE + "/讀書會-grill第9題密碼政策.jpg",
    "IMG_CODEX_RUN": MINE + "/讀書會-codex審查過程.jpg",
    "IMG_CODEX_SUM": MINE + "/讀書會-codex審查總結.jpg",
    "IMG_TICKETS":   SHOT + "/file-20260911135140887.png",
    "IMG_HUB_EARLY": SHOT + "/file-20260911135140856.png",
    "IMG_HUB_LATE":  SHOT + "/file-20260911135140817.png",
    "IMG_COMMIT":    SHOT + "/file-20260911135140835.png",
}


def encode(path):
    """縮圖 → JPEG → data URI"""
    img = Image.open(path)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    if img.width > MAX_W:
        h = int(img.height * MAX_W / float(img.width))
        img = img.resize((MAX_W, h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    data = buf.getvalue()
    return "data:image/jpeg;base64,%s" % base64.b64encode(data).decode("ascii"), len(data)


HEAD_TMPL = u"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(desc)s">
<meta name="author" content="%(author)s">
<link rel="canonical" href="%(url)s">
<meta property="og:type" content="article">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(url)s">
<meta property="og:locale" content="zh_TW">
<meta name="twitter:card" content="summary">
</head>
<body>
"""


def wrap_standalone(html):
    """把片段包成完整 HTML 文件（自架網站用）"""
    head = HEAD_TMPL % {"title": SITE_TITLE, "desc": SITE_DESC,
                        "url": SITE_URL, "author": SITE_AUTHOR}
    return head + html + u"\n</body>\n</html>\n"


def main():
    global VAULT
    if "--vault" in sys.argv:
        VAULT = sys.argv[sys.argv.index("--vault") + 1]
    if not os.path.isdir(VAULT):
        sys.stderr.write("找不到 vault：%s（用 --vault <路徑> 指定）\n" % VAULT)
        return 1

    with io.open(os.path.join(BASE, "template.html"), encoding="utf-8") as f:
        html = f.read()

    total = 0
    for key, rel in IMAGES.items():
        path = os.path.join(VAULT, rel.replace("/", os.sep))
        if not os.path.exists(path):
            sys.stderr.write("找不到圖片：%s\n" % path)
            return 1
        token = "{{%s}}" % key
        if token not in html:
            sys.stderr.write("template 裡沒有佔位符：%s\n" % token)
            return 1
        uri, size = encode(path)
        total += size
        html = html.replace(token, uri)

    out = os.path.join(BASE, "artifact.html")
    with io.open(out, "w", encoding="utf-8") as f:
        f.write(html)

    print("已產出 %s" % out)
    print("%d 張圖，壓縮後共 %.1f KB；輸出檔 %.1f KB"
          % (len(IMAGES), total / 1024.0, os.path.getsize(out) / 1024.0))

    # --site <路徑>：額外輸出完整 HTML 文件
    if "--site" in sys.argv:
        i = sys.argv.index("--site")
        if i + 1 >= len(sys.argv):
            sys.stderr.write("--site 後面要接輸出路徑\n")
            return 1
        site_out = sys.argv[i + 1]
        d = os.path.dirname(os.path.abspath(site_out))
        if d and not os.path.isdir(d):
            os.makedirs(d)
        with io.open(site_out, "w", encoding="utf-8") as f:
            f.write(wrap_standalone(html))
        print("已產出網站版 %s（%.1f KB）"
              % (site_out, os.path.getsize(site_out) / 1024.0))

    return 0


if __name__ == "__main__":
    sys.exit(main())
