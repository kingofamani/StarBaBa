# StarBaBa 專案初始化總結與規劃

## 一、現有專案理解 (基於 TODO.md, FRAMEWORK.MD, FLOW.MD, README.MD)

StarBaBa 是一個個人訂閱管理 Web 應用程式的最小可行性產品 (MVP)。

**核心目標：**
*   追蹤個人訂閱服務。
*   管理訂閱相關支出。
*   透過商品換算直觀了解支出。

**技術棧：**
*   **後端：** Python (Flask)
*   **前端：** HTML, JavaScript, CSS (TailwindCSS)
*   **資料儲存 (MVP)：** JSON 檔案 (`data/settings.json`, `data/subscriptions.json`)
*   **環境管理：** `.env`, `requirements.txt`, `package.json`

**主要功能模組：**
*   **資料模型 (`app/models.py`)：** 負責讀寫 JSON 檔案，處理訂閱和設定的 CRUD 操作。
*   **路由 (`app/routes.py`)：** 定義 API 端點，處理 HTTP 請求，調用模型和服務。
*   **服務 (`app/services.py`)：** 包含業務邏輯，如統計計算 (MVP 初期部分邏輯在 `routes.py`)。
*   **前端 (`app/static/js/main.js`, `app/templates/`)：** 負責頁面渲染、使用者互動、API 請求。

**核心流程：**
1.  **首次載入：** 獲取設定和訂閱資料，渲染主頁面及統計資訊。
2.  **新增訂閱：** 前端收集資料 -> 後端 API 處理 -> 更新 JSON -> 前端更新視圖。
3.  **編輯訂閱：** 前端獲取資料填充表單 -> 後端 API 處理 -> 更新 JSON -> 前端更新視圖。
4.  **刪除訂閱：** 前端確認 -> 後端 API 處理 -> 更新 JSON -> 前端更新視圖。
5.  **查看統計：** 根據當前訂閱資料計算並顯示。

**已完成事項：**
根據 `TODO.md`，專案已完成 MVP 的大部分核心功能，包括環境設定、前後端基本架構、JSON 資料的 CRUD 操作以及基本統計顯示。

## 二、新功能規劃：整合 PostgreSQL 資料庫

**目標：** 將 `data/settings.json` 和 `data/subscriptions.json` 的資料管理遷移至 PostgreSQL 資料庫，先在本地環境實現，最終部署到 Heroku PostgreSQL。

**預期效益：**
*   更可靠和高效的資料儲存。
*   更佳的資料一致性和完整性。
*   為未來功能擴展（如更複雜查詢、使用者認證）打下基礎。

**階段性實施計畫：**

### 階段一：本地 PostgreSQL 整合

1.  **環境準備：**
    *   安裝 PostgreSQL 本地服務。
    *   建立專用的資料庫 (e.g., `starbaba_db`) 和使用者。
2.  **專案修改：**
    *   **新增依賴：** 在 `requirements.txt` 中加入 `psycopg2-binary` (PostgreSQL 適配器) 和 `Flask-SQLAlchemy` (簡化 SQLAlchemy 與 Flask 的整合，建議使用) 或直接使用 `SQLAlchemy`。
    *   **環境變數：** 在 `.env` 和 `.env.example` 中新增 `DATABASE_URL`，格式如 `postgresql://user:password@host:port/database_name`。
    *   **資料庫模型 (`app/models.py`)：**
        *   使用 SQLAlchemy (或 Flask-SQLAlchemy) 定義 `Settings` 和 `Subscription` 兩個資料表模型，欄位對應原 JSON 結構。
        *   確保模型包含必要的欄位類型、約束（如主鍵、外鍵、非空等）。
        *   修改現有的資料存取函式 (`get_settings`, `get_all_subscriptions`, `add_subscription`, etc.)，使其透過 SQLAlchemy ORM 與 PostgreSQL 互動，而非讀寫 JSON 檔案。
    *   **應用程式初始化 (`app/__init__.py`)：**
        *   初始化 SQLAlchemy (或 Flask-SQLAlchemy)。
        *   設定從環境變數讀取 `DATABASE_URL`。
        *   (可選) 整合資料庫遷移工具如 `Flask-Migrate` (基於 Alembic)。
3.  **資料遷移：**
    *   **編寫一次性遷移腳本：** (例如放在 `manage.py` 或一個獨立的 `db_init_script.py` 中)
        *   腳本連接到 PostgreSQL 資料庫。
        *   讀取 `data/settings.json` 檔案內容，將其轉換並寫入 `Settings` 表。
        *   讀取 `data/subscriptions.json` 檔案內容，將其轉換並寫入 `Subscription` 表。
        *   確保 `id`、`createdAt`、`updatedAt` 等欄位正確處理。
4.  **測試：**
    *   執行遷移腳本，確認資料成功匯入。
    *   全面測試應用程式的所有功能 (CRUD 操作、統計顯示)，確保其基於 PostgreSQL 資料庫正常運作。

### 階段二：部署至 Heroku PostgreSQL

1.  **Heroku 設定：**
    *   在 Heroku 應用程式中新增 Heroku Postgres 附加服務。
    *   Heroku 會自動設定一個 `DATABASE_URL` 環境變數，指向此 PostgreSQL 服務。確保應用程式能讀取此環境變數。
2.  **程式碼調整 (如有必要)：**
    *   確保 `app/__init__.py` 中的資料庫設定能正確處理 Heroku 提供的 `DATABASE_URL`。
    *   若使用 `Flask-Migrate`，確保遷移指令能在 Heroku 環境執行。
3.  **部署：**
    *   將更新後的程式碼部署到 Heroku。
4.  **資料庫遷移/初始化 (Heroku)：**
    *   如果 Heroku 上的資料庫是空的，需要執行資料庫結構建立 (例如，透過 `Flask-Migrate` 的 `upgrade` 指令，或者如果沒有遷移工具，則首次部署時 SQLAlchemy 會根據模型建立表結構)。
    *   接著，需要在 Heroku 環境執行一次性的資料遷移腳本 (將本地 JSON 資料或已在本地資料庫的資料同步到 Heroku DB，這一步需要謹慎規劃，或者在本地開發完成後，直接以 Heroku DB 為主要資料來源進行操作)。
    *   **另一種策略**：在本地完成所有開發和資料遷移至本地 PostgreSQL 後，可以 dump 本地 PostgreSQL 資料，然後 restore 到 Heroku PostgreSQL。
5.  **測試：**
    *   在 Heroku 環境全面測試應用程式功能。

**文字式流程圖 (已於上一則訊息提供)**
**文字式程式架構圖 (已於上一則訊息提供)**

## 三、後續步驟建議

1.  依照【階段一：本地 PostgreSQL 整合】開始進行開發。
2.  優先完成環境設定和資料庫模型的建立。
3.  編寫並測試資料遷移腳本。
4.  逐步修改 `app/models.py` 和相關的 `app/routes.py` 邏輯。
5.  充分測試本地整合後，再進行 Heroku 部署。

此 `INIT.MD` 檔案已包含對現有專案的理解以及新功能 PostgreSQL 整合的詳細規劃。 