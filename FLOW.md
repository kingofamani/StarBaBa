# StarBaBa MVP - 應用程式流程

本文件描述 StarBaBa 應用程式的核心使用者流程和相關的系統互動。

## 1. 首次載入與顯示

1.  **使用者**: 開啟瀏覽器並存取應用程式根路徑 (`/`)。
2.  **瀏覽器**: 向後端 Flask 應用程式發送 `GET /` 請求。
3.  **後端 (`app/routes.py`)**: 接收請求，執行對應的路由處理函式。
4.  **後端**: 渲染 `app/templates/index.html` 模板並回傳給瀏覽器。
5.  **瀏覽器**: 載入 `index.html`。
    *   `index.html` 內部連結 `app/static/css/style.css` (TailwindCSS 編譯後) 和 `app/static/js/main.js`。
6.  **前端 (`app/static/js/main.js`)**: 腳本開始執行。
    *   **非同步請求設定**: 發送 `GET /api/settings` 請求。
        *   **後端 (`app/routes.py`)**: 處理 `/api/settings`，呼叫 `app/models.py` 中的 `get_settings()` 函式。
        *   **後端 (`app/models.py`)**: 透過 ORM 從 PostgreSQL 資料庫的 `Settings` 表讀取設定資料。
        *   **後端**: 將設定資料以 JSON 格式回傳。
        *   **前端 (`main.js`)**: 收到設定資料，用於後續填充表單下拉選單。
    *   **非同步請求訂閱**: 發送 `GET /api/subscriptions` 請求。
        *   **後端 (`app/routes.py`)**: 處理 `/api/subscriptions`，呼叫 `app/models.py` 中的 `get_all_subscriptions()` 函式。
        *   **後端 (`app/models.py`)**: 透過 ORM 從 PostgreSQL 資料庫的 `Subscription` 表讀取所有訂閱記錄。
        *   **後端**: 將訂閱列表以 JSON 格式回傳。
        *   **前端 (`main.js`)**: 收到訂閱列表資料。
7.  **前端 (`main.js`)**: 動態渲染訂閱列表。
    *   遍歷收到的訂閱資料。
    *   對於每個訂閱項目，使用 `app/templates/partials/_subscription_item.html` 的結構生成 HTML。
    *   將生成的 HTML 插入到 `index.html` 中指定的訂閱列表區域。
8.  **前端 (`main.js`)**: 計算並顯示統計資訊。
    *   (方式一: 前端計算) 使用已獲取的訂閱資料和設定資料（特別是 `equivalencyItems` 和 `defaultCurrency`）在前端計算總月費、年費和商品換算結果。
    *   (方式二: 後端計算) (可選) 發送 `GET /api/stats` 請求，後端處理並回傳統計結果。
    *   將統計結果顯示在 `index.html` 中指定的統計區域。

## 2. 新增訂閱

1.  **使用者**: 點擊「新增訂閱」按鈕。
2.  **前端 (`main.js`)**: 觸發事件處理器。
    *   顯示訂閱表單 (可能是一個 Modal，使用 `app/templates/partials/_subscription_form.html` 的結構)。
    *   表單中的下拉選單 (如服務類型、標籤、貨幣、付款週期) 已由先前從 `/api/settings` 獲取的資料填充。
3.  **使用者**: 填寫表單中的訂閱詳細資訊 (服務名稱、價格、週期等) 並點擊「儲存」或「提交」按鈕。
4.  **前端 (`main.js`)**: 收集表單所有欄位的資料。
    *   進行基本的前端驗證 (MVP 可簡化)。
    *   建構一個包含訂閱資料的 JSON 物件。
5.  **前端 (`main.js`)**: 發送 `POST /api/subscriptions` 請求到後端，請求主體 (body) 為 JSON 格式的訂閱資料。
6.  **後端 (`app/routes.py`)**: 接收 `POST` 請求。
    *   呼叫 `app/models.py` 中的 `add_subscription(data)` 函式，傳入從請求中解析的訂閱資料。
7.  **後端 (`app/models.py` - `add_subscription`)**:
    *   使用 SQLAlchemy 模型接收資料。
    *   (ORM 通常處理 `id` 的生成，`createdAt`, `updatedAt` 時間戳可由資料庫或 ORM 自動管理)。
    *   將新的訂閱物件儲存到 PostgreSQL 資料庫的 `Subscription` 表。
    *   回傳新建立的訂閱物件 (或成功訊息)。
8.  **前端 (`main.js`)**: 接收後端的回應。
    *   若成功：
        *   將新的訂閱項目動態添加到前端的訂閱列表中 (無需重新整理頁面)。
        *   更新統計數據的顯示。
        *   清空表單欄位並隱藏表單/Modal。
        *   (可選) 顯示成功訊息。
    *   若失敗：
        *   顯示錯誤訊息。

## 3. 編輯訂閱 (MVP 可先簡化或不做)

1.  **使用者**: 在某個已存在的訂閱項目上點擊「編輯」按鈕。
2.  **前端 (`main.js`)**: 觸發事件處理器。
    *   獲取該訂閱項目的 `id`。
    *   (可選，推薦) 發送 `GET /api/subscriptions/<id>` 請求以獲取最新的訂閱資料。
    *   使用獲取到的訂閱資料填充 `_subscription_form.html` 表單 (與新增訂閱共用表單結構)。
    *   顯示已填充資料的表單。
3.  **使用者**: 修改表單中的資訊並點擊「儲存」或「更新」按鈕。
4.  **前端 (`main.js`)**: 收集修改後的表單資料。
    *   建構一個包含更新後訂閱資料的 JSON 物件。
5.  **前端 (`main.js`)**: 發送 `PUT /api/subscriptions/<id>` 請求到後端，`<id>` 是被編輯訂閱的 ID，請求主體為 JSON 格式的更新資料。
6.  **後端 (`app/routes.py`)**: 接收 `PUT` 請求。
    *   呼叫 `app/models.py` 中的 `update_subscription(id, data)` 函式。
7.  **後端 (`app/models.py` - `update_subscription`)**:
    *   根據 `id` 透過 ORM 找到對應的訂閱記錄。
    *   更新該記錄的欄位值。
    *   (ORM 通常處理 `updatedAt` 時間戳的自動更新)。
    *   將更新儲存回 PostgreSQL 資料庫的 `Subscription` 表。
    *   回傳更新後的訂閱物件 (或成功訊息)。
8.  **前端 (`main.js`)**: 接收後端的回應。
    *   若成功：
        *   更新前端訂閱列表中對應項目的顯示。
        *   更新統計數據的顯示。
        *   隱藏表單/Modal。
        *   (可選) 顯示成功訊息。
    *   若失敗：
        *   顯示錯誤訊息。

## 4. 刪除訂閱

1.  **使用者**: 在某個已存在的訂閱項目上點擊「刪除」按鈕。
2.  **前端 (`main.js`)**: 觸發事件處理器。
    *   獲取該訂閱項目的 `id`。
    *   顯示一個確認對話框 (例如 `window.confirm()`)，詢問使用者是否確定刪除。
3.  **使用者**: 確認刪除。
4.  **前端 (`main.js`)**: 發送 `DELETE /api/subscriptions/<id>` 請求到後端，`<id>` 是被刪除訂閱的 ID。
5.  **後端 (`app/routes.py`)**: 接收 `DELETE` 請求。
    *   呼叫 `app/models.py` 中的 `delete_subscription(id)` 函式。
6.  **後端 (`app/models.py` - `delete_subscription`)**:
    *   根據 `id` 透過 ORM 從 PostgreSQL 資料庫的 `Subscription` 表中刪除對應的記錄。
    *   回傳成功訊息。
7.  **前端 (`main.js`)**: 接收後端的回應。
    *   若成功：
        *   從前端的訂閱列表中移除該項目。
        *   更新統計數據的顯示。
        *   (可選) 顯示成功訊息。
    *   若失敗：
        *   顯示錯誤訊息。

## 5. 查看統計資訊

此流程與「首次載入與顯示」的步驟 7 和 8 相關，並且在新增、編輯或刪除訂閱後會被觸發更新。

1.  **觸發時機**: 頁面初始載入完成後，或在訂閱列表發生變更 (新增、編輯、刪除) 後。
2.  **資料來源**:
    *   所有訂閱項目: 從 `/api/subscriptions` (後端從 PostgreSQL) 獲取。
    *   商品換算設定: 從 `/api/settings` (後端從 PostgreSQL) 獲取的 `equivalencyItems` 和 `defaultCurrency`。
3.  **計算邏輯 (`main.js` 請求 `/api/stats`，後端在 `app/routes.py` 中計算，資料來源為 PostgreSQL)**:
    *   篩選 `isActive: true` 的訂閱項目。
    *   根據 `billingCycle` 和 `price` 計算總月費和總年費 (需要將不同週期的費用統一轉換，例如年繳費用除以12得到月費)。
    *   (MVP階段假設所有訂閱和商品都是 `defaultCurrency`，未來可擴展貨幣轉換)。
    *   遍歷 `equivalencyItems`，用計算出的總花費 (例如總月費) 除以每個商品的 `price`，得到可換算的商品數量。
4.  **前端 (`main.js`)**: 將計算出的總月費、總年費以及各商品的換算數量更新到 `index.html` 中指定的統計區域。

---

# 📊 資料庫部署與遷移指南

## 6. Supabase PostgreSQL 資料庫部署 🚀

### 6.1 前置準備

1.  **註冊 Supabase 帳號**:
    *   前往 [supabase.com](https://supabase.com) 註冊免費帳號
    *   可以使用 GitHub、Google 或 Email 註冊
    *   **免費方案包含**：500MB 資料庫空間、50MB 檔案儲存、50,000 月活躍使用者

2.  **安裝 Supabase CLI** (可選，但推薦):
    *   **Windows (PowerShell)**:
        ```powershell
        # 安裝 Scoop (如果沒有的話)
        Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
        irm get.scoop.sh | iex
        
        # 安裝 Supabase CLI
        scoop install supabase
        ```
    *   **macOS**: `brew install supabase/tap/supabase`
    *   **Linux**: `npm install -g supabase`
    *   **使用 npm**: `npm install -g supabase`

### 6.2 建立 Supabase 專案

1.  **建立新專案**:
    *   登入 [Supabase Dashboard](https://app.supabase.com)
    *   點擊「New project」
    *   選擇組織（個人帳號會自動建立預設組織）

2.  **設定專案資訊**:
    *   **Name**: `starbaba-mvp` 或您喜歡的名稱
    *   **Database Password**: 設定一個強密碼（**請記住，稍後需要使用**）
    *   **Region**: 選擇最接近您用戶的區域（如 Southeast Asia (Singapore)）
    *   **Pricing Plan**: 選擇「Free」

3.  **等待專案建立**:
    *   通常需要 1-2 分鐘
    *   建立完成後會看到專案 Dashboard

### 6.3 ⚠️ 取得資料庫連線資訊 (重要步驟)

1.  **進入專案設定**:
    *   在 Supabase Dashboard 中，點擊左側選單的「Settings」
    *   選擇「Database」

2.  **🔥 重要：選擇正確的連線方式**:
    *   在「Connection string」區段，您會看到兩個選項：
        1. ❌**「Direct connection」** - 直接連接
        2. ✅**「Connection pooling」** - 連接池 ⭐

    *   **📢 請務必選擇第二項⭐「Connection pooling」！**
    
    **為什麼必須使用 Connection Pooling？**
    - ✅ **穩定性更好**：避免連接數超限問題
    - ✅ **效能更佳**：連接池管理，減少連接建立開銷
    - ✅ **適合生產環境**：Supabase 推薦的最佳實務
    - ❌ **Direct connection 問題**：容易遇到 DNS 解析失敗、連接超時等問題

3.  **複製 Connection pooling 連線字串**:
    *   選擇「Transaction pooler」模式
    *   複製類似以下格式的 URI：
        ```
        postgresql://postgres.xxxxxxxxxxxx:password@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres
        ```
    
    **連線字串格式說明**:
    - **Host**: `aws-0-ap-southeast-1.pooler.supabase.com` (注意有 `.pooler`)
    - **Port**: `5432` (Transaction pooler) 或 `6543` (Session pooler)
    - **Database**: `postgres`
    - **Username**: `postgres.xxxxxxxxxxxx` (注意前綴格式)
    - **Password**: 您在建立專案時設定的密碼

### 6.4 設定本地環境

1.  **更新 `.env` 檔案**:
    ```env
    # Flask 設定
    SECRET_KEY=your-secret-key-here
    
    # 🔥 重要：使用 Connection pooling 連線字串
    DATABASE_URL=postgresql://postgres.xxxxxxxxxxxx:your-password@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres
    
    # Supabase 額外資訊 (可選，未來擴展用)
    SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
    SUPABASE_ANON_KEY=your-anon-key
    SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
    ```

2.  **取得 Supabase API 金鑰** (可選，未來擴展用):
    *   在 Supabase Dashboard > Settings > API
    *   複製「anon」和「service_role」金鑰

### 6.5 建立資料庫結構

#### 方法 A: 使用 Supabase SQL Editor (推薦)

### 6.6 資料遷移：使用 pgAdmin 操作 📋

#### 步驟 1: 從本地資料庫匯出資料

1.  **開啟 pgAdmin**:
    *   連接到您的本地 PostgreSQL 伺服器

2.  **選擇要備份的資料庫(包含資料表建立與資料轉移)**:
    *   在左側物件瀏覽器中，右鍵點擊包含 `app_settings` 和 `subscriptions` 資料表的資料庫
    *   選擇「Backup...」

3.  **在「Backup」對話方塊中設定**:
    
    **General (一般) 標籤頁**:
    - **Filename (檔案名稱)**: 指定匯出檔案位置，例如 `starbaba_backup.sql`
    - **Format (格式)**: 選擇「Plain」

    **Objects (物件) 標籤頁**:
    - 展開您的綱要 (通常是 `public`)
    - 在「Tables」清單中，**只勾選** `app_settings` 和 `subscriptions`
    - 確保其他資料表是未勾選狀態
    - **也要勾選✅「Sequences」** (用於 SERIAL 欄位)

    **Dump Options (傾印選項) 標籤頁**:
    - **Use Insert Commands**: ✅ 勾選
    - **Use Column Inserts**: ✅ 勾選 (推薦)
    - **Owner**: ❌ 取消勾選
    - **Privileges**: ❌ 取消勾選

4.  **執行備份**:
    *   點擊「Backup」按鈕
    *   等待匯出完成

#### 步驟 2: 修改 SQL 檔案

1.  **開啟匯出的 `.sql` 檔案**:
    *   使用文字編輯器（如 VS Code、Notepad++）開啟

2.  **移除 schema 前綴**:
    *   將檔案中所有的⭐ `public.` 字串刪除
    *   例如：將 `public.app_settings` 改為 `app_settings`

3.  **檢查並修正**:
    *   確認 SQL 語法正確
    *   移除不必要的 Owner 或 Grant 語句

#### 步驟 3: 匯入到 Supabase

1.  **回到 Supabase SQL Editor**:
    *   在 Supabase Dashboard 左側選單點擊「SQL Editor」
    *   複製修改後的 `.sql` 檔案內容

2.  **貼上並執行**:
    *   將 SQL 內容貼上到 SQL Editor 中
    *   點擊「Run」執行

3.  **驗證資料**:
    *   前往「Table Editor」
    *   檢查 `app_settings` 和 `subscriptions` 資料表
    *   確認資料已正確匯入

### 6.7 使用 Supabase CLI 初始化本地 Supabase 專案

1.  **初始化本地 Supabase 專案**:
    ```bash
    # 在專案根目錄執行
    supabase init
    ```
    *   會建立 `supabase/` 目錄和相關配置檔案
    *   選擇所有問題都回答 "N" (使用預設設定)

2.  **連結到遠端 Supabase 專案**:
    ```bash
    # 替換 your-project-ref 為您的專案 ID
    supabase link --project-ref your-project-ref
    ```
    *   專案 ID 可在 Supabase Dashboard > Settings > General 中找到
    *   會要求輸入資料庫密碼 (建立專案時設定的密碼)

3.  **修改 `supabase/config.toml` 配置檔案**:
    ```toml
    # 開啟檔案: supabase/config.toml
    
    [api]
    # 設定 API 版本
    enabled = true
    port = 54321
    
    [db]
    # 資料庫設定 (本地開發用)
    port = 54322
    major_version = 15
    
    [studio]
    # Supabase Studio 設定
    enabled = true
    port = 54323
    
    [auth]
    # 認證設定 (未來使用)
    enabled = true
    
    [storage]
    # 檔案儲存設定 (未來使用)
    enabled = false
    ```

4.  **檢查 Supabase 狀態**:
    ```bash
    supabase status
    ```
    *   顯示本地和遠端專案的連接狀態
    *   確認是否成功連結到遠端專案

### 6.8 測試連線

1.  **在本地測試連線**:
    *   要設定postgresql在Windows path環境變數，例如：`C:\Program Files\PostgreSQL\17\bin`
    *   開啟PowerShell測試
    ```
    psql postgresql://postgres.[supabase專案project_id]:[你的密碼]@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres
    ```

2.  **啟動應用程式測試**:
    ```bash
    python run.py
    ```
    *   訪問 `http://localhost:5000`
    *   測試 API 端點: `http://localhost:5000/api/settings`

---

## 7. Flask 應用程式部署到 Heroku 🌐

### 7.1 前置準備

1.  **註冊 Heroku 帳號**:
    *   前往 [heroku.com](https://heroku.com) 註冊免費帳號
    *   驗證電子信箱

2.  **安裝 Heroku CLI**:
    *   **Windows**: 下載並安裝 [Heroku CLI for Windows](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli)
    *   **macOS**: `brew tap heroku/brew && brew install heroku`
    *   **Linux**: `curl https://cli-assets.heroku.com/install.sh | sh`

3.  **登入 Heroku CLI**:
    ```bash
    heroku login
    ```

### 7.2 準備部署檔案

1.  **確認 `Procfile` 存在** (專案根目錄):
    ```
    web: python run.py
    ```

2.  **確認 `requirements.txt` 完整**:
    ```bash
    pip freeze > requirements.txt
    ```

3.  **建立 `runtime.txt`** (可選):
    ```
    python-3.11.0
    ```

### 7.3 建立 Heroku 應用程式

1.  **建立應用程式**:
    ```bash
    heroku create your-starbaba-app
    ```

2.  **設定環境變數**:
    ```bash
    # 設定密鑰
    heroku config:set SECRET_KEY=your-secret-key
    
    # 🔥 重要：設定 Supabase 連線字串
    heroku config:set DATABASE_URL="postgresql://postgres.xxxxxxxxxxxx:password@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"
    ```

### 7.4 部署應用程式

1.  **確認 Git 提交**:
    ```bash
    git add .
    git commit -m "準備部署到 Heroku"
    ```

2.  **部署到 Heroku**:
    ```bash
    git push heroku main
    ```

3.  **查看應用程式**:
    ```bash
    heroku open
    ```

### 7.5 監控與維護

1.  **查看日誌**:
    ```bash
    heroku logs --tail
    ```

2.  **檢查應用程式狀態**:
    ```bash
    heroku ps
    ```

---

## 8. Supabase 進階功能與管理 ⚡

### 8.1 即時資料同步 (Real-time)

1.  **啟用資料表即時功能**:
    *   在 Supabase Dashboard > Database > Replication
    *   為 `subscriptions` 資料表開啟 Realtime

2.  **前端整合** (未來擴展):
    ```bash
    npm install @supabase/supabase-js
    ```

### 8.2 資料庫管理

1.  **查看使用量**:
    *   Supabase Dashboard > Settings > Usage

2.  **備份資料庫**:
    *   Settings > Database > Download backup

3.  **監控效能**:
    *   使用 SQL Editor 執行效能查詢

### 8.3 安全性設定

1.  **Row Level Security (RLS)**:
    ```sql
    -- 啟用 RLS (未來加入使用者認證時)
    ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
    ALTER TABLE app_settings ENABLE ROW LEVEL SECURITY;
    ```

2.  **API 金鑰管理**:
    *   定期更換 service_role 金鑰
    *   限制 anon 金鑰權限

---

## 🎯 部署檢查清單

### Supabase 設定 ✅
- [ ] 已建立 Supabase 專案
- [ ] **已使用 Connection pooling 連線字串**
- [ ] 資料表結構已建立
- [ ] 資料已成功遷移
- [ ] 本地連線測試通過

### Heroku 部署 ✅
- [ ] Heroku 應用程式已建立
- [ ] 環境變數已設定
- [ ] 應用程式成功部署
- [ ] API 端點正常運作
- [ ] 前端頁面正常顯示

### 驗證測試 ✅
- [ ] 新增訂閱功能正常
- [ ] 編輯訂閱功能正常
- [ ] 刪除訂閱功能正常
- [ ] 統計計算正確顯示
- [ ] 響應時間在可接受範圍內

完成以上步驟後，您的 StarBaBa 應用程式就成功部署在 Heroku + Supabase 的雲端架構上了！🎉 