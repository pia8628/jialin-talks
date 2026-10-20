# -*- coding: utf-8 -*-
"""產生第 19 節「課後測驗」HTML，題目與紙本測驗卷（APQP_CP/教材/課後測驗_紙本.html）逐題相同。
改題目時：兩邊一起改。改完依序執行 python make_quiz.py、python build.py。
以 <!--QUIZ--> ... <!--/QUIZ--> 區塊取代，可重複執行。"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(BASE, "template.html")

SEC = {
    1: "哪些手冊改版", 3: "五個階段沒變", 4: "採購與高風險供應商", 5: "變更管理", 8: "透過貿易商接單時",
    9: "安全投產", 10: "反應計畫", 11: "抽樣頻率", 12: "防錯與全檢", 13: "外包製程與傳遞特性",
    14: "家族管制計劃", 15: "管制計劃與 PFMEA 對齊", 17: "CP 找碴",
}

# (題目, 選項, 正解 index, 說明, 回看章節)
MC = [
    ("這次改版後，管制計劃的寫法要看哪一本手冊？",
     ["APQP 第三版的第 6 章", "獨立的管制計劃第一版手冊", "PPAP 手冊", "MSA 手冊"], 1,
     "管制計劃從 APQP 拆出來，獨立成第一版手冊。", [9]),
    ("下列哪一本手冊這次「沒有」改版？",
     ["APQP", "管制計劃", "PPAP", "SPC"], 2,
     "PPAP 仍是第 4 版（2006）；APQP、管制計劃、SPC 都有新版。", [1]),
    ("下列哪一家外包廠屬於「高風險供應商」？",
     ["合作十年、沒有異常、有 IATF 16949 證書的熱處理廠", "剛開始合作、沒有 IATF 16949 證書的電鍍廠",
      "有 ISO 9001 證書、過去三年沒有客訴的包材廠"], 1,
     "新供應商、沒有 ISO 9001／IATF 16949 證書，都是高風險條件。", [4]),
    ("沖床要搬到另一個廠房生產，應該怎麼做？",
     ["機台一樣，直接搬過去生產", "搬完做首件，合格就好，不用通知客戶", "走變更管理：先評估、通知客戶，依客戶要求處理"], 2,
     "生產地點改變屬於變更，要先評估並通知客戶。", [5]),
    ("管制計劃上「反應計畫負責人」應該怎麼寫？",
     ["品保課", "品保課長", "全體人員", "不用寫"], 1,
     "寫單一職稱，不寫部門。新版表單在反應計畫底下新增「負責人」欄。", [10]),
    ("巡檢每 2 小時一次。這次巡檢發現外徑超規，可疑品的範圍是？",
     ["只有這次抽到的 5 件", "上次巡檢合格之後到現在生產的產品", "今天全部的產品都要報廢"], 1,
     "可疑品追溯到上一次合格的檢驗點。所以頻率越低，出事時要遏制的量越大。", [10, 11]),
    ("新料號的「安全投產」什麼時候可以結束？",
     ["量產第二天", "達到事先訂好的退出條件（依客戶要求）", "主管覺得可以就結束"], 1,
     "手冊要求事先訂好結束的判斷準則，並由主管審查決定；客戶有準則或要求授權時，要先達成或取得授權。手冊沒有寫「90 天」。", [9]),
    ("依手冊建議，管制計劃的「頻率」欄最好怎麼寫？",
     ["每小時", "不定期", "每 3,600 沖次", "視需要"], 2,
     "頻率要寫明確的數量或時機；手冊建議用數量為基準，不要用時間，所以「每 3,600 沖次」比「每小時」好。", [11]),
    ("哪些平華司適合放在同一份「家族管制計劃」？",
     ["同材質、同製程，只有尺寸不同", "有的鍍鋅、有的不鍍", "熱處理硬度規格不同"], 0,
     "表面處理或熱處理規格不同，就要分開。", [14]),
    ("PFMEA 修改了一個失效原因的預防控制。管制計劃應該？",
     ["不用動，兩份文件各管各的", "同步檢查並更新對應的管制方法", "等兩年定期審查時再說"], 1,
     "PFMEA 和管制計劃要一起更新。", [15]),
]

# (敘述, 是否正確, 說明, 回看章節)
TF = [
    ("APQP 第三版把五個階段的名稱都改了。", False, "五個階段的名稱和順序都沒變。", [3]),
    ("我們的直接客戶是貿易商，依 IATF 的定義，貿易商也算「汽車顧客」。", True,
     "IATF SI 29：汽車供應鏈中任何採購汽車產品的組織。", [8]),
    ("人工目視全檢就是 100% 檢查，不需要再確認有沒有效。", False, "人工全檢會漏，要定期確效並使用界限樣品。", [12]),
    ("電鍍膜厚只看電鍍廠的報告時，管制計劃要寫出「最後控制點」在哪裡。", True,
     "這是傳遞特性，要寫出最後控制點和我們的確認方式。", [13]),
    ("反應計畫只寫「通知主管」就足夠了。", False, "不能只寫「通知主管」：要連結到特定職位，並寫出遏制步驟、可疑品處置與矯正、重新開始生產的步驟。", [10]),
]

LETTERS = "ABCD"


def back(secs):
    return "　".join(f'<a class="q-back" href="#s{n}">回看 {n:02d} {SEC[n]}</a>' for n in secs)


def build():
    o = []
    o.append('<p class="dek">題目和紙本測驗卷完全相同。寫完紙本後，大家一起看這裡逐題檢討：點選答案會顯示對錯和說明，'
             '說明後面的連結可以跳回講義對應的段落。</p>')
    o.append('<div class="quiz-bar"><button class="btn" id="quizReveal">檢討模式：全部顯示答案</button>'
             '<button class="btn" id="quizReset">清除重來</button></div>')
    o.append('<h3>一、選擇題（每題 7 分，共 70 分）</h3>')
    o.append('<div class="quiz" id="quiz">')
    for i, (t, opts, a, ex, secs) in enumerate(MC, 1):
        o.append(f'    <div class="q" data-a="{a}" data-pt="7">')
        o.append(f'      <div class="q-t"><span class="qn">{i:02d}</span>{t}</div>')
        o.append('      <div class="q-opts">')
        for j, op in enumerate(opts):
            o.append(f'        <button class="q-opt"><span class="q-l">({LETTERS[j]})</span> {op}</button>')
        o.append('      </div>')
        o.append(f'      <div class="q-ex"><b>答案 ({LETTERS[a]})</b>　{ex}<br>{back(secs)}</div>')
        o.append('    </div>')
    o.append('</div>')
    o.append('<h3>二、是非題（每題 6 分，共 30 分）</h3>')
    o.append('<div class="quiz">')
    for i, (t, ok, ex, secs) in enumerate(TF, 1):
        a = 0 if ok else 1
        o.append(f'    <div class="q" data-a="{a}" data-pt="6">')
        o.append(f'      <div class="q-t"><span class="qn">{i:02d}</span>{t}</div>')
        o.append('      <div class="q-opts q-tf">')
        o.append('        <button class="q-opt">○ 對</button>')
        o.append('        <button class="q-opt">× 錯</button>')
        o.append('      </div>')
        o.append(f'      <div class="q-ex"><b>答案 {"○" if ok else "×"}</b>　{ex}<br>{back(secs)}</div>')
        o.append('    </div>')
    o.append('</div>')
    o.append('<div class="score" id="score">'
             '<span>得分：<b id="scoreN">0</b> / 100 分　（已作答 <span id="doneN">0</span> / 15 題）</span>'
             '<span class="score-note">滿分 100，70 分及格。</span></div>')
    return "\n  ".join(o)


s = open(TPL, encoding="utf-8").read()
start = s.index('<section class="sec" id="s19">')
end = s.index("</section>", start)
sec = s[start:end]
head_end = sec.index("</div>", sec.index('class="sec-head"')) + len("</div>")
new_sec = sec[:head_end] + "\n\n  <!--QUIZ-->\n  " + build() + "\n  <!--/QUIZ-->\n"
s = s[:start] + new_sec + s[end:]
open(TPL, "w", encoding="utf-8").write(s)
print("ok")
