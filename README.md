# jialin-talks

佳臨的公開分享教材網站，部署在 Cloudflare Pages，網址 <https://talks.iterlab.dev>。

**一場分享 = 一個資料夾 = 一個永久網址。網址發出去之後就不再更動。**

---

## 目錄結構

```
jialin-talks/
├── index.html                  總索引頁（新增分享時要手動加一張卡片）
├── sitemap.xml                 給搜尋引擎，新增分享時加一筆
├── robots.txt                  允許全站索引
├── _redirects                  擋掉 /_src/* 不對外
├── ai-coding-2026/
│   └── index.html              ← 部署出去的成品（完整 HTML，含 SEO meta）
└── _src/
    └── ai-coding-2026/
        ├── template.html       ← 改內容只改這裡
        ├── build.py            建置腳本
        └── artifact.html       給 Claude Artifact 用的片段版（非網站用）
```

## 為什麼要有 `_src`

`template.html` 裡的圖片是佔位符（`{{IMG_XXX}}`），`build.py` 會把 Obsidian vault 裡的圖片縮圖、轉 JPEG、編成 base64 塞進 HTML，產出**單一自包含檔案**（離線可開、可直接傳給別人）。

所以：**改內容一律改 `_src/<分享>/template.html`，改完重跑 build。直接改 `<分享>/index.html` 會在下次 build 時被蓋掉。**

## 建置指令

```bash
cd _src/ai-coding-2026
python build.py --site ../../ai-coding-2026/index.html
```

會同時產出兩個檔案：

| 檔案 | 用途 |
|------|------|
| `_src/<分享>/artifact.html` | HTML 片段，發佈到 Claude Artifact 用 |
| `<分享>/index.html` | 完整 HTML 文件（doctype + head + SEO meta），網站用 |

其他參數：

- `--vault <路徑>`：圖片素材所在的 Obsidian vault，預設 `D:/JL_Obsidian_Vault`（也可用環境變數 `JL_VAULT`）

## 新增一場分享

1. `_src/<新分享>/` 放 `template.html` 與 `build.py`（複製既有的改）
2. 改 `build.py` 開頭的 `SITE_URL` / `SITE_TITLE` / `SITE_DESC`、`IMAGES` 圖片清單
3. 跑 build，輸出到 `<新分享>/index.html`
4. `index.html` 加一張卡片、`sitemap.xml` 加一筆
5. commit & push → Cloudflare Pages 自動部署

有 `talks-publish` skill 可以帶著走這個流程。

## Cloudflare Pages 設定（只做一次）

| 項目 | 值 |
|------|-----|
| 連接方式 | Git（GitHub） |
| Build command | 留空 |
| Build output directory | `/`（根目錄） |
| 自訂網域 | `talks.iterlab.dev` |

網域本身已託管在 Cloudflare，加自訂網域時 DNS 會自動設定。
