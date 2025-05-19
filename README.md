# StarBaBa - 個人訂閱管理

StarBaBa 是一個簡單易用的個人訂閱服務管理 Web 應用程式 MVP (最小可行性產品)。它可以幫助您追蹤您的線上訂閱、管理相關花費，並透過有趣的商品換算方式來了解您的支出情況。

## ✨ 功能特性 (MVP)

- **訂閱追蹤**: 記錄您的所有訂閱服務，包括服務名稱、開始日期、價格、付款週期等。
- **花費管理**: 清晰了解您在各項訂閱上的支出。
- **商品換算**: 將您的月度或年度訂閱總支出，換算成等值的日常商品 (例如：相當於多少杯星巴克、多少個大麥克)，讓支出更有感！
- **標籤分類**: 為您的訂閱加上標籤，方便分類與篩選。
- **簡易操作**: 直觀的介面，輕鬆新增、編輯、刪除訂閱項目。
- **設定彈性**: 可自訂預設服務、標籤、貨幣、商品換算項目等。

## 🛠️ 技術棧

- **後端**: Flask (Python), SQLAlchemy (ORM)
- **前端**: HTML, JavaScript, CSS (TailwindCSS)
- **資料庫**: PostgreSQL (主要), JSON 檔案 (遷移前/備份)
- **環境**: Python 3.x, Node.js (用於 TailwindCSS), PostgreSQL

## 🚀 環境設定與啟動

### 1. 前置需求

- Python (建議 3.8 或更高版本)
- Pip (Python 套件安裝器)
- Node.js 和 npm (用於安裝和執行 TailwindCSS)
- PostgreSQL 本地服務 (用於本地開發)

### 2. 取得專案

```bash
git clone <repository_url> # 或者解壓縮您下載的專案檔案
cd StarBaBa
```

### 3. 設定 Python 虛擬環境 (建議)

```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Windows (Command Prompt)
python -m venv .venv
.\.venv\Scripts\activate.bat

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. 安裝 Python 依賴

在已啟動的虛擬環境中執行：
```bash
pip install -r requirements.txt # 將包含 Flask, python-dotenv, psycopg2-binary, Flask-SQLAlchemy/SQLAlchemy 等
```

### 5. 安裝 Node.js 依賴 (用於 TailwindCSS)

```bash
npm install
```

### 6. 設定環境變數

複製 `.env.example` 並重新命名為 `.env`。

然後編輯 `.env` 檔案。您 **必須** 設定 `SECRET_KEY` 和 `DATABASE_URL`。

**`SECRET_KEY`**: 您可以使用 Python 在虛擬環境中生成一個隨機金鑰：
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**`DATABASE_URL`**: 設定您的 PostgreSQL 連接字串。本地開發範例如下 (請根據您的實際設定修改使用者名稱、密碼、主機、埠和資料庫名稱)：
`postgresql://your_db_user:your_db_password@localhost:5432/starbaba_db`

`.env` 檔案內容應類似：

```env
FLASK_APP=run.py
FLASK_ENV=development
# 佈署上線heroku時改成FLASK_ENV=production
SECRET_KEY=您生成的超長隨機安全金鑰
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### 7. 編譯 TailwindCSS

開啟一個新的終端機視窗/分頁，進入專案根目錄，並執行以下指令來即時監看 CSS 檔案的變更並自動編譯：

```bash
npm run tailwind:css
```
此指令會持續執行，監看 `./app/static/css/input.css` 和 `tailwind.config.js` 的變化，並將編譯後的 CSS 輸出到 `./app/static/css/style.css`。

### 8. 啟動 Flask 應用程式

確保您的 Python 虛擬環境已啟動，PostgreSQL 服務正在執行，並且 TailwindCSS 編譯程序 (`npm run tailwind:css`) 正在另一個終端機中執行。

首次執行前，您可能需要初始化資料庫並遷移資料：
1.  **(若使用 Flask-Migrate/Alembic)** 執行資料庫遷移指令 (如 `flask db upgrade`)。
2.  執行資料植入腳本將現有 `data/*.json` 內容匯入 PostgreSQL (例如 `python manage.py seed_db`，如果提供了這樣的腳本)。

**開發模式:**

在虛擬環境啟動的終端機中執行：
```bash
python run.py
```
或者，如果您設定了 `FLASK_APP=run.py`，依然可以使用：
```bash
flask run
```

**使用 Gunicorn (通常用於生產環境模擬或部署):**
```bash
gunicorn run:app
```

應用程式預設會在 `http://127.0.0.1:5000/` (使用 `flask run` 或 `python run.py`) 或 `http://127.0.0.1:8000/` (預設 Gunicorn) 上執行。

## 🗂️ 專案結構 (概覽)

```
StarBaBa/
├── app/                # Flask 應用程式
│   ├── models.py       # SQLAlchemy 資料庫模型
│   ├── static/         # 靜態檔案 (CSS, JS, Images)
│   └── templates/      # HTML 模板
├── data/               # JSON 資料檔案 (遷移後可移除或備份)
├── migrations/         # (可選) Flask-Migrate/Alembic 遷移腳本
├── .env                # 環境變數 (含 DATABASE_URL)
├── Procfile            # Gunicorn/部署設定
├── run.py              # Flask 啟動點
├── requirements.txt    # Python 依賴 (含 DB 相關套件)
├── package.json        # Node.js 依賴 (for Tailwind)
└── tailwind.config.js  # TailwindCSS 設定
└── manage.py           # (可選) 管理腳本
```

## ⚙️ API 端點 (MVP)

- `GET /`: 主頁面。
- `GET /api/settings`: 獲取應用程式設定。
- `GET /api/subscriptions`: 獲取所有訂閱項目。
- `POST /api/subscriptions`: 新增訂閱項目。
- `GET /api/subscriptions/<id>`: 獲取指定 ID 的訂閱項目。
- `PUT /api/subscriptions/<id>`: 更新指定 ID 的訂閱項目。
- `DELETE /api/subscriptions/<id>`: 刪除指定 ID 的訂閱項目。
- `GET /api/stats`: 獲取統計數據 (總月費、年費、商品換算)。

### 測試 API (使用 curl)

以下是使用 `curl` 測試 StarBaBa API 端點的範例指令。請確保您的 Flask 應用程式正在執行。

**1. 獲取應用程式設定**
```bash
curl -X GET http://127.0.0.1:5000/api/settings
```

**2. 新增訂閱項目**
```bash
curl -X POST http://127.0.0.1:5000/api/subscriptions \
-H "Content-Type: application/json" \
-d '{
    "serviceName": "範例服務",
    "price": 9.99,
    "currency": "USD",
    "billingCycle": "monthly",
    "startDate": "2024-01-01",
    "endDate": null,
    "category": "工具",
    "tags": ["生產力", "雲端"],
    "notes": "這是一個測試訂閱。",
    "isActive": true,
    "paymentMethod": "信用卡",
    "accountIdentifier": "test@example.com",
    "url": "http://example.com",
    "autoRenew": true
}'
```
**注意:** 上述 `POST` 指令成功後會回傳新增的訂閱項目，其中包含一個 `id` (通常是 UUID 字串)。請記下這個 `id`，以便在後續的讀取、更新和刪除操作中使用。

**3. 讀取所有訂閱項目**
```bash
curl -X GET http://127.0.0.1:5000/api/subscriptions
```

**4. 讀取單個訂閱項目**

將 `<your_subscription_id>` 替換為您想要讀取的訂閱項目 ID (例如，從新增操作的回應中取得的 ID)。
```bash
curl -X GET http://127.0.0.1:5000/api/subscriptions/<your_subscription_id>
```
範例 (假設 ID 為 `d8f8f8f8-f8f8-f8f8-f8f8-f8f8f8f8f8f8`):
```bash
curl -X GET http://127.0.0.1:5000/api/subscriptions/d8f8f8f8-f8f8-f8f8-f8f8-f8f8f8f8f8f8
```

**5. 更新訂閱項目**

將 `<your_subscription_id>` 替換為您想要更新的訂閱項目 ID。
```bash
curl -X PUT http://127.0.0.1:5000/api/subscriptions/<your_subscription_id> \
-H "Content-Type: application/json" \
-d '{
    "price": 12.99,
    "notes": "價格已更新，並新增備註。"
}'
```
範例 (假設 ID 為 `d8f8f8f8-f8f8-f8f8-f8f8-f8f8f8f8f8f8`):
```bash
curl -X PUT http://127.0.0.1:5000/api/subscriptions/d8f8f8f8-f8f8-f8f8-f8f8-f8f8f8f8f8f8 \
-H "Content-Type: application/json" \
-d '{
    "price": 12.99,
    "notes": "價格已更新，並新增備註。"
}'
```

**6. 刪除訂閱項目**

將 `<your_subscription_id>` 替換為您想要刪除的訂閱項目 ID。
```bash
curl -X DELETE http://127.0.0.1:5000/api/subscriptions/<your_subscription_id>
```
範例 (假設 ID 為 `d8f8f8f8-f8f8-f8f8-f8f8-f8f8f8f8f8f8`):
```bash
curl -X DELETE http://127.0.0.1:5000/api/subscriptions/d8f8f8f8-f8f8-f8f8-f8f8-f8f8f8f8f8f8
```

## 🔮 未來展望

- [完成 - 本地] 資料庫整合 (PostgreSQL 本地環境已設定並運作)。
- [待辦] 資料庫部署 (Heroku PostgreSQL)。
- 使用者認證系統。
- 更進階的統計與圖表報告。
- 匯入/匯出功能。
- 到期提醒通知。
- 貨幣自動轉換。

---

感謝使用 StarBaBa！ 