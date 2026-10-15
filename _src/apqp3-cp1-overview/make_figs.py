# -*- coding: utf-8 -*-
"""產生講義用的三張簡化圖（內嵌 SVG），並插入 template.html。
圖的內容依手冊重畫，不使用掃描圖。改圖只改本檔，改完依序執行 python make_figs.py、python build.py。可重複執行：以 <!--FIG:xxx--> 區塊取代。"""
import os, re, sys

TPL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.html")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, cls="sv-t", anchor="middle", size=None, weight=None):
    lines = s.split("\n")
    attrs = f'x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"'
    if size:
        attrs += f' font-size="{size}"'
    if weight:
        attrs += f' font-weight="{weight}"'
    if len(lines) == 1:
        return f"<text {attrs}>{esc(s)}</text>"
    lh = (size or 13) * 1.25
    y0 = -(len(lines) - 1) * lh / 2
    spans = "".join(
        f'<tspan x="{x}" dy="{(y0 if i == 0 else lh):.1f}">{esc(l)}</tspan>' for i, l in enumerate(lines)
    )
    return f"<text {attrs}>{spans}</text>"


def rect(x, y, w, h, cls="sv-bar", rx=6, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}" {extra}/>'


def diamond(cx, cy, n, r=12):
    pts = f"{cx},{cy-r} {cx+r},{cy} {cx},{cy+r} {cx-r},{cy}"
    return (f'<polygon points="{pts}" class="sv-gate"/>'
            + f'<text x="{cx}" y="{cy+4.5}" class="sv-gate-n" text-anchor="middle">{n}</text>')


def wrap(svg_body, w, h, label, caption, minw=600):
    return (f'<figure class="fig">\n<div class="fig-scroll"><svg viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{esc(label)}" style="min-width:{minw}px">{svg_body}</svg></div>\n'
            f'<figcaption>{caption}</figcaption>\n</figure>')


# ---------- 圖 1：APQP 時程圖＋6 個閘門 ----------
def fig_gates():
    W, H = 720, 330
    ms = [(70, "概念啟動\n／核准"), (170, "專案\n核准"), (300, "設計模型\n／原型樣品"), (450, "試產"), (580, "投產")]
    b = []
    top, bottom = 62, 300
    for x, lab in ms:
        b.append(f'<line x1="{x}" y1="{top}" x2="{x}" y2="{bottom}" class="sv-ms"/>')
        b.append(text(x, 22, lab, "sv-m", size=12.5))
    rows = [
        (40, 170, 80, "① 規劃"),
        (170, 450, 114, "② 產品設計與開發"),
        (230, 540, 148, "③ 製程設計與開發"),
        (330, 580, 182, "④ 產品與製程確認"),
    ]
    for x1, x2, y, lab in rows:
        b.append(rect(x1, y, x2 - x1, 26))
        b.append(text(x1 + 10, y + 18, lab, anchor="start"))
    # 量產（箭頭）
    b.append(f'<path d="M580,216 H690 L706,229 L690,242 H580 Z" class="sv-bar"/>')
    b.append(text(590, 234, "⑤ 量產", anchor="start"))
    # 下一案規劃（淡）
    b.append(rect(580, 80, 120, 26, "sv-bar sv-faint"))
    b.append(text(590, 98, "下一案規劃", "sv-m", anchor="start", size=12))
    # 回饋帶
    b.append(rect(40, 258, 666, 26, "sv-bar"))
    b.append(text(60, 276, "回饋、評估與矯正措施（貫穿全程）", anchor="start"))
    # 閘門
    for i, (x, _) in enumerate(ms):
        b.append(diamond(x, 50, i))
    b.append(diamond(650, 271, 5))
    # 圖例
    b.append(diamond(52, 318, "", r=7))
    b.append(text(66, 322, "閘門：主管審查，留下「誰、何時、依據什麼放行」的紀錄", "sv-m", anchor="start", size=12))
    return wrap("".join(b), W, H + 10, "APQP 時程圖與 6 個閘門",
                "APQP 第三版時程圖：五個階段和第二版一樣，新增的是 6 個閘門（G0～G5）。"
                "G0～G4 落在專案里程碑上，G5 在量產後的回饋階段。依手冊附錄 B 重畫、簡化。")


# ---------- 圖 2：安全投產在哪裡 ----------
def fig_safe_launch():
    W, H = 720, 300
    ms = [(150, "設計模型\n／原型樣品"), (360, "試產"), (520, "投產")]
    b = []
    for x, lab in ms:
        b.append(f'<line x1="{x}" y1="44" x2="{x}" y2="208" class="sv-ms"/>')
        b.append(text(x, 20, lab, "sv-m", size=12.5))
    b.append(rect(80, 56, 200, 30))
    b.append(text(180, 76, "原型管制計劃"))
    b.append(rect(280, 96, 240, 30))
    b.append(text(400, 116, "試產管制計劃"))
    b.append(rect(400, 136, 230, 30, "sv-new", extra='stroke-dasharray="6 4"'))
    b.append(text(515, 156, "＋ 安全投產（加強期）", "sv-t", weight="700"))
    b.append(f'<path d="M520,176 H680 L698,191 L680,206 H520 Z" class="sv-bar"/>')
    b.append(text(600, 196, "量產管制計劃"))
    # 說明
    notes = [
        (40, 238, "表單：試產或量產的框，加上「安全投產」框，兩個一起勾"),
        (40, 262, "做法：增加檢驗項目、提高頻率，或用更嚴的規格界限；寫成附件或「特別管制期」"),
        (40, 286, "結束：公司自訂判斷準則＋主管決策；客戶有準則或要授權，就要先達成／取得"),
    ]
    for x, y, s in notes:
        b.append(f'<circle cx="{x+4}" cy="{y-4.5}" r="3.5" class="sv-dot"/>')
        b.append(text(x + 16, y, s, anchor="start", size=13))
    return wrap("".join(b), W, H + 4, "安全投產在時程上的位置",
                "安全投產（虛線）夾在試產和量產之間、跨過投產這條線。它不是第四份獨立的管制計劃，"
                "而是加在試產或量產管制計劃上的加強期。依 CP 手冊第 3 章與表單 B-1 重畫、簡化。")


# ---------- 圖 3：B-1 表單欄位結構 ----------
def fig_form():
    W = 760
    x0 = 20
    b = []
    # 階段勾選
    boxes = [("原型", False), ("試產", False), ("量產", False), ("安全投產", True)]
    x = x0
    for lab, new in boxes:
        b.append(rect(x, 14, 13, 13, "sv-new" if new else "sv-box", rx=2))
        b.append(text(x + 19, 25, lab + ("  新增" if new else ""), "sv-newt" if new else "sv-t", anchor="start", size=13))
        x += 90 if not new else 0
    # 表頭（簡化）
    hy = 40
    head = [
        [("管制計劃編號", 180), ("主要聯絡人／電話", 240), ("日期（初版）", 150), ("日期（修訂）", 150)],
        [("料號／最新變更等級", 420), ("客戶工程核准／日期（如要求）", 300)],
        [("品名／描述", 180), ("組織／工廠核准／日期", 240), ("客戶品質核准／日期（如要求）", 300)],
        [("組織／工廠", 180), ("組織代碼", 240), ("其他核准／日期（如要求）", 300)],
    ]
    for r, row in enumerate(head):
        x = x0
        for lab, w in row:
            b.append(f'<rect x="{x}" y="{hy + r*24}" width="{w}" height="24" class="sv-cell"/>')
            if lab:
                b.append(text(x + 6, hy + r*24 + 16, lab, "sv-m", anchor="start", size=11.5))
            x += w
    # 已刪除：核心小組
    dy = hy + 4*24 + 8
    b.append(f'<rect x="{x0}" y="{dy}" width="150" height="24" rx="4" class="sv-del"/>')
    b.append(text(x0 + 75, dy + 16, "核心小組", "sv-delt", size=12))
    b.append(f'<line x1="{x0+30}" y1="{dy+12}" x2="{x0+120}" y2="{dy+12}" class="sv-strike"/>')
    b.append(text(x0 + 162, dy + 16, "舊版表頭的「核心小組」欄，新版表單已經拿掉", "sv-m", anchor="start", size=12))
    # 明細欄
    cols = [("零件／\n製程\n編號", 40), ("製程名稱\n／作業\n說明", 70), ("機器、\n設備、\n治工具", 60),
            ("編號", 34), ("產品", 50), ("製程", 50), ("特殊\n特性\n分類", 46),
            ("產品／\n製程規格\n／公差", 66), ("評估／\n量測\n技術", 60), ("樣本\n數", 38), ("頻率", 38), ("管制\n方法", 56),
            ("措施", 56), ("負責人", 56)]
    groups = {3: ("特性", 3), 7: ("方法", 5), 12: ("反應計畫", 2)}
    ty = dy + 40
    gh, ch = 26, 58
    x = x0
    i = 0
    while i < len(cols):
        if i in groups:
            g, n = groups[i]
            gw = sum(w for _, w in cols[i:i+n])
            b.append(f'<rect x="{x}" y="{ty}" width="{gw}" height="{gh}" class="sv-cellh"/>')
            b.append(text(x + gw/2, ty + 17, g, size=12.5, weight="700"))
            xx = x
            for j in range(i, i+n):
                lab, w = cols[j]
                new = j == 13
                b.append(f'<rect x="{xx}" y="{ty+gh}" width="{w}" height="{ch}" class="{"sv-new" if new else "sv-cell"}" rx="0"/>')
                b.append(text(xx + w/2, ty + gh + ch/2 + 4, lab, "sv-newt" if new else "sv-t", size=11.5,
                              weight="700" if new else None))
                xx += w
            x = xx
            i += n
        else:
            lab, w = cols[i]
            b.append(f'<rect x="{x}" y="{ty}" width="{w}" height="{gh+ch}" class="sv-cellh"/>')
            b.append(text(x + w/2, ty + (gh+ch)/2 + 4, lab, size=11.5))
            x += w
            i += 1
    # 標註
    ny = ty + gh + ch + 22
    # 特性編號：保留
    kx = x0 + 40 + 70 + 60 + 17
    b.append(f'<path d="M{kx},{ty+gh+ch+2} V{ny-6}" class="sv-lead"/>')
    b.append(text(kx - 10, ny + 8, "特性編號：保留", "sv-m", anchor="start", size=12))
    # 負責人：新增
    rx_ = x0 + 720 - 28
    b.append(f'<path d="M{rx_},{ty+gh+ch+2} V{ny-6}" class="sv-lead sv-lead-new"/>')
    b.append(text(rx_ + 20, ny + 8, "負責人：新增，是反應計畫的負責人，寫職稱", "sv-newt", anchor="end", size=12.5, weight="700"))
    H = ny + 22
    return wrap("".join(b), W, H, "管制計劃表單 B-1 欄位結構",
                "新版管制計劃表單（附錄 B-1）的欄位結構。金色是新增：表頭多了「安全投產」勾選框，"
                "反應計畫分成「措施」和「負責人」兩欄。依 CP 手冊附錄 B-1 重畫、簡化，欄名用講義用語。", minw=640)


CSS = """
/* ---- 手冊重畫配圖 ---- */
.fig{margin:24px 0;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px 16px 12px;box-shadow:var(--shadow)}
.fig-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
.fig svg{display:block;width:100%;height:auto}
.fig figcaption{font-size:14px;line-height:1.7;color:var(--muted);margin-top:10px}
.fig text{font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif}
.sv-t{fill:var(--ink);font-size:13px}
.sv-m{fill:var(--muted);font-size:12.5px}
.sv-bar{fill:var(--surface-2);stroke:var(--line-strong);stroke-width:1}
.sv-faint{opacity:.55}
.sv-ms{stroke:var(--line-strong);stroke-width:1;stroke-dasharray:3 3}
.sv-gate{fill:var(--gold);stroke:var(--gold)}
.sv-gate-n{fill:#0D1B2A;font-size:12px;font-weight:700;font-family:"JetBrains Mono",monospace}
.sv-new{fill:var(--gold-soft);stroke:var(--gold);stroke-width:1.5}
.sv-newt{fill:var(--accent-text)}
.sv-box{fill:none;stroke:var(--line-strong)}
.sv-dot{fill:var(--gold)}
.sv-cell{fill:var(--surface);stroke:var(--line-strong);stroke-width:.8}
.sv-cellh{fill:var(--surface-2);stroke:var(--line-strong);stroke-width:.8}
.sv-del{fill:none;stroke:var(--muted);stroke-dasharray:4 3}
.sv-delt{fill:var(--muted)}
.sv-strike{stroke:var(--muted);stroke-width:1.5}
.sv-lead{stroke:var(--muted);stroke-width:1;fill:none}
.sv-lead-new{stroke:var(--gold)}
"""


def put(s, key, html, anchor, after=True):
    block = f"<!--FIG:{key}-->\n{html}\n<!--/FIG:{key}-->"
    pat = re.compile(rf"<!--FIG:{key}-->.*?<!--/FIG:{key}-->", re.S)
    if pat.search(s):
        return pat.sub(lambda m: block, s)
    assert s.count(anchor) == 1, (key, s.count(anchor))
    return s.replace(anchor, anchor + "\n" + block if after else block + "\n" + anchor)


s = open(TPL, encoding="utf-8").read()
# CSS
pat = re.compile(r"/\* ---- 手冊重畫配圖 ---- \*/.*?\.sv-lead-new\{[^}]*\}\n", re.S)
if pat.search(s):
    s = pat.sub(lambda m: CSS.lstrip("\n"), s)
else:
    i = s.index("</style>")
    s = s[:i] + CSS + s[i:]

# 圖 1：第 06 節，閘門步驟流程之前
s = put(s, "gates", fig_gates(), '<p class="dek">附錄 B：每個關卡由主管審查，過了才能往下走</p>')
# 圖 3：第 09 節第一段之後
s = put(s, "form", fig_form(),
        "AIAG 拆出來的理由是凸顯管制計劃的重要性，也方便以後單獨改版。</p>")
# 圖 2：第 09 節階段流程之後（安全投產卡片之前）
anchor2 = '<div class="step"><div class="step-num">3</div><div class="step-c"><div class="step-t">量產（Production）<span class="b b-same">不變</span></div><div class="step-d">正常量產的管制</div></div></div>\n    </div>\n  </div>'
s = put(s, "safelaunch", fig_safe_launch(), anchor2)
open(TPL, "w", encoding="utf-8").write(s)
print("ok")
