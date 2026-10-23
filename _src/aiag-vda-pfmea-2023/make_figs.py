# -*- coding: utf-8 -*-
"""產生講義用的示意圖（內嵌 SVG），並插入 template.html。
講義原圖多為外部來源（含簡體中文與浮水印），一律依內容重畫成繁中，不使用原圖。
改圖只改本檔，改完依序執行 python make_figs.py、python build.py。可重複執行：以 <!--FIG:xxx--> 區塊取代。"""
import os, re, sys

TPL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.html")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, cls="sv-t", anchor="middle", size=None, weight=None, lh=None):
    """多行文字以 \\n 分隔，y 是第一行的基線"""
    lines = s.split("\n")
    attrs = f'x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"'
    if size:
        attrs += f' font-size="{size}"'
    if weight:
        attrs += f' font-weight="{weight}"'
    if len(lines) == 1:
        return f"<text {attrs}>{esc(s)}</text>"
    lh = lh or (size or 13) * 1.45
    spans = "".join(
        f'<tspan x="{x}" dy="{0 if i == 0 else lh:.1f}">{esc(l)}</tspan>' for i, l in enumerate(lines)
    )
    return f"<text {attrs}>{spans}</text>"


def rect(x, y, w, h, cls="sv-bar", rx=6, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}" {extra}/>'


def line(x1, y1, x2, y2, cls="sv-ln", arrow=False):
    m = ' marker-end="url(#ah)"' if arrow else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}"{m}/>'


def path(d, cls="sv-ln", arrow=False):
    m = ' marker-end="url(#ah)"' if arrow else ""
    return f'<path d="{d}" class="{cls}"{m}/>'


DEFS = ('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="sv-ah"/></marker></defs>')


def wrap(svg_body, w, h, label, caption, minw=600, fid=None):
    idattr = f' id="{fid}"' if fid else ""
    zoom = (f'\n<button class="btn zoom-btn" type="button" data-zoom="{fid}" '
            f'data-zoom-title="{esc(label)}">⛶ 全螢幕檢視</button>') if fid else ""
    return (f'<figure class="fig"{idattr}>\n<div class="fig-scroll"><svg viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{esc(label)}" style="min-width:{minw}px">{DEFS}{svg_body}</svg></div>\n'
            f'<figcaption>{caption}</figcaption>\n</figure>{zoom}')


def ask_arrows(y, x_left, x_mid, x_right, left_lab, right_lab):
    """底部「往左問／往右問」的兩支粗箭頭"""
    b = []
    b.append(f'<path d="M{x_mid - 8},{y - 13} H{x_left + 18} V{y - 22} L{x_left},{y} L{x_left + 18},{y + 22} V{y + 13} H{x_mid - 8} Z" class="sv-ask"/>')
    b.append(f'<path d="M{x_mid + 8},{y - 13} H{x_right - 18} V{y - 22} L{x_right},{y} L{x_right - 18},{y + 22} V{y + 13} H{x_mid + 8} Z" class="sv-ask"/>')
    b.append(text((x_left + x_mid) / 2 + 6, y + 5, left_lab, "sv-askt", size=13.5, weight=700))
    b.append(text((x_mid + x_right) / 2 - 6, y + 5, right_lab, "sv-askt", size=13.5, weight=700))
    return "".join(b)


# ---------- 失效鏈 ----------
def fig_chain():
    W, H = 720, 340
    b = []
    cy, r = 150, 118
    b.append(f'<circle cx="180" cy="{cy}" r="{r}" class="sv-fe"/>')
    b.append(f'<circle cx="540" cy="{cy}" r="{r}" class="sv-fc"/>')
    b.append(f'<circle cx="360" cy="{cy}" r="{r}" class="sv-fm"/>')
    b.append(text(135, 118, "發生了什麼？", "sv-m", size=13))
    b.append(text(135, 148, "失效影響", "sv-fet", size=19, weight=800))
    b.append(text(135, 170, "FE · Failure Effect", "sv-fet", size=11.5))
    b.append(text(360, 148, "失效模式", "sv-fmt", size=19, weight=800))
    b.append(text(360, 170, "FM · Failure Mode", "sv-fmt", size=11.5))
    b.append(text(585, 118, "為什麼？", "sv-m", size=13))
    b.append(text(585, 148, "失效原因", "sv-fct", size=19, weight=800))
    b.append(text(585, 170, "FC · Failure Cause", "sv-fct", size=11.5))
    b.append(line(318, 205, 200, 205, "sv-ln sv-thick", arrow=True))
    b.append(line(402, 205, 520, 205, "sv-ln sv-thick", arrow=True))
    b.append(text(258, 228, "會造成什麼後果？", "sv-m sv-halo", size=12.5))
    b.append(text(462, 228, "為什麼會發生？", "sv-m sv-halo", size=12.5))
    b.append(line(360, 296, 360, 272, "sv-ln sv-thick", arrow=True))
    b.append(rect(255, 296, 210, 34, "sv-focus", rx=8))
    b.append(text(360, 318, "聚焦元素：從失效模式出發", "sv-t", size=13.5, weight=700))
    return wrap("".join(b), W, H, "失效鏈：失效原因、失效模式、失效影響",
                "失效鏈：先鎖定失效模式，再往兩邊問。")


# ---------- FMEA 瀑布圖 ----------
def fig_cascade():
    W, H = 720, 350
    levels = ["產品", "系統", "子系統", "組件", "特性"]
    y0, dy = 70, 58
    cols = [300, 450, 600]
    b = []
    for i, lv in enumerate(levels):
        y = y0 + i * dy
        b.append(rect(20, y - 19, 140, 38, "sv-bar", rx=8))
        b.append(text(36, y + 5, f"0{i + 1}", "sv-num", anchor="start", size=12))
        b.append(text(100, y + 5, lv, "sv-t", size=15, weight=700))
        b.append(line(160, y, 228, y, "sv-ms"))
    kinds = [("FE", "sv-fe", "sv-fet"), ("FM", "sv-fm", "sv-fmt"), ("FC", "sv-fc", "sv-fct")]
    for c, x in enumerate(cols):
        b.append(text(x, 26, f"分析 0{c + 1}", "sv-m", size=12.5, weight=700))
        for k, (lab, cls, tcls) in enumerate(kinds):
            y = y0 + (c + k) * dy
            b.append(rect(x - 46, y - 18, 92, 36, cls, rx=18))
            b.append(text(x, y + 5, lab, tcls, size=15, weight=800))
            if k < 2:
                b.append(line(x, y + 18, x, y + dy - 20, "sv-ln", arrow=True))
    # 跨欄「＝」：上一欄的 FM／FC 就是下一欄的 FE／FM
    for c in range(2):
        for k in range(2):
            y = y0 + (c + 1 + k) * dy
            x1, x2 = cols[c] + 46, cols[c + 1] - 46
            b.append(line(x1 + 4, y, x2 - 4, y, "sv-ms"))
            b.append(text((x1 + x2) / 2, y - 6, "＝", "sv-m", size=13, weight=700))
    return wrap("".join(b), W, H, "FMEA 瀑布圖：上一層分析的失效模式，是下一層分析的失效影響",
                "同一個失效，換一個層級看角色就換了：分析 01 的失效模式，到了分析 02 就是失效影響。DFMEA 與 PFMEA 也是這樣串起來的。")


# ---------- 結構樹 ----------
def fig_structure():
    W, H = 800, 420
    b = []
    for x, lab in [(95, "製程項目"), (330, "製程步驟"), (640, "製程工作要素（4M）")]:
        b.append(text(x, 24, lab, "sv-m", size=13, weight=700))
    iy = 215
    b.append(rect(20, iy - 24, 150, 48, "sv-new", rx=8))
    b.append(text(95, iy + 5, "車窗電機組裝線", "sv-t", size=14, weight=700))
    steps = [(60, "［OP10］潤滑（承重軸）", False), (130, "［OP20］潤滑（齒輪）", False),
             (240, "［OP30］燒結軸承壓入", True), (335, "［OP40］齒輪罩組裝", False), (390, "［OP…］…", False)]
    for y, lab, key in steps:
        b.append(path(f"M170,{iy} H200 V{y} H226", "sv-ln", arrow=True))
        b.append(rect(230, y - 17, 200, 34, "sv-new" if key else "sv-bar", rx=6))
        b.append(text(330, y + 5, lab, "sv-t", size=13.5, weight=700 if key else None))
    elems = {130: ["人（作業員）", "設備（潤滑裝置）", "材料（潤滑油）", "環境（…）"],
             240: ["人（作業員）", "設備（壓入設備）", "環境（…）"]}
    for sy, items in elems.items():
        n = len(items)
        for i, lab in enumerate(items):
            ey = sy + (i - (n - 1) / 2) * 30 + (-12 if sy == 130 else 18)
            b.append(path(f"M430,{sy} H470 V{ey:.0f} H536", "sv-ln", arrow=True))
            b.append(rect(540, ey - 12, 200, 24, "sv-cell", rx=5))
            b.append(text(640, ey + 5, lab, "sv-t", size=12.5))
    return wrap("".join(b), W, H, "結構樹範例：車窗電機組裝線",
                "以車窗電機組裝線為例：製程項目拆成各個製程步驟（OP），每個步驟再依 4M 拆出工作要素。後面的功能分析、失效分析都沿用 OP30 這條線。",
                minw=640, fid="figStructure")


def _tree(title_left, left_lines, mid_title, mid_lines, rights, ask, caption, label, fid, kinds):
    """功能樹／失效樹共用版型：左＝製程項目、中＝製程步驟、右＝工作要素清單"""
    W = 860
    b = []
    rh = [34 + 19 * len(r[1]) for r in rights]
    H = max(320, 40 + sum(rh) + 10 * (len(rights) - 1) + 80)
    mid_y = (40 + H - 80) / 2
    # 左
    lh = 36 + 19 * len(left_lines)
    b.append(rect(14, mid_y - lh / 2, 210, lh, kinds[0], rx=8))
    b.append(text(28, mid_y - lh / 2 + 24, title_left, "sv-t", anchor="start", size=14, weight=700))
    for i, (s, cls) in enumerate(left_lines):
        b.append(text(28, mid_y - lh / 2 + 46 + i * 19, s, cls, anchor="start", size=12.5))
    # 中
    mh = 36 + 19 * len(mid_lines)
    b.append(rect(268, mid_y - mh / 2, 250, mh, kinds[1], rx=8))
    b.append(text(282, mid_y - mh / 2 + 24, mid_title, "sv-t", anchor="start", size=14, weight=700))
    for i, (s, cls) in enumerate(mid_lines):
        b.append(text(282, mid_y - mh / 2 + 46 + i * 19, s, cls, anchor="start", size=12.5))
    b.append(line(224, mid_y, 264, mid_y, "sv-ln", arrow=True))
    b.append(text(393, mid_y - mh / 2 - 12, "▼ 聚焦元素", "sv-num", size=12.5, weight=700))
    # 右
    y = 40
    for (t, ls), h in zip(rights, rh):
        b.append(path(f"M518,{mid_y} H545 V{y + h / 2:.0f} H568", "sv-ln", arrow=True))
        b.append(rect(572, y, 274, h, kinds[2], rx=8))
        b.append(text(586, y + 22, t, "sv-t", anchor="start", size=13, weight=700))
        for i, (s, cls) in enumerate(ls):
            b.append(text(586, y + 42 + i * 19, s, cls, anchor="start", size=12.5))
        y += h + 10
    b.append(ask_arrows(H - 34, 120, 430, 740, ask[0], ask[1]))
    return wrap("".join(b), W, H, label, caption, minw=640, fid=fid)


def fig_function():
    P = "sv-m"
    return _tree(
        "電機組裝線", [("製程要求：", P), ("零件組裝", "sv-t"), ("（在定子殼上組裝傳動軸）", "sv-t")],
        "［OP30］燒結軸承壓入", [("產品特性：", P), ("燒結軸承在定子殼內的軸向位置", "sv-t"), ("（間隙 < 0.3 mm）", "sv-t")],
        [("人（作業員）", [("製程特性：上料完成後，作業員", P), ("按下按鈕啟動壓入", P)]),
         ("人（作業員）", [("製程特性：取出燒結軸承，", P), ("裝到傳動軸頂端", P)]),
         ("設備（壓入設備）", [("製程特性：將燒結軸承對準", P), ("定子殼內的軸承座", P)]),
         ("設備（壓入設備）", [("製程特性：將燒結軸承壓入軸承座，", P), ("直到位置固定", P)])],
        ("它的作用？", "怎麼做到的？"),
        "功能樹範例（OP30）：往左問「它的作用是什麼」，往右問「怎麼做到的」。每一格寫成「動詞＋名詞」。",
        "功能樹範例：OP30 燒結軸承壓入", "figFunction", ("sv-bar", "sv-new", "sv-cell"))


def fig_failure():
    P = "sv-m"
    return _tree(
        "電機組裝線", [("製程要求：", P), ("將傳動軸組入電機殼總成", "sv-t"), ("失效影響 FE：", "sv-fet"), ("傳動軸組裝間隙太小", "sv-fet")],
        "［OP30］燒結軸承壓入", [("產品特性：", P), ("燒結軸承的軸向位置（間隙 < 0.3 mm）", "sv-t"), ("失效模式 FM：", "sv-fmt"), ("壓入時，燒結軸承沒有到達軸向位置", "sv-fmt")],
        [("壓入設備", [("製程特性：將燒結軸承壓入軸承座，", P), ("直到位置固定", P), ("失效原因 FC：", "sv-fct"), ("設備在到達最終位置前停止", "sv-fct")]),
         ("壓入設備", [("（其他失效原因…）", P)]),
         ("人（作業員）", [("（其他失效原因…）", P)])],
        ("發生了什麼？", "為什麼？"),
        "失效分析結構樹範例（OP30）：把功能樹每一格翻成反面，就得到失效影響、失效模式、失效原因。",
        "失效分析結構樹範例：OP30 燒結軸承壓入", "figFailure", ("sv-fe", "sv-fm", "sv-fc"))


# ---------- PC／DC 在製程中的位置 ----------
def fig_pcdc():
    W, H = 840, 340
    b = []
    b.append(rect(150, 18, 290, 262, "sv-frame", rx=4))
    b.append(rect(572, 18, 254, 262, "sv-frame", rx=4))
    b.append(text(295, 266, "工位 n", "sv-m", size=13, weight=700))
    b.append(text(699, 266, "工位 n＋1", "sv-m", size=13, weight=700))
    # PC
    b.append(rect(14, 128, 100, 52, "sv-pc", rx=6))
    b.append(text(64, 149, "PC", "sv-pct", size=13, weight=800))
    b.append(text(64, 168, "製程規劃", "sv-t", size=12.5))
    b.append(line(114, 160, 232, 160, "sv-ln", arrow=True))
    b.append(rect(162, 30, 250, 46, "sv-pc", rx=6))
    b.append(text(174, 50, "PC：作業前的確認與反應", "sv-t", anchor="start", size=12.5, weight=700))
    b.append(text(174, 68, "例：防錯（Poka-Yoke）", "sv-t", anchor="start", size=12.5))
    b.append(text(174, 104, "製程參數", "sv-m", anchor="start", size=12.5))
    for dx in (0, 14, 28):
        b.append(line(232 + dx, 92, 266 + dx, 118, "sv-ln", arrow=True))
    # 製程 B
    b.append(rect(236, 120, 150, 80, "sv-bar", rx=4))
    b.append(text(311, 152, "執行作業", "sv-t", size=13.5))
    b.append(text(311, 176, "製程 B", "sv-t", size=13.5, weight=700))
    b.append('<path d="M402,134 L418,150 L408,152 L424,172 L400,156 L410,154 Z" class="sv-bolt"/>')
    # 製程失效
    b.append(line(456, 10, 456, 300, "sv-fail"))
    b.append(text(456, 330, "製程失效發生", "sv-failt", size=14, weight=800))
    b.append(line(386, 160, 606, 160, "sv-ln", arrow=True))
    # DC 1
    b.append(f'<circle cx="514" cy="160" r="11" class="sv-dc"/>')
    b.append(line(522, 168, 531, 177, "sv-dcl"))
    b.append(text(514, 206, "DC：在製程 B", "sv-dct", size=12.5, weight=700))
    b.append(text(514, 224, "檢出失效", "sv-t", size=12.5))
    # 製程 C
    b.append(rect(610, 120, 120, 80, "sv-bar", rx=4))
    b.append(text(670, 152, "執行作業", "sv-t", size=13.5))
    b.append(text(670, 176, "製程 C", "sv-t", size=13.5, weight=700))
    b.append(line(730, 160, 758, 160, "sv-ln", arrow=True))
    b.append(f'<circle cx="772" cy="160" r="11" class="sv-dc"/>')
    b.append(line(780, 168, 789, 177, "sv-dcl"))
    b.append(text(772, 206, "DC：在製程 C", "sv-dct", size=12.5, weight=700))
    b.append(text(772, 224, "檢出失效", "sv-t", size=12.5))
    # 時間軸
    b.append(line(14, 300, 826, 300, "sv-ln", arrow=True))
    b.append(text(810, 330, "時間", "sv-m", size=12.5))
    return wrap("".join(b), W, H, "PFMEA 中的預防控制與探測控制",
                "預防控制（PC）在失效發生之前起作用：製程規劃、防錯、製程參數。探測控制（DC）在失效發生之後起作用：在本工位或下游工位把失效檢出來。",
                minw=640)


# ---------- 製程理解路線圖 ----------
def fig_roadmap():
    W, H = 720, 290
    b = []
    x0, xm, x1 = 60, 360, 660
    b.append(path(f"M{x0},84 q0,-16 16,-16 H{(x0 + xm) / 2 - 16} q16,0 16,-16 q0,16 16,16 H{xm - 16} q16,0 16,16", "sv-brace-p"))
    b.append(path(f"M{xm},84 q0,-16 16,-16 H{(xm + x1) / 2 - 16} q16,0 16,-16 q0,16 16,16 H{x1 - 16} q16,0 16,16", "sv-brace-d"))
    b.append(text((x0 + xm) / 2, 34, "預防", "sv-pct", size=16, weight=800))
    b.append(text((xm + x1) / 2, 34, "探測", "sv-dct", size=16, weight=800))
    b.append(text((x0 + xm) / 2, 104, "顧好製程品質", "sv-t", size=13.5, weight=700))
    b.append(text((xm + x1) / 2, 104, "攔住產品特性", "sv-t", size=13.5, weight=700))
    b.append(line(30, 122, 700, 122, "sv-ln sv-thick", arrow=True))
    b.append(f'<circle cx="{x0}" cy="122" r="5" class="sv-dot"/>')
    b.append(f'<circle cx="{xm}" cy="122" r="5" class="sv-dot"/>')
    b.append(text(x0, 146, "0", "sv-m", size=12.5))
    b.append(text(xm, 146, "100%", "sv-m", size=12.5, weight=700))
    b.append(text(690, 146, "時間", "sv-m", size=12.5))
    pre = ["作業指導書", "設備能力", "製程監控"]
    det = ["目視檢查", "光學檢查", "各種檢驗"]
    for i in range(3):
        y = 180 + i * 34
        b.append(line(x0, y, xm - 6, y, "sv-ms"))
        b.append(line(xm + 6, y, x1, y, "sv-ms"))
        b.append(rect((x0 + xm) / 2 - 56, y - 13, 112, 26, "sv-pc", rx=13))
        b.append(text((x0 + xm) / 2, y + 5, pre[i], "sv-t", size=13))
        b.append(rect((xm + x1) / 2 - 56, y - 13, 112, 26, "sv-dcbox", rx=13))
        b.append(text((xm + x1) / 2, y + 5, det[i], "sv-t", size=13))
    return wrap("".join(b), W, H, "製程理解路線圖：預防與探測",
                "越往左（預防）越早擋下失效；探測是最後一道防線。最佳化時，優先做能消除失效影響或降低發生率的製程變更，提升探測能力排在最後。",
                minw=560)


FIGS = {
    "chain": fig_chain,
    "cascade": fig_cascade,
    "structure": fig_structure,
    "function": fig_function,
    "failure": fig_failure,
    "pcdc": fig_pcdc,
    "roadmap": fig_roadmap,
}


def main():
    with open(TPL, encoding="utf-8") as f:
        html = f.read()
    for name, fn in FIGS.items():
        pat = re.compile(r"(<!--FIG:%s-->).*?(<!--/FIG:%s-->)" % (name, name), re.S)
        if not pat.search(html):
            sys.stderr.write("template 裡沒有 <!--FIG:%s--> 區塊\n" % name)
            return 1
        html = pat.sub(lambda m: m.group(1) + "\n" + fn() + "\n" + m.group(2), html)
    with open(TPL, "w", encoding="utf-8", newline="") as f:
        f.write(html)
    print("已更新 %d 張圖" % len(FIGS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
