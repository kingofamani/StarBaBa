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
- [x] 建立 `data/settings.json` 並填入提供的範例內容。
- [x] 建立 `data/subscriptions.json` 並填入初始空陣列或範例資料。

## 後端開發 (Flask)
- **`app.py`**:
    - [x] 建立 Flask 應用程式啟動腳本。
- **`app/__init__.py`**:
    - [x] 實作 `create_app` Flask App Factory。
    - [x] 從 `.env` 讀取 `SECRET_KEY`。
    - [x] 註冊 `routes` 藍圖。
    - [x] 加入 `current_year` 上下文處理器。
- **`app/models.py`**:
    - [x] 實作 `get_settings()` 函式以讀取 `data/settings.json`。
    - [x] 實作 `get_all_subscriptions()` 函式以讀取 `data/subscriptions.json`。
    - [x] 實作 `get_subscription_by_id(id)` 函式。
    - [x] 實作 `add_subscription(data)` 函式 (自動生成 `id`, `createdAt`, `updatedAt`)。
    - [x] 實作 `update_subscription(id, data)` 函式 (自動更新 `updatedAt`)。
    - [x] 實作 `delete_subscription(id)` 函式。
- **`app/routes.py`**:
    - [x] 建立 `main` 藍圖。
    - [x] `GET /`: 渲染 `index.html`。
    - [x] `GET /api/settings`: 回傳 `settings.json` 內容。
    - [x] `GET /api/subscriptions`: 回傳所有訂閱項目。
    - [x] `POST /api/subscriptions`: 新增訂閱項目。
    - [x] `GET /api/subscriptions/<id>`: 回傳指定 ID 的訂閱項目。
    - [x] `PUT /api/subscriptions/<id>`: 更新指定 ID 的訂閱項目。
    - [x] `DELETE /api/subscriptions/<id>`: 刪除指定 ID 的訂閱項目。
    - [x] `GET /api/stats`: MVP 初期已實作簡化統計回傳 (總月費/年費/商品換算)。
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