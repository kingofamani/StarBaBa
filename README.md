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

- **後端**: Flask (Python)
- **前端**: HTML, JavaScript, CSS (TailwindCSS)
- **資料庫**: JSON 檔案 (MVP 階段)
- **環境**: Python 3.x, Node.js (用於 TailwindCSS)

## 🚀 環境設定與啟動

### 1. 前置需求

- Python (建議 3.8 或更高版本)
- Pip (Python 套件安裝器)
- Node.js 和 npm (用於安裝和執行 TailwindCSS)

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
pip install -r requirements.txt
```

### 5. 安裝 Node.js 依賴 (用於 TailwindCSS)

```bash
npm install
```

### 6. 設定環境變數

複製 `.env.example` 並重新命名為 `.env`：

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# Windows (Command Prompt)
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

然後編輯 `.env` 檔案。您 **必須** 設定一個 `SECRET_KEY`。您可以使用 Python 在虛擬環境中生成一個隨機金鑰：

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

將生成的金鑰填入 `.env` 的 `SECRET_KEY` 欄位。`.env` 檔案內容應如下：

```env
FLASK_APP=run.py
FLASK_ENV=development
# 佈署上線heroku時改成FLASK_ENV=production
SECRET_KEY=您生成的超長隨機安全金鑰
# 例如: SECRET_KEY=a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0
```

### 7. 編譯 TailwindCSS

開啟一個新的終端機視窗/分頁，進入專案根目錄，並執行以下指令來即時監看 CSS 檔案的變更並自動編譯：

```bash
npm run tailwind:css
```
此指令會持續執行，監看 `./app/static/css/input.css` 和 `tailwind.config.js` 的變化，並將編譯後的 CSS 輸出到 `./app/static/css/style.css`。

### 8. 啟動 Flask 應用程式

確保您的 Python 虛擬環境已啟動，並且 TailwindCSS 編譯程序 (`npm run tailwind:css`) 正在另一個終端機中執行。

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
│   ├── static/         # 靜態檔案 (CSS, JS, Images)
│   └── templates/      # HTML 模板
├── data/               # JSON 資料檔案
├── .env                # 環境變數
├── Procfile            # Gunicorn/部署設定
├── run.py              # Flask 啟動點
├── requirements.txt    # Python 依賴
├── package.json        # Node.js 依賴 (for Tailwind)
└── tailwind.config.js  # TailwindCSS 設定
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

## 🔮 未來展望

- 使用者認證系統。
- 資料庫整合 (例如 SQLite, PostgreSQL)。
- 更進階的統計與圖表報告。
- 匯入/匯出功能。
- 到期提醒通知。
- 貨幣自動轉換。

---

感謝使用 StarBaBa！ 