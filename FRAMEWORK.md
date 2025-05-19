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
    - **ORM**: SQLAlchemy (或 Flask-SQLAlchemy)
    - **WSGI 伺服器**: Gunicorn (用於部署)
- **資料庫**:
    - **主要資料庫**: PostgreSQL
    - **JSON 檔案 (遷移前/備份)**:
        - `data/subscriptions.json`: 儲存使用者訂閱資料。
        - `data/settings.json`: 儲存應用程式設定。
- **Python 套件管理**: `requirements.txt` (新增 `psycopg2-binary`, `SQLAlchemy`/`Flask-SQLAlchemy`)
- **前端套件管理**: `package.json` (主要用於 TailwindCSS)
- **環境變數管理**: `.env` 檔案 (使用 `python-dotenv` 讀取，新增 `DATABASE_URL`)

## 3. 專案結構

```
StarBaBa/
├── .venv/                  # Python 虛擬環境
├── app/                    # Flask 應用程式核心目錄
│   ├── __init__.py         # Flask App Factory, 初始化應用, 資料庫設定
│   ├── routes.py           # 定義 API 端點和頁面路由
│   ├── models.py           # SQLAlchemy 資料庫模型定義及操作邏輯
│   ├── services.py         # 業務邏輯 (例如統計計算)
│   ├── static/             # 靜態檔案 (CSS, JavaScript, Images)
│   │   ├── css/
│   │   │   └── style.css
│   │   │   └── input.css
│   │   ├── js/
│   │   │   └── main.js
│   │   ├── images/
│   └── templates/          # HTML 模板
│       └── index.html
│       └── base.html
│       └── partials/
│           └── _subscription_form.html
│           └── _subscription_item.html
├── data/                   # (遷移後可作為備份或移除)
│   ├── subscriptions.json
│   └── settings.json
├── migrations/             # (可選) 資料庫遷移腳本 (若使用 Flask-Migrate/Alembic)
│   └── versions/
├── .env                    # 環境變數檔案 (FLASK_APP, FLASK_ENV, SECRET_KEY, DATABASE_URL)
├── .env.example            # .env 檔案的範例 (包含 DATABASE_URL 範例)
├── .python-version
├── Procfile
├── tailwind.config.js
├── package.json
├── requirements.txt
├── run.py                  # Flask 應用程式啟動腳本
└── manage.py               # (可選) 應用程式管理腳本 (如執行遷移、自訂命令)
    └── db_init_script.py   # (可選) 將 JSON 資料寫入 PostgreSQL 的初始腳本
```

## 4. 核心組件說明

- **`run.py`**: 作為 Flask 應用程式的進入點，呼叫 `create_app()` 並用於啟動開發伺服器。
- **`app/__init__.py`**: 包含 `create_app` 函式，用於建立和設定 Flask 應用實例。這裡會進行藍圖註冊、設定讀取 (包括資料庫連接設定)、初始化 SQLAlchemy (或 Flask-SQLAlchemy)、日誌設定等。
- **`app/models.py`**: 負責定義 SQLAlchemy 資料庫模型 (例如 `Settings`, `Subscription`) 並包含所有與資料庫互動的邏輯 (CRUD 操作)。取代原先直接讀寫 JSON 檔案的功能。
- **`app/routes.py`**: 定義應用程式的所有 HTTP 路由和 API 端點。它將接收前端請求，呼叫 `models.py` 或 `services.py` 中的相應函式處理請求，並回傳 HTTP 回應。
- **`app/services.py`**: 包含較複雜的業務邏輯，例如 `calculate_statistics` 函式，該函式將從 `models.py` 獲取資料進行計算。
- **`app/static/`**: 存放所有靜態資源。
- **`app/templates/`**: 存放 Jinja2 HTML 模板。
- **`data/`**: 在資料遷移至 PostgreSQL 後，此目錄下的 JSON 檔案主要用於備份或最終被移除。
- **`.env`**: 儲存環境特定的配置，如 Flask 的 `SECRET_KEY` 和 `DATABASE_URL`。此檔案不應提交到版本控制。
- **`migrations/`**: (若使用) 存放由 Flask-Migrate 或 Alembic 管理的資料庫版本控制腳本。
- **`manage.py` / `db_init_script.py`**: (若使用) 用於執行特定任務，如資料庫初始化、資料遷移、啟動應用等。

## 5. 資料模型簡述

在整合 PostgreSQL 後，原先 `settings.json` 和 `subscriptions.json` 的結構將被映射到資料庫中的 `Settings` 和 `Subscription` 表格。欄位將大致保持一致，但會利用資料庫的類型系統和約束。

### `Settings` 表 (原 `settings.json`)
包含應用程式的通用設定，例如：
- `appName`: 應用程式名稱。
- `predefinedServices`: (可能正規化為單獨的表或以 JSON 類型儲存) 預定義的服務列表。
- `availableTags`: (可能正規化為單獨的表或以 JSON 類型儲存) 可用的標籤列表。
- `billingCycles`: 付款週期選項。
- `currencies`: 支援的貨幣列表。
- `paymentMethods`: 支援的付款方式。
- `equivalencyItems`: 用於商品換算的物品及其價格。
- `defaultCurrency`: 預設貨幣。

### `Subscription` 表 (原 `subscriptions.json`)
儲存每個訂閱的詳細資訊，每個訂閱記錄包含：
- `id`: 主鍵，唯一識別碼 (可由資料庫自動生成，如 Serial 或 UUID)。
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

## 6. 安全性考量
- `SECRET_KEY` 和 `DATABASE_URL` (包含資料庫憑證) 必須儲存在 `.env` 檔案中，並且 `.env` 檔案不能提交到版本控制系統。
- 實際部署時，資料庫憑證管理應遵循最佳實踐 (例如使用 Heroku 的 Config Vars)。
- MVP 階段暫不處理 JSON 檔案直接儲存敏感資訊 (如完整信用卡號) 的複雜安全性問題，`paymentDetails` 僅為示意。 