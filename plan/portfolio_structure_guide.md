# 個人作品集網站專案：資料夾結構管理指南

本文件專門針對您的個人作品集網站，定義了一套標準且具備高擴充性的專案目錄結構（特別適用於 React / Next.js / Vue.js / Astro 等現代前端開發環境），確保程式碼易於維護與擴充。

---

## 1. 專案目錄結構圖 (Project Directory Tree)

```text
my-portfolio/
├── .github/                  # GitHub 自動化部署與工作流設定 (CI/CD)
│   └── workflows/
│       └── deploy.yml        # 自動化部署腳本 (如部署至 Vercel/GitHub Pages)
├── public/                   # 靜態資源目錄 (不會被編譯的原始檔案，直接對應網站根路徑)
│   ├── favicon.ico           # 網站瀏覽器標籤頁圖標
│   ├── robots.txt            # SEO 搜尋引擎爬蟲指令檔案
│   └── resume.pdf            # 提供給 HR/招募人員一鍵下載的個人最新履歷
├── src/                      # 網站核心原始碼目錄
│   ├── assets/               # 需經過 Webpack/Vite 打包與壓縮的最佳化資源
│   │   ├── images/           # 通用圖片資源 (如個人形象照、背景圖、Icons)
│   │   └── projects/         # 作品集專用截圖 (強烈建議轉換為高效能的 .webp 格式)
│   ├── components/           # 跨頁面、可重複使用的原子級 UI 元件
│   │   ├── Footer.jsx        # 全站通用頁尾區塊
│   │   ├── Navbar.jsx        # 頂部導覽列 (整合響應式 RWD 手機版選單)
│   │   ├── ThemeToggle.jsx   # 深色 / 淺色模式 (Dark Mode) 切換按鈕
│   │   └── UI/               # 基礎通用元件庫
│   │       ├── Button.jsx    # 自訂按鈕元件
│   │       ├── Card.jsx      # 作品或卡片專用外框元件
│   │       └── Input.jsx     # 表單輸入欄位元件
│   ├── content/              # 網站內容文本檔案 (落實資料與網頁邏輯分離)
│   │   └── projects/         # 各個精選作品的詳細 Case Study 文本 (以 Markdown 撰寫)
│   │       ├── project-1.md  # 專案 A 的詳細開發背景與量化成果
│   │       └── project-2.md  # 專案 B 的詳細開發背景與量化成果
│   ├── sections/             # 首頁單頁式（Single Page）的核心區塊元件
│   │   ├── Hero.jsx          # [區塊 1] 英雄總覽區 (第一印象強烈主標題與 CTA 按鈕)
│   │   ├── About.jsx         # [區塊 2] 關於我 (個人簡介、熱情所在與核心優勢)
│   │   ├── Skills.jsx        # [區塊 3] 核心技能區 (技術棧、專業領域工具分類呈現)
│   │   ├── Projects.jsx      # [區塊 4] 精選作品卡片網格 (撈取資料並呈現卡片)
│   │   ├── Experience.jsx    # [區塊 5] 工作經歷與學歷時間軸 (倒敘式 Timeline)
│   │   └── Contact.jsx       # [區塊 6] 聯絡我 (聯絡表單與社群 icon 連結整合)
│   ├── styles/               # 樣式表管理目錄
│   │   └── global.css        # 全域樣式設定與 Tailwind CSS 基礎注入
│   ├── App.jsx               # 主應用程式進入點 (負責首頁單頁區塊的依序渲染邏輯)
│   └── main.jsx              # 框架渲染進入點 (ReactDOM 綁定)
├── .gitignore                # 排除不需要、或帶有敏感資訊不需上傳至 GitHub 的檔案
├── package.json              # 專案專屬依賴套件、版本資訊與 scripts 指令設定
├── README.md                 # 本地端專案的基礎啟動與開發說明文件
└── tailwind.config.js        # Tailwind CSS 視覺風格、自訂顏色計畫與字體設定檔
```

---

## 2. 核心架構設計亮點與維護規範

### 📌 規範一：將 `src/sections/` 與 `src/components/` 嚴格抽離

- **首頁大區塊 (`sections/`)**：專門存放您首頁上「由上而下滾動」的各大核心內容。這能讓您的 `App.jsx` 保持極度乾淨與高可讀性，只需依序引入 `<Hero />`, `<About />` 等元件。
- **通用元件 (`components/`)**：存放可在各處隨插即用的微小元件（如自訂按鈕、導覽列）。未來若網站要擴充獨立頁面，這些元件都能無縫複用。

### 📌 規範二：落實資料分離的內容管理 (`src/content/projects/`)

- 為了避免未來每新增一項作品就要重新修改前端 HTML/React 原始碼，此架構採用**資料分離設計**。
- 每當您完成一個新專案，**只需在 `src/content/projects/` 資料夾下新增一個 `.md` 檔案**。前端程式碼會自動解析該目錄並渲染出對應的作品卡片與獨立 Case Study 內頁，大幅降低工程維護成本。

### 📌 規範三：為 HR 特設的快捷靜態資源 (`public/resume.pdf`)

- 在 `public/` 目錄下放置您的最新履歷檔案。在網站的導覽列或 Hero 區設計一個「下載 PDF 履歷」的按鈕，直接將連結指向 `/resume.pdf`，方便招募人員與獵頭快速獲取您的實體履歷，提升轉化率。
