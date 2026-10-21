# 前端升級規劃（2026-10）

範圍：根目錄 `index.html`（總索引頁）＋索引頁上每張講義卡片加 2–3 張圖的輪播。
各場分享的講義內頁（`<分享>/index.html`）這次**不動**，等索引頁定調後再看要不要沿用同一套視覺。

---

## 現況盤點

| 項目 | 現況 | 問題 |
|------|------|------|
| 版面 | 760px 單欄、白底卡片、純文字 | 像部落格文章列表，沒有「教材作品集」的份量感 |
| 卡片 | 標題＋描述＋標籤／日期／長度 | 沒有視覺錨點，兩張卡長得一模一樣，掃讀分不出主題 |
| 設計語言 | 深藍 `#0D1B2A`＋金 `#C9A15A`、Noto Serif TC 標題 | 跟講義內頁同一組色票，**這是資產，要保留** |
| 建置 | 索引頁手寫、沒有 build | 加圖片不能走 base64 內嵌，會讓首頁變肥 |
| 設計脈絡檔 | 沒有 `PRODUCT.md` / `DESIGN.md` | impeccable 沒有依據，要先補 |

## 設計方向（建議）

- **模式：Read＋Experience 混合**：訪客來是為了「找到那場分享、點進去讀」，但首頁同時也是你的作品門面。
- **重新設計（使用者 2026-10-21 決定）**：不必沿用深藍＋金，舊外觀只當參考。要決定的是：講義內頁要不要跟著換（不換會與首頁斷開）。
- 首頁目標是**個人門面**（見 PRODUCT.md）。
- 頁首加一點個人份量：一句定位＋分享場次／主題數之類的小統計（可選）。
- 卡片改成「圖在上（或左）、文字在下（或右）」。**每張卡一樣大**（使用者決定：目前只有 2 場，不做 featured 大卡）。

## 卡片輪播的技術決策

0. **有照片才輪播（使用者規則）**
   - 有 1–3 張 → 卡片顯示圖片（1 張就靜態圖、2–3 張才出現輪播按鈕）
   - 沒照片 → 先問使用者要不要用 Codex 生成封面；不要 → 維持現在的純文字卡
   - 卡片 CSS 兩種都要好看，不能讓純文字卡看起來像「圖片壞掉」
1. **圖片放成獨立檔案，不用 base64**（✅ 腳本已完成）
   - 原圖：使用者直接放 `_src/_index/photos/<分享>/`（1.jpg、2.jpg…依檔名排序，已 gitignore，不經過 Obsidian）
   - 產出：`assets/talks/<分享>/01.webp`～`03.webp`（要進 git）
   - `_src/_index/make_covers.py`：EXIF 轉正 → 置中裁 16:10 → 1200×750 → WebP 品質 80，移除 EXIF（含 GPS）。最後列出沒照片的場次。
2. **輪播用 CSS scroll-snap，不加函式庫**
   - 手機可以原生滑動；桌機加左右按鈕＋圓點，JS 只負責按鈕和圓點同步（< 40 行）。
   - **預設不自動播放**：首頁只有幾張卡，同時在動很吵，也有無障礙問題。若一定要自動播放：滑鼠移上去暫停、`prefers-reduced-motion` 時關掉。
3. **連結結構要改**：現在整張卡是一個 `<a>`，輪播的按鈕不能放在連結裡（巢狀互動元素）。改成 `<article>` 卡片，標題是真正的連結並用 `::after` 撐滿可點範圍，輪播按鈕疊在上層。
4. **防版面跳動**：圖片區固定 `aspect-ratio: 16/10`，`loading="lazy"`、寫 `width/height`，第一張卡的第一張圖不 lazy。
5. **順手的好處**：每場的封面圖可以同時當該場的 `og:image`（社群分享縮圖），目前兩場都沒有。

## 要注意的風險

- **上課照片有學員的臉**：這是公開網站。要嘛取得同意，要嘛挑背影／講台／投影畫面，或做模糊處理。
- `ai-coding-2026/index.html` 已經 2.1 MB（base64 圖片），不在這次範圍，但之後可以考慮改成跟這次一樣的獨立圖檔。

---

## 待辦清單

### 階段 0：impeccable 前置（需要你親自輸入指令，impeccable 設定成只能由使用者呼叫）
- [x] `/impeccable hooks on`：CLI 只寫了 `.impeccable/config.json`，沒裝 Claude Code hook（它只認專案內的 `.claude/skills/impeccable`）。已依內建範本手寫 `.claude/settings.local.json`（PostToolUse Edit|Write＋Stop，指向全域 skill），模擬事件實測可回報。
- [ ] `/impeccable init`：寫 `PRODUCT.md`（誰會來看、你想給人什麼印象）
- [x] ~~`/impeccable document`~~：改為重新設計，不記錄舊系統；新的 DESIGN.md 由 new-work 產出
- [x] `/impeccable init`：PRODUCT.md 完成；buildPath = comp（先出設計稿）

### 階段 1：素材
- [x] 寫 `_src/_index/make_covers.py`（假照片測試通過：直拍轉正、裁切 1200×750、EXIF 清空）
- [x] ai-coding-2026：上課照片＋活動海報＋講義首屏截圖（Playwright 1440×900）→ `assets/talks/ai-coding-2026/01～03.webp`，共約 140 KB
- [x] 腳本補強：直式圖（海報）完整放入＋模糊背景；`FOCUS` 可指定照片裁切焦點
- [ ] apqp3-cp1-overview：還沒上課沒照片 → 問使用者要不要用 Codex 生成，不要就純文字卡
- [ ] 確認照片肖像權

### 階段 1.5：方向決策（2026-10-21 完成）
- [x] 方向：教育訓練活頁夾（seed dbd4aaeb，assigned）；重抽一輪後使用者指定回到活頁夾
- [x] 配色：封面鐵灰 #474C55、品質管理籤 #E2583E、AI 協作籤 #3A6FD8（使用者：先用，之後改版再換 → 顏色集中成 CSS 變數）
- [x] 名稱：IterLab Talks（設計稿上暫寫 IterLab 講義夾，實作照名稱改）
- [x] 構圖：comp-3 上方分頁籤（`.impeccable/mocks/comp-3-top-tabs.webp`，sidecar approved）
- [x] 「邀請我分享」聯絡管道：iterlab8628@gmail.com（mailto）

### 階段 2：設計與實作
- [x] 版面由方向決策＋comp round 決定（取代 shape）
- [x] 改 `index.html`：活頁夾封面＋上方分頁籤（tablist，#slug 可直連）＋照片輪播＋APQP 純文字頁（含講義目錄）＋封底邀約
  - impeccable build-phase：comps ✓ → spec ✓ → plates ✓（照片依使用者原話 force）→ hero 81% ✓ → sections ✓ → motion ✓ → responsive 80% ✓ → review：三輪（fix → fix → ship）✓
  - 首屏照 comp 原文過 gate 後，依使用者決定把名稱改為 IterLab Talks
- [ ] 各場 `build.py` 補 `og:image`
- [ ] 更新 `talks-publish` skill 的「新增一場分享」流程：多一步「有照片 → 放 photos/ 跑腳本；沒照片 → 問要不要 Codex 生成，不要就純文字卡」，卡片範本換新結構（有圖／無圖兩版）
- [ ] 更新 README 目錄結構（加 `assets/`）

- [ ] 首頁 og:image 目前指向 ai-coding-2026/01.webp；各場 build.py 尚未補 og:image
- [ ] 舊 index.html 備份在 session scratchpad（git 也有舊版，可 `git show HEAD:index.html`）

- [x] 審查修正：PP 壓紋紋理與透明插袋改用生成素材、選中分頁籤蓋到內頁上、鍵盤焦點、手機版排版、首屏放人名、封底兩欄、cqw＋1680px 上限
- [x] 素材轉 WebP（2.6MB → 約 340KB），移除未使用的 photo.png
- [x] 1000px／2560px 補驗（無溢出、最小字 12px、2560 時首屏封頂 1680 置中）
- [x] README 補首頁維護說明；.gitignore 排除 .impeccable 中間產物（約 70MB）
- [ ] DESIGN.md＋.impeccable/design.json（documenter 進行中）
- [ ] talks-publish skill 更新新增分享流程（在 ClaudeSetting repo，需使用者同意）

### 階段 3：驗收
- [ ] `/impeccable critique index.html`：設計面評分
- [ ] `/impeccable audit index.html`：無障礙、效能、響應式
- [ ] `/impeccable polish index.html`：上線前最後一輪
- [ ] 桌機＋手機截圖確認、深色模式確認
- [ ] 走 `git-commit` skill 提交，push 前等你點頭
- [x] 文案定稿（2026-10-21）：封面標語「把經驗變成方法，把想法做成工具。」、邀約卡與關於改為使用者提供的文字
- [x] 整體縮小：`.frame` 與封底改為 74vw（960–1280px）置中，頁尾字級等比縮 0.74；1000／1440／1920／390px 實測無溢出
