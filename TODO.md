# StarBaBa MVP - 待辦事項

## 專案初始化
- [x] 建立符合描述的完整專案目錄結構。
- [x] 初始化 Git 版本控制。 (假設使用者已自行處理)

## 環境設定
- [x] 建立 `requirements.txt` 並包含 `Flask` 和 `python-dotenv`。
- [x] 建立 `package.json` 包含 `tailwindcss` 依賴及 `tailwind:css` 指令。
- [x] 建立 `tailwind.config.js` 並設定 `content`路徑。
- [x] 建立 `app/static/css/input.css` 並引入 TailwindCSS 指令。

## 資料檔案
- [x] 建立 `data/settings.json` 並填入提供的範例內容。(遷移至 PostgreSQL 後將被取代)
- [x] 建立 `data/subscriptions.json` 並填入初始空陣列或範例資料。(遷移至 PostgreSQL 後將被取代)

## 後端開發 (Flask)
- **`run.py`**:
    - [x] 建立 Flask 應用程式啟動腳本。
- **`app/__init__.py`**:
    - [x] 實作 `create_app` Flask App Factory。
    - [x] 從 `.env` 讀取 `SECRET_KEY`。
    - [ ] (新) 初始化 SQLAlchemy 並設定資料庫連線 (讀取 `DATABASE_URL`)。
    - [x] 註冊 `routes` 藍圖。
    - [x] 加入 `current_year` 上下文處理器。
- **`app/models.py`**:
    - [ ] (新) 定義 `Settings` SQLAlchemy 模型。
    - [ ] (新) 定義 `Subscription` SQLAlchemy 模型。
    - [ ] (修改) `get_settings()` 函式改為從 PostgreSQL 讀取。
    - [ ] (修改) `get_all_subscriptions()` 函式改為從 PostgreSQL 讀取。
    - [ ] (修改) `get_subscription_by_id(id)` 函式改為從 PostgreSQL 讀取。
    - [ ] (修改) `add_subscription(data)` 函式改為寫入 PostgreSQL (處理 `id`, `createdAt`, `updatedAt` 邏輯可能由 DB 或 ORM 控制)。
    - [ ] (修改) `update_subscription(id, data)` 函式改為更新 PostgreSQL (處理 `updatedAt` 邏輯可能由 DB 或 ORM 控制)。
    - [ ] (修改) `delete_subscription(id)` 函式改為從 PostgreSQL 刪除。
- **`app/routes.py`**:
    - [x] 建立 `main` 藍圖。
    - [x] `GET /`: 渲染 `index.html`。
    - [ ] (確認) `GET /api/settings`: 確認回傳從 PostgreSQL 取得的設定內容。
    - [ ] (確認) `GET /api/subscriptions`: 確認回傳從 PostgreSQL 取得的所有訂閱項目。
    - [ ] (確認) `POST /api/subscriptions`: 確認能新增訂閱項目至 PostgreSQL。
    - [ ] (確認) `GET /api/subscriptions/<id>`: 確認能從 PostgreSQL 回傳指定 ID 的訂閱項目。
    - [ ] (確認) `PUT /api/subscriptions/<id>`: 確認能更新 PostgreSQL 中指定 ID 的訂閱項目。
    - [ ] (確認) `DELETE /api/subscriptions/<id>`: 確認能從 PostgreSQL 刪除指定 ID 的訂閱項目。
    - [ ] (確認) `GET /api/stats`: 確認統計回傳基於 PostgreSQL 資料。
- **`app/services.py`**:
    - [x] (MVP 初期) 實作 `calculate_statistics(subscriptions, equivalency_items, target_currency)` 函式 (目前在 `routes.py` 中有類似的簡化實現，可視為部分完成或待重構至此)。

## 前端開發 (HTML, CSS, JavaScript)
- **`app/templates/base.html`**:
    - [x] 建立基礎 HTML 佈局。
- **`app/templates/index.html`**:
    - [x] 基本 HTML 結構，使用 TailwindCSS。
    - [x] 包含訂閱列表區域、新增按鈕、統計區域。
    - [x] 引入 `main.js` 和 `style.css`。
    - [x] 包含 Modal 結構及基本開關邏輯。
- **`app/templates/partials/_subscription_form.html`**:
    - [x] 訂閱表單的 HTML 結構。
    - [x] 欄位選項 (如服務、標籤、貨幣) 將由 JS 動態填充 (已規劃)。
- **`app/templates/partials/_subscription_item.html`**:
    - [x] 單個訂閱項目的 HTML 卡片結構，包含編輯/刪除按鈕。
- **`app/static/js/main.js`**:
    - [x] **頁面載入**:
        - [x] 呼叫 `/api/settings` 獲取設定，填充表單下拉選單。
        - [x] 呼叫 `/api/subscriptions` 獲取訂閱，動態渲染列表。
    - [x] **新增訂閱**:
        - [x] 顯示表單。
        - [x] 收集表單資料，呼叫 `POST /api/subscriptions`。
        - [x] 成功後更新列表。
    - [x] **編輯訂閱**:
        - [x] 點擊編輯，填充表單。
        - [x] 呼叫 `PUT /api/subscriptions/<id>`。
        - [x] 成功後更新列表。
    - [x] **刪除訂閱**:
        - [x] 點擊刪除，確認後呼叫 `DELETE /api/subscriptions/<id>`。
        - [x] 成功後移除項目。
    - [x] **統計顯示**:
        - [x] 呼叫 `/api/stats` (前端已呼叫)。
        - [x] 顯示月費、年費、商品換算結果。
- **`app/static/css/style.css`**:
    - [x] 透過 `npm run tailwind:css` 從 `input.css` 編譯產生 (已設定指令)。

## 文件
- [x] `README.md` (已完成首次生成，根據目前進度更新)
- [x] `FRAMEWORK.md` (已完成首次生成，根據目前進度更新)
- [x] `FLOW.md` (已完成首次生成，根據目前進度更新)
- [x] `TODO.md` (本檔案，正在更新)
- [x] `.gitignore`
- [ ] (新) `INIT.MD` (已建立，包含專案初始化總結與 PostgreSQL 整合規劃)

## (新) 資料庫整合 (PostgreSQL)

### 階段一：本地 PostgreSQL 整合
- [x] **環境準備** (使用者已自行完成)
    - [x] 安裝 PostgreSQL 本地服務。
    - [x] 建立專用的資料庫 (e.g., `starbaba_db`) 和使用者。
- [x] **專案修改**
    - [x] **新增依賴**: 在 `requirements.txt` 中加入 `psycopg2-binary` 和 `Flask-SQLAlchemy`。
    - [x] **環境變數**: 在 `.env` 和 `.env.example` 中新增 `DATABASE_URL` (使用者已手動處理 `.env`)。
    - [x] **資料庫模型 (`app/models.py`)**: 完成 SQLAlchemy 模型定義與調整 (對應 DDL)。
    - [x] **應用程式初始化 (`app/__init__.py`)**: 完成 SQLAlchemy 初始化與資料庫連線設定。
    - [ ] (可選) 整合資料庫遷移工具如 `Flask-Migrate`。 (目前未執行)
- [x] **資料遷移**
    - [x] 編寫一次性遷移腳本 (使用者已手動將 `data/*.json` 內容匯入 PostgreSQL)。
        - [ ] 腳本讀取 `data/settings.json` 並寫入 PostgreSQL `Settings` 表。(手動完成)
        - [ ] 腳本讀取 `data/subscriptions.json` 並寫入 PostgreSQL `Subscription` 表。(手動完成)
    - [x] 執行並驗證遷移腳本。(手動完成並由使用者驗證)
- [x] **測試**
    - [x] 全面測試應用程式 CRUD 操作及統計功能 (使用者已確認 API 測試成功)。

**階段一：本地 PostgreSQL 整合已完成。**

### 階段二：部署至 Heroku PostgreSQL
- [ ] **Heroku 設定**
    - [ ] 在 Heroku 應用程式中新增 Heroku Postgres 附加服務。
    - [ ] 確認應用程式能讀取 Heroku 設定的 `DATABASE_URL`。
- [ ] **程式碼調整 (如有必要)**
    - [ ] 確保資料庫設定能處理 Heroku 環境。
    - [ ] 若使用 `Flask-Migrate`，確保遷移指令能在 Heroku 執行。
- [ ] **部署**
    - [ ] 將更新後的程式碼部署到 Heroku。
- [ ] **資料庫遷移/初始化 (Heroku)**
    - [ ] 在 Heroku 上建立資料庫結構 (e.g., `Flask-Migrate upgrade` 或 ORM 自動建立)。
    - [ ] 在 Heroku 環境執行資料遷移 (若直接從 JSON 或本地同步)。
- [ ] **測試**
    - [ ] 在 Heroku 環境全面測試應用程式功能。