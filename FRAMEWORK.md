# StarBaBa MVP - 專案框架

## 1. 專案目標

StarBaBa 是一個個人訂閱管理 Web 應用程式的最小可行性產品 (MVP)。目標是提供一個簡單易用的工具，讓使用者可以：
- 追蹤個人訂閱的服務。
- 管理訂閱相關的支出。
- 透過將花費換算成等值商品（例如：一杯咖啡、一個大麥克漢堡）來更直觀地了解支出情況。

## 2. 技術棧

- **開發環境**: Windows 11 64bit (使用者指定，但專案應具備跨平台兼容性)
- **前端**: HTML, JavaScript, CSS
    - **CSS 框架**: TailwindCSS
- **後端**: Python
    - **Web 框架**: Flask
- **資料庫 (MVP)**: JSON 檔案
    - `data/subscriptions.json`: 儲存使用者訂閱資料。
    - `data/settings.json`: 儲存應用程式設定 (如預設服務、標籤、貨幣、商品換算項目等)。
- **Python 套件管理**: `requirements.txt`
- **前端套件管理**: `package.json` (主要用於 TailwindCSS)
- **環境變數管理**: `.env` 檔案 (使用 `python-dotenv` 讀取)

## 3. 專案結構

```
StarBaBa/
├── .venv/                  # Python 虛擬環境
├── app/                    # Flask 應用程式核心目錄
│   ├── __init__.py         # Flask App Factory, 初始化應用
│   ├── routes.py           # 定義 API 端點和頁面路由
│   ├── models.py           # 資料處理邏輯 (讀寫 JSON 檔案)
│   ├── services.py         # 業務邏輯 (例如統計計算)
│   ├── static/             # 靜態檔案 (CSS, JavaScript, Images)
│   │   ├── css/
│   │   │   └── style.css   # TailwindCSS 編譯後的 CSS
│   │   │   └── input.css   # TailwindCSS 原始指令輸入檔
│   │   ├── js/
│   │   │   └── main.js     # 前端主要 JavaScript 邏輯
│   │   ├── images/         # 服務圖示等圖片資源 (MVP 初期可空)
│   └── templates/          # HTML 模板
│       └── index.html      # 主頁面
│       └── base.html       # (可選) 基礎佈局模板
│       └── partials/       # HTML 片段模板
│           └── _subscription_form.html # 新增/編輯訂閱表單
│           └── _subscription_item.html # 單個訂閱項目顯示
├── data/                   # 資料檔案目錄
│   ├── subscriptions.json  # 訂閱資料
│   └── settings.json       # 應用程式設定
├── .env                    # 環境變數檔案 (FLASK_APP, FLASK_ENV, SECRET_KEY)
├── .env.example            # .env 檔案的範例
├── tailwind.config.js    # TailwindCSS 設定檔
├── package.json          # Node.js 依賴管理 (用於 TailwindCSS)
├── requirements.txt      # Python 依賴管理
└── app.py                # Flask 應用程式啟動腳本 (包含 create_app() 的呼叫)
```

## 4. 核心組件說明

- **`app.py`**: 作為 Flask 應用程式的進入點，呼叫 `create_app()` 並用於啟動開發伺服器。
- **`app/__init__.py`**: 包含 `create_app` 函式，用於建立和設定 Flask 應用實例。這裡會進行藍圖註冊、設定讀取等初始化工作。
- **`app/models.py`**: 負責所有與資料存取相關的邏輯。在 MVP 階段，這包括讀取和寫入 `subscriptions.json` 和 `settings.json` 檔案的函式。它將處理資料的增、刪、改、查操作，並管理如 `id`、`createdAt`、`updatedAt` 等欄位的自動生成與更新。
- **`app/routes.py`**: 定義應用程式的所有 HTTP 路由和 API 端點。它將接收前端請求，呼叫 `models.py` 或 `services.py` 中的相應函式處理請求，並回傳 HTTP 回應 (渲染 HTML 模板或 JSON 資料)。
- **`app/services.py`**: 包含較複雜的業務邏輯，例如 `calculate_statistics` 函式，用於計算訂閱總支出並進行商品換算。MVP 初期此檔案的邏輯已整合入 `routes.py` 中簡化實現。
- **`app/static/`**: 存放所有靜態資源。`css/style.css` 是由 TailwindCSS 編譯生成的最終樣式表，`css/input.css` 是 TailwindCSS 的原始指令輸入檔案。`js/main.js` 包含前端主要的互動邏輯。
- **`app/templates/`**: 存放 Jinja2 HTML 模板。`index.html` 是應用程式的主頁面。`partials/` 目錄下的模板用於可重用的 UI 組件，如訂閱表單和訂閱項目顯示卡片。
- **`data/`**: 存放應用程式的資料。`subscriptions.json` 以 JSON 陣列形式儲存所有訂閱紀錄。`settings.json` 以 JSON 物件形式儲存應用程式的配置資訊。
- **`.env`**: 儲存環境特定的配置，如 Flask 的 `SECRET_KEY`。此檔案不應提交到版本控制。
- **`tailwind.config.js` 和 `package.json`**: 用於設定和管理 TailwindCSS。
- **`requirements.txt`**: 列出專案所需的 Python 套件。

## 5. 資料模型簡述

### `settings.json`
包含應用程式的通用設定，例如：
- `appName`: 應用程式名稱。
- `predefinedServices`: 預定義的服務列表，方便使用者快速選擇。
- `availableTags`: 可用的標籤列表。
- `billingCycles`: 付款週期選項。
- `currencies`: 支援的貨幣列表。
- `paymentMethods`: 支援的付款方式。
- `equivalencyItems`: 用於商品換算的物品及其價格。
- `defaultCurrency`: 預設貨幣。

### `subscriptions.json`
以 JSON 陣列儲存每個訂閱的詳細資訊，每個訂閱物件包含：
- `id`: 唯一識別碼 (UUID)。
- `serviceName`: 服務名稱。
- `serviceIcon`: 服務圖示路徑。
- `tags`: 標籤陣列。
- `startDate`: 開始日期。
- `billingCycle`: 付款週期。
- `billingDetails`: 付款週期相關細節 (如月繳的日期)。
- `price`: 價格。
- `currency`: 貨幣。
- `notes`: 備註。
- `paymentMethod`: 付款方式。
- `paymentDetails`: 付款方式相關細節。
- `isActive`: 是否啟用。
- `createdAt`, `updatedAt`: 記錄的建立與更新時間戳。

## 6. 安全性考量 (MVP 初期)
- `SECRET_KEY` 將用於 Flask session 管理等。MVP 階段會在 `.env` 中設定，但實際部署時需有更安全的管理方式。
- MVP 階段暫不處理 JSON 檔案直接儲存敏感資訊 (如完整信用卡號) 的複雜安全性問題，`paymentDetails` 僅為示意。 