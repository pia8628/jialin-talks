---
name: IterLab Talks
description: 一本永遠不下架的訓練用活頁夾：鐵灰封面、名牌插袋、每場分享一張分頁籤，翻開就是那一場的講義頁。
colors:
  cover: "#474C55"
  cover-ink: "#EBECF3"
  paper: "#FFFFFF"
  ink: "#16181B"
  ink-2: "#4A4F57"
  topic-quality: "#E2583E"
  on-quality: "#16181B"
  topic-ai: "#3A6FD8"
  on-ai: "#FFFFFF"
  marker: "#F7E26B"
  hole: "#1E2024"
  card: "#F8F9FC"
  graphite: "#2E333D"
  dot: "#C3C6CC"
  rule: "#D5D8DC"
  toc-num: "#B8432C"
  cover-muted: "#C5C8D0"
  on-dim: "#FFFFFF"
typography:
  sleeve-title:
    fontFamily: "Noto Sans TC, PingFang TC, Microsoft JhengHei, sans-serif"
    fontSize: "3.45cqw"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.01em"
  sleeve-sub:
    fontFamily: "Noto Sans TC, PingFang TC, Microsoft JhengHei, sans-serif"
    fontSize: "1.9cqw"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.02em"
  display:
    fontFamily: "Noto Sans TC, PingFang TC, Microsoft JhengHei, sans-serif"
    fontSize: "3.19cqw"
    fontWeight: 800
    lineHeight: 1.32
    letterSpacing: "0.01em"
  headline:
    fontFamily: "Noto Sans TC, PingFang TC, Microsoft JhengHei, sans-serif"
    fontSize: "clamp(24px, 2.5vw, 40px)"
    fontWeight: 800
    lineHeight: 1.25
    letterSpacing: "0.02em"
  highlight:
    fontFamily: "Noto Sans TC, PingFang TC, Microsoft JhengHei, sans-serif"
    fontSize: "1.82cqw"
    fontWeight: 600
    lineHeight: 1.5
    letterSpacing: "0.1em"
  lede:
    fontFamily: "Noto Sans TC, PingFang TC, Microsoft JhengHei, sans-serif"
    fontSize: "1.56cqw"
    fontWeight: 500
    lineHeight: 1.46
    letterSpacing: "0.04em"
  body:
    fontFamily: "Noto Sans TC, PingFang TC, Microsoft JhengHei, sans-serif"
    fontSize: "clamp(16px, 1.45vw, 22px)"
    fontWeight: 500
    lineHeight: 1.85
  label:
    fontFamily: "Noto Sans TC, PingFang TC, Microsoft JhengHei, sans-serif"
    fontSize: "1.43cqw"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.04em"
  mono:
    fontFamily: "JetBrains Mono, ui-monospace, monospace"
    fontWeight: 500
    letterSpacing: "0.1em"
    fontFeature: "tnum"
rounded:
  control: "4px"
  tab: "0.9cqw"
  pill: "999px"
  round: "50%"
spacing:
  gutter: "16px"
  frame-max: "1280px"
  back-pad-y: "clamp(48px, 5.2vw, 88px)"
  back-gap: "clamp(32px, 4vw, 72px)"
components:
  button-outline:
    textColor: "{colors.cover-ink}"
    rounded: "{rounded.control}"
    typography: "{typography.label}"
  button-outline-hover:
    backgroundColor: "{colors.cover-ink}"
    textColor: "{colors.cover}"
  tab-quality:
    backgroundColor: "{colors.topic-quality}"
    textColor: "{colors.on-quality}"
    rounded: "{rounded.tab}"
  tab-ai:
    backgroundColor: "{colors.topic-ai}"
    textColor: "{colors.on-ai}"
    rounded: "{rounded.tab}"
  tab-inactive:
    textColor: "{colors.paper}"
  chip-quality:
    backgroundColor: "{colors.topic-quality}"
    textColor: "{colors.on-quality}"
    rounded: "{rounded.pill}"
    typography: "{typography.label}"
  chip-ai:
    backgroundColor: "{colors.topic-ai}"
    textColor: "{colors.on-ai}"
    rounded: "{rounded.pill}"
    typography: "{typography.label}"
  name-sleeve:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
  carousel-nav:
    backgroundColor: "{colors.graphite}"
    textColor: "{colors.paper}"
    rounded: "{rounded.round}"
  carousel-nav-hover:
    backgroundColor: "{colors.ink}"
  button-mail:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.control}"
  button-mail-hover:
    backgroundColor: "{colors.graphite}"
  link-open:
    textColor: "{colors.ink}"
---

# Design System: IterLab Talks

## Overview

**Creative North Star: "永遠不下架的訓練活頁夾"**

整個首頁就是一本攤在桌上的訓練用活頁夾：鐵灰色壓紋 PP 封面（`assets/plates/cover-texture.webp` 平鋪）、左上角一個透明名牌插袋寫著站名、封面下緣立著每場分享一張的彩色分頁籤，選中的那張站到最前面，下面是打了孔的純白內頁，左緣露出金屬活頁環。訪客點一張籤，內頁就「翻」到那一場：真實上課照片、標題、日期與長度、一句用螢光筆劃過的重點，以及「翻開講義 →」。

它刻意拒絕講者網站的預設樣板（大頭照首屏加卡片網格）。可信度來自實物感與真實素材：插袋、活頁環、封面紋理都是素材圖，但字一律由程式排，照片只用真的上課照片。版面密度偏低、字重偏重，像一本正在用的工作講義，不像作品集。

第一屏以 `.frame` 為容器（寬度為螢幕的 74%、最小 960px、最大 1280px、置中，比例 1536:1024），所有位置與字級用 `cqw` 綁在框寬上，所以整本活頁夾在任何桌機寬度都等比縮放；999px 以下改成直式堆疊。

**Key Characteristics:**
- 鐵灰壓紋封面＋純白打孔內頁，兩種材質就是全部的底。
- 每場分享一張分頁籤，顏色只表示主題（品質管理橘、AI 協作開發藍）。
- 每場分享只有一道黃色螢光筆。
- 素材圖負責材質（插袋、活頁環、紋理），文字永遠是活的 HTML。
- 顏色全部集中在 `:root` 自訂屬性，方便日後整套換色。

## Colors

一個中性的鐵灰與白構成整本夾子，兩個主題色只出現在分頁籤與主題標籤上，黃色螢光筆是唯一的強調。

### Primary
- **主題橘・品質管理**（`topic-quality`）：品質管理類分享的分頁籤與主題標籤底色，上面配深色字（`on-quality`）。
- **主題藍・AI 協作開發**（`topic-ai`）：AI 協作開發類分享的分頁籤與主題標籤底色，上面配白字（`on-ai`）。

### Secondary
- **螢光筆黃**（`marker`）：每場分享那一句重點的螢光筆底、`::selection` 反白、所有 `:focus-visible` 外框。

### Neutral
- **鐵灰封面**（`cover`）：`body` 背景色，疊在壓紋素材圖下；封面與封底的底。
- **封面字白**（`cover-ink`）：封面上的標語、外框按鈕、封底文字。
- **內頁白**（`paper`）：打孔內頁。
- **墨黑**（`ink`）：內頁所有主要文字、名牌字、寄信按鈕底、輪播圓點的目前頁。
- **次要墨灰**（`ink-2`）：說明段落、目錄標題等次要文字。
- **打孔黑**（`hole`）：內頁左緣的孔。
- **名牌卡紙**（`card`）：名牌插袋與邀約插袋裡的卡紙，與插袋素材同色。
- **石墨灰**（`graphite`）：輪播左右圓鈕底、寄信按鈕 hover。已收進 `:root`。
- **圓點灰**（`dot`）：輪播未選中的圓點。
- **分隔線灰**（`rule`）：講義目錄的分隔線。
- **目錄編號紅**（`toc-num`）：品質管理色加深，白底上的目錄編號。
- **封面次要字**（`cover-muted`）：封面與封底上的署名、小字。
- **退後籤字色**（`on-dim`）：未選中、變暗的分頁籤一律用白字。

### Named Rules
**換色只改一處規則。** 主題色、封面、內頁、墨色、螢光筆一律以 `:root` 自訂屬性存在（業主決定，日後要整套換皮）；新元件只能引用 `var(--…)`，不新增寫死的色碼。

**主題色只當籤規則。** `topic-*` 只出現在分頁籤與主題標籤（chip）上，不拿來當按鈕、連結或大面積底色。

**退後的籤用白字規則。** 未選中的分頁籤會被壓暗（`brightness(.82) saturate(.9)`），一律改白字：深色字在壓暗的橘上只有 3.29:1，白字是 5.41:1（業主實測後決定）。選中的品質管理籤維持深色字，AI 協作開發籤維持白字。

## Typography

**Display Font:** Noto Sans TC（備援 PingFang TC、Microsoft JhengHei、sans-serif），使用 500 / 600 / 700 / 800
**Body Font:** Noto Sans TC
**Label/Mono Font:** JetBrains Mono 500，搭配 `font-variant-numeric: tabular-nums`

**Character:** 單一中文黑體從 500 用到 800，靠字重與字距分層；等寬字只用來排像表單欄位的資料，讓日期與時間長度讀起來像講義上的編號。

### Hierarchy
- **Sleeve Title**（700，3.45cqw，1.1）：名牌插袋裡的站名「IterLab Talks」。
- **Sleeve Sub**（600，1.9cqw，1.2）：名牌第二行「佳臨｜製造業 × Vibe Coder」，「×」縮小上移、拉丁字放大 1.085em 以對齊中文視覺大小。
- **Display**（800，3.19cqw，1.32）：內頁的分享標題，是整頁最重的字。
- **Headline**（800，clamp(24px, 2.5vw, 40px)，1.25）：封底區塊標題（邀請我分享、關於 IterLab Talks）。
- **Highlight**（600，1.82cqw，1.5，字距 0.1em）：螢光筆那一句。
- **Lede**（500，1.56cqw，1.46，字距 0.04em）：封面上的兩行標語。
- **Body**（500，clamp(16px, 1.45vw, 22px)，1.85）：封底介紹段落，最寬 30em。
- **Label**（600，1.43cqw，字距 0.04em）：主題標籤、外框按鈕（按鈕用 500、字距 0.06em）；分頁籤標題用 500、1.37cqw。
- **Mono**（500，字距 0.1em）：日期與時間長度（`2026-09　約 60 分鐘`）。

### Named Rules
**等寬只排資料規則。** JetBrains Mono 只用在日期、時間長度這類資料欄位，不用在標題或內文。

**第一屏字級跟著框走規則。** 999px 以上，第一屏所有字級用 `cqw`；需要最小可讀值的小字用 `max(12px, …cqw)` 托底。999px 以下改回 px／clamp。

## Layout

第一屏是一個 `.frame`（`width: max(960px,74vw)`、`max-width: 1280px`、置中、`aspect-ratio: 1536/1024`、`container-type: inline-size`），裡面的名牌、標語、按鈕、分頁籤、內頁、照片、標題全部用百分比絕對定位，字級用 `cqw`，整張等比縮放，像一張被精確擺好的照片。上方約 31% 是封面帶，內頁從 31.25% 開始往下佔滿，左緣 2.86% 寬是活頁環素材。

分頁籤沿封面下緣以 flex 自動等分排列（`flex: 1 1 0`，彼此重疊 0.4cqw），新增場次不用重算位置。有照片的分享：輪播在左（約內頁寬 48%）、文字在右；沒照片的分享（`.panel--text`）：文字移到左欄，右欄放講義目錄。

封底（`.back`）回到正常文件流：與 `.frame` 同寬（74vw，960–1280px），兩欄 grid（1.15fr / 1fr），左邊邀約插袋、右邊關於，最下方署名列。

999px 以下整本改直式：名牌、標語、按鈕依序堆疊；分頁籤變成可橫向捲動、捲動吸附的列，每張約半寬；內頁變成一般區塊（左側留 40px 給孔），輪播 16:10；封底變單欄且「關於」排到前面。手機左右間距 16px。

## Elevation & Depth

深度來自實物的層疊，不是 UI 陰影系統：封面在最底、分頁籤插在封面與內頁之間、選中的籤站到最前（`z-index: 3`）並接上內頁，內頁蓋過未選中的籤底部。陰影都是柔和的接觸陰影，模擬紙張與塑膠的厚度。

### Shadow Vocabulary
- **內頁接觸陰影**（`box-shadow: 0 -.25cqw .7cqw rgba(0,0,0,.28), -.25cqw .35cqw .9cqw rgba(0,0,0,.18)`）：白色內頁壓在封面上；手機版簡化為 `0 2px 8px rgba(0,0,0,.2)`。
- **插袋落影**（`filter: drop-shadow(0 .1cqw .15cqw rgba(0,0,0,.35))`）：名牌插袋與邀約插袋貼在封面上。
- **分頁籤厚度**（`box-shadow: inset 0 .12cqw 0 rgba(255,255,255,.28), inset 0 -.5cqw .6cqw -.3cqw rgba(0,0,0,.22)`）：籤上緣的反光與下緣的暗部；選中時只留上緣反光。

### Named Rules
**選中的籤站到前面規則。** 選中與否用前後層次與明暗表達：未選中的籤下沉 0.7cqw 並壓暗，選中的籤歸位、全亮、蓋在其他籤前面。不用底線或外框表示選中。

## Shapes

形狀語言來自文具：分頁籤是上方圓角（0.9cqw）、經 `perspective` + `rotateX(20deg)` 透視成梯形的塑膠籤；主題標籤是全圓角膠囊；按鈕是 4px 小圓角的直角矩形；輪播鈕是正圓；打孔是用 `radial-gradient` 畫的圓點。內頁、照片都是直角。插袋外框用 `border-image` 九宮格拉伸素材圖，中間填 `card` 底色。

## Components

### Buttons
- **Shape:** 微圓角矩形（4px）。
- **外框按鈕（封面）：** 2px `cover-ink` 外框、`cover-ink` 字、透明底；hover 時反白成 `cover-ink` 底、`cover` 字，0.2s 過場。用於「追蹤方格子」「邀請我分享」。
- **寄信按鈕（封底）：** `ink` 實心底、白字、600 字重，信箱地址以等寬字排；hover 變 `graphite`。
- **Focus：** 全站 3px `marker` 外框、外推 3px。

### Chips
- **Style:** 全圓角膠囊，主題色底配對應的 `on-*` 字色，600 字重。
- **State:** 只是主題標示；封底的主題標籤是連結，hover 時 `brightness(1.08)`。

### Navigation（分頁籤）
- **Style:** 每場分享一張籤，顏色依主題，第一行是「主題｜標題」（500、過長以刪節號截斷），第二行是等寬的日期與時間長度。
- **States:** 未選中：下沉、壓暗、白字；hover：上浮 0.25cqw；選中：歸位、全亮、站到最前。過場 0.25s `cubic-bezier(.2,.8,.2,1)`。
- **行為:** `role="tablist"`，左右鍵切換，網址 `#slug` 直接翻到那一場；點籤時內頁播放一次由上往下展開的翻頁（0.42s），螢光筆再從左劃過（0.55s，延遲 0.28s）。
- **Mobile:** 橫向捲動列，捲動吸附，每張約半寬，標題最多兩行。

### 名牌插袋（Signature）
透明塑膠插袋素材（`label-holder.webp`，有鉚釘；封底用無鉚釘的 `label-holder-plain.webp`）以 `border-image` 拉伸，裡面是 `card` 卡紙與程式排的字。站名與身分永遠放在插袋裡。

### 螢光筆重點（Signature）
每場分享一句，`<mark>` 底下是一道略微傾斜（176deg）的 `marker` 色線性漸層，跨行時用 `box-decoration-break: clone`。

### 照片輪播
左右深色圓鈕（`graphite`，hover 變 `ink`）、下方圓點（目前頁 `ink`）。不自動播放，滑動、按鈕、圓點三種操作同步；只有一張照片時自動拿掉按鈕與圓點。

### 翻開講義連結
700 字重、字距 0.11em，文字加 `ink` 粗底線，後接一支 SVG 箭頭，hover 時箭頭右移 0.5cqw。這是每場分享的主要行動。

### 講義目錄（無照片的分享）
上方 3px `ink` 粗線起頭，標題「講義目錄」，每列一個等寬的章節編號加章節名，列間 1px 淺灰分隔線。

## Do's and Don'ts

### Do:
- **Do** 新增場次時只加一張分頁籤與一個 panel，讓 flex 自動排籤位置。
- **Do** 沒有照片的分享用純文字版面（`.panel--text`），右欄放該講義真實的目錄。
- **Do** 每場分享只放一句螢光筆重點，而且必須是講義裡真的那句話。
- **Do** 所有顏色經由 `:root` 自訂屬性引用，主題籤依主題選 `--topic-*` 與 `--on-*` 成對使用。
- **Do** 第一屏的新元素用百分比定位、`cqw` 字級，放在 `.frame`（74vw，960–1280px）裡；999px 以下另寫直式規則。
- **Do** 所有動態包在 `prefers-reduced-motion: reduce` 底下可關閉，輪播不自動播放。

### Don't:
- **Don't** 用大頭照首屏加卡片網格的講者網站樣板。
- **Don't** 做精選大卡或讓某一場分享比其他場大；每張籤一樣寬。
- **Don't** 拿示意照片冒充上課現場；沒有真實照片時預設維持純文字（要不要生成封面，先問業主）。
- **Don't** 把站名、標題等文字烙進素材圖；素材只負責材質。
- **Don't** 在未選中（壓暗）的分頁籤上用深色字。
- **Don't** 把主題色用在按鈕、連結或大面積底色上。
