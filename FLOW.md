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

## (新) 6. 資料庫初始化/遷移流程 (本地開發首次)

1.  **開發者**: 準備好本地 PostgreSQL 環境 (已安裝服務，建立資料庫和使用者)。 (使用者已完成)
2.  **開發者**: 設定 `.env` 檔案中的 `DATABASE_URL` 指向本地資料庫。 (使用者已完成)
3.  **應用程式/開發者**: (若使用 Flask-Migrate/Alembic)
    *   執行遷移指令 (例如 `flask db init`, `flask db migrate -m "Initial migration"`, `flask db upgrade`) 以在資料庫中建立表格結構。 (目前未使用)
4.  **開發者**: (若無遷移工具，SQLAlchemy 會在首次合適操作時嘗試根據模型 `Base.metadata.create_all(engine)` 建立表格)。 (資料庫表格由使用者根據 DDL 手動建立)
5.  **使用者**: 將 `data/settings.json` 和 `data/subscriptions.json` 的資料手動匯入到 PostgreSQL 的 `app_settings` 和 `subscriptions` 表。
    *   ~~**遷移腳本**: 連接到 PostgreSQL 資料庫。~~
    *   ~~**遷移腳本**: 讀取 `data/settings.json` 檔案內容。~~
    *   ~~**遷移腳本**: 將 `settings` 資料轉換並使用 ORM 寫入 PostgreSQL 的 `Settings` 表。~~
    *   ~~**遷移腳本**: 讀取 `data/subscriptions.json` 檔案內容。~~
    *   ~~**遷移腳本**: 將 `subscriptions` 資料轉換並使用 ORM 寫入 PostgreSQL 的 `Subscription` 表。~~
6.  **使用者**: 驗證資料是否成功匯入資料庫。
7.  **應用程式**: 正常啟動，從 PostgreSQL 讀寫資料。 (已由使用者測試 API 確認)

## (新) 7. Heroku 部署時的資料庫設定與遷移

### 7.1 前置準備

1.  **註冊 Heroku 帳號**:
    *   前往 [heroku.com](https://heroku.com) 註冊免費帳號。
    *   驗證電子信箱。

2.  **安裝 Heroku CLI**:
    *   **Windows**: 下載並安裝 [Heroku CLI for Windows](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli)
    *   **macOS**: `brew tap heroku/brew && brew install heroku`
    *   **Linux**: `curl https://cli-assets.heroku.com/install.sh | sh`

3.  **登入 Heroku CLI**:
    ```bash
    heroku login
    ```
    *   會開啟瀏覽器進行授權登入。

4.  **確認 Git 版本控制**:
    *   確保專案已初始化 Git (`git init`)。
    *   確保所有變更已提交 (`git add .` 和 `git commit -m "準備部署至 Heroku"`)。

### 7.2 建立 Heroku 應用程式

1.  **在專案根目錄建立 Heroku 應用程式**:
    ```bash
    heroku create your-app-name-starbaba
    ```
    *   如果不指定名稱，Heroku 會自動生成一個隨機名稱。
    *   應用程式名稱必須是全球唯一的。

2.  **確認遠端倉庫已新增**:
    ```bash
    git remote -v
    ```
    *   應該會看到 `heroku` 遠端指向您的 Heroku 應用程式。

### 7.3 新增 PostgreSQL 附加元件

1.  **新增 Heroku Postgres 附加元件**:
    ```bash
    heroku addons:create heroku-postgresql:essential-0
    ```
    *   `essential-0` 是免費方案，適合開發和小型應用。
    *   如需更多資源可選擇付費方案如 `mini`、`basic` 等。

2.  **確認 PostgreSQL 附加元件已新增**:
    ```bash
    heroku addons
    ```
    *   應該會看到 `heroku-postgresql` 附加元件。

3.  **查看資料庫資訊**:
    ```bash
    heroku pg:info
    ```
    *   會顯示資料庫版本、狀態、連線數等資訊。

4.  **確認 DATABASE_URL 環境變數**:
    ```bash
    heroku config
    ```
    *   應該會看到 `DATABASE_URL` 已自動設定。

### 7.4 設定應用程式部署檔案

1.  **建立 `Procfile`** (在專案根目錄):
    ```
    web: python run.py
    ```
    *   告訴 Heroku 如何啟動您的應用程式。

2.  **建立 `runtime.txt`** (在專案根目錄，可選):
    ```
    python-3.11.0
    ```
    *   指定 Python 版本 (如果不指定，Heroku 會使用預設版本)。

3.  **確認 `requirements.txt` 包含所有依賴**:
    *   確保包含 `Flask`, `Flask-SQLAlchemy`, `psycopg2-binary`, `python-dotenv` 等。

### 7.5 部署應用程式

1.  **設定必要的環境變數**:
    ```bash
    heroku config:set SECRET_KEY=your-secret-key-here
    ```
    *   可以生成一個新的密鑰：`python -c "import secrets; print(secrets.token_hex(16))"`

2.  **部署到 Heroku**:
    ```bash
    git push heroku main
    ```
    *   如果您的主分支是 `master`，則使用 `git push heroku master`。
    *   Heroku 會自動偵測 Python 應用程式並安裝依賴。

3.  **查看部署日誌**:
    ```bash
    heroku logs --tail
    ```
    *   即時查看應用程式日誌，排除部署問題。

### 7.6 建立資料庫結構

**方法 A: 使用 Flask-Migrate (推薦)**

1.  **安裝 Flask-Migrate** (本地):
    ```bash
    pip install Flask-Migrate
    # 更新 requirements.txt
    pip freeze > requirements.txt
    ```

2.  **修改 `app/__init__.py` 新增 Migrate**:
    ```python
    from flask_migrate import Migrate
    migrate = Migrate(app, db)
    ```

3.  **初始化遷移資料夾** (本地):
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

4.  **提交遷移檔案**:
    ```bash
    git add migrations/
    git commit -m "Add database migrations"
    git push heroku main
    ```

5.  **在 Heroku 執行遷移**:
    ```bash
    heroku run flask db upgrade
    ```

**方法 B: 直接使用 SQLAlchemy (較簡單)**

1.  **在 Heroku 執行 Python 指令建立表格**:
    ```bash
    heroku run python -c "
    from app import create_app, db
    app = create_app()
    with app.app_context():
        db.create_all()
        print('Tables created successfully')
    "
    ```

### 7.7 遷移資料到 Heroku PostgreSQL

**方法 A: 從本地 PostgreSQL 匯出/匯入 (推薦)**

1.  **從本地資料庫匯出資料**:
    ```bash
    pg_dump -h localhost -U your_username -d starbaba_db -f local_backup.sql
    ```

2.  **取得 Heroku 資料庫 URL**:
    ```bash
    heroku config:get DATABASE_URL
    ```

3.  **將資料匯入到 Heroku**:
    ```bash
    heroku pg:psql < local_backup.sql
    ```
    *   或者使用：`psql $(heroku config:get DATABASE_URL) < local_backup.sql`

**方法 B: 透過遷移腳本**

1.  **建立遷移腳本 `migrate_to_heroku.py`**:
    ```python
    import os
    import json
    from app import create_app, db
    from app.models import Settings, Subscription

    def migrate_data():
        app = create_app()
        with app.app_context():
            # 匯入設定資料
            with open('data/settings.json', 'r', encoding='utf-8') as f:
                settings_data = json.load(f)
            
            settings = Settings(**settings_data)
            db.session.add(settings)
            
            # 匯入訂閱資料
            with open('data/subscriptions.json', 'r', encoding='utf-8') as f:
                subscriptions_data = json.load(f)
            
            for sub_data in subscriptions_data:
                subscription = Subscription(**sub_data)
                db.session.add(subscription)
            
            db.session.commit()
            print("Data migration completed successfully")

    if __name__ == "__main__":
        migrate_data()
    ```

2.  **在 Heroku 執行遷移腳本**:
    ```bash
    heroku run python migrate_to_heroku.py
    ```

**方法 C: 使用 Heroku Postgres 匯入功能**

1.  **將本地資料庫備份上傳到可存取的 URL** (如 S3、Google Drive 等)

2.  **使用 Heroku 匯入功能**:
    ```bash
    heroku pg:backups:restore 'https://your-backup-url/backup.dump' DATABASE_URL
    ```

### 7.8 驗證部署

1.  **開啟應用程式**:
    ```bash
    heroku open
    ```

2.  **檢查資料庫連線**:
    ```bash
    heroku run python -c "
    from app import create_app, db
    from app.models import Settings, Subscription
    app = create_app()
    with app.app_context():
        settings_count = Settings.query.count()
        subscriptions_count = Subscription.query.count()
        print(f'Settings: {settings_count}, Subscriptions: {subscriptions_count}')
    "
    ```

3.  **查看應用程式日誌**:
    ```bash
    heroku logs --tail
    ```

4.  **測試 API 端點**:
    *   存取 `https://your-app-name.herokuapp.com/api/settings`
    *   存取 `https://your-app-name.herokuapp.com/api/subscriptions`

### 7.9 常見問題排除

1.  **資料庫連線問題**:
    ```bash
    heroku pg:info
    heroku logs --tail
    ```

2.  **應用程式無法啟動**:
    *   檢查 `Procfile` 是否正確
    *   檢查 `requirements.txt` 是否包含所有依賴
    *   查看日誌：`heroku logs --tail`

3.  **環境變數問題**:
    ```bash
    heroku config
    heroku config:set VAR_NAME=value
    ```

4.  **重新部署**:
    ```bash
    git add .
    git commit -m "Fix deployment issues"
    git push heroku main
    ```

### 7.10 Heroku PostgreSQL 管理

1.  **連接到 Heroku PostgreSQL**:
    ```bash
    heroku pg:psql
    ```

2.  **查看資料庫大小**:
    ```bash
    heroku pg:info
    ```

3.  **備份資料庫**:
    ```bash
    heroku pg:backups:capture
    heroku pg:backups:download
    ```

4.  **重置資料庫** (小心使用):
    ```bash
    heroku pg:reset DATABASE_URL
    ```

### 7.11 最終確認

1.  **功能測試**:
    *   測試新增訂閱
    *   測試編輯訂閱
    *   測試刪除訂閱
    *   測試統計顯示

2.  **效能監控**:
    ```bash
    heroku logs --tail
    heroku ps
    ```

3.  **設定自訂網域** (可選):
    ```bash
    heroku domains:add your-domain.com
    ```

完成以上步驟後，您的 StarBaBa 應用程式就成功部署到 Heroku 並連接到 Heroku PostgreSQL 了！

## 8. Supabase 部署時的資料庫設定與遷移

### 8.1 前置準備

1.  **註冊 Supabase 帳號**:
    *   前往 [supabase.com](https://supabase.com) 註冊免費帳號。
    *   可以使用 GitHub、Google 或 Email 註冊。
    *   免費方案包含：500MB 資料庫空間、50MB 檔案儲存、50,000 月活躍使用者。

2.  **安裝 Supabase CLI** (可選，但推薦):

    *   **Windows**:PowerShell 中執行：
`Set-ExecutionPolicy RemoteSigned -Scope CurrentUser # 可選，如果你的執行原則限制了腳本執行
irm get.scoop.sh | iex`
    *   **Windows**: `scoop install supabase`
    *   **macOS**: `brew install supabase/tap/supabase`
    *   **Linux**: `npm install -g supabase` 或下載 binary
    *   **使用 npm**: `npm install -g supabase`

3.  **登入 Supabase CLI** (如果安裝了):
    ```bash
    supabase login
    ```

### 8.2 建立 Supabase 專案

1.  **建立新專案**:
    *   登入 [Supabase Dashboard](https://app.supabase.com)
    *   點擊「New project」
    *   選擇組織（個人帳號會自動建立預設組織）

2.  **設定專案資訊**:
    *   **Name**: `starbaba-mvp` 或您喜歡的名稱
    *   **Database Password**: 設定一個強密碼（請記住，稍後需要使用）
    *   **Region**: 選擇最接近您用戶的區域（如 Southeast Asia (Singapore)）
    *   **Pricing Plan**: 選擇「Free」

3.  **等待專案建立**:
    *   通常需要 1-2 分鐘
    *   建立完成後會看到專案 Dashboard

### 8.3 取得資料庫連線資訊

1.  **進入專案設定**:
    *   在 Supabase Dashboard 中，點擊左側選單的「Settings」
    *   選擇「Database」

2.  **取得連線字串**:
    *   在「Connection string」區段找到「Direct connection」
    *   複製「Connection pooling」下的 URI
    *   格式類似：`postgresql://postgres.xxxxxxxxxxxx:password@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres`

3.  **記錄重要資訊**:
    *   **Host**: `aws-0-ap-southeast-1.pooler.supabase.com`
    *   **Port**: `6543` (Pooler) 或 `5432` (Direct)
    *   **Database**: `postgres`
    *   **Username**: `postgres.xxxxxxxxxxxx`
    *   **Password**: 您在建立專案時設定的密碼

### 8.4 設定本地環境

1.  **更新 `.env` 檔案**:
    ```env
    # 原有設定
    SECRET_KEY=your-secret-key-here
    
    # Supabase PostgreSQL 連線
    DATABASE_URL=postgresql://postgres.xxxxxxxxxxxx:your-password@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
    
    # Supabase 額外資訊 (可選)
    SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
    SUPABASE_ANON_KEY=your-anon-key
    SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
    ```

2.  **取得 Supabase API 金鑰** (可選，未來擴展用):
    *   在 Supabase Dashboard > Settings > API
    *   複製「anon」和「service_role」金鑰

### 8.5 建立資料庫結構

**方法 A: 使用 Supabase Dashboard (推薦，初學者友善)**
1.  **先匯出本地資料表及資料 SQL**:`
    1.1.	連接到你的資料庫：
    在 pgAdmin 的左側物件瀏覽器中，展開你的伺服器。
    1.2.	選擇要備份的資料庫：
    右鍵點擊你包含 app_settings 和 subscriptions 資料表的資料庫 (而不是個別資料表)。
    選擇「Backup...」。
    1.3.	在「Backup」對話方塊中設定：
        o	General (一般) 標籤頁：
            -Filename (檔案名稱)：指定匯出 SQL 檔案的名稱和儲存位置 (例如 selected_tables_backup.sql)。
            -Format (格式)：選擇「Plain」。
        o	Objects (物件) 標籤頁 (或 Data/Objects 標籤頁)：
            -這個標籤頁允許你選擇要包含在備份中的特定物件。
            -找到並展開你的綱要 (通常是 public)。
            -在該綱要下的「Tables」(資料表) 清單中，只勾選 app_settings 和 subscriptions。確保其他不想匯出的資料表是未勾選狀態。另外也勾選「Sequences」。            
        o	Dump Options (傾印選項) 標籤頁 (或 Data/Objects 標籤頁內的選項區塊，依 pgAdmin 版本)：
            -Section (區段)：
            -如果你希望匯出資料表結構 (CREATE TABLE) 和 資料 (INSERT INTO)，選擇「Schema and data」。
            -如果你在 Supabase 中已經手動建立了相同結構的資料表，只需要匯入資料，選擇「Data only」。
            -Type of statements (語句類型) / Queries (查詢)：
            -務必勾選「Use Insert Commands」(使用 INSERT 命令)。
            -建議勾選「Use Column Inserts」(使用欄位 INSERT)。
            -Clean objects (清除物件) / Drop objects (刪除物件)：
            -如果你選擇了「Schema and data」，並且希望在匯入 Supabase 前先刪除 Supabase 中可能已存在的同名資料表，可以勾選「Clean before restore」(或類似的「DROP objects」選項)。
            -Do not save (不儲存) / Save options (儲存選項)：
            -通常建議取消勾選「Owner」(擁有者) 和「Privileges」(權限)。
            -確認其他選項：通常其他選項保持預設即可。「Include CREATE DATABASE statement」應保持不勾選。
        o	點擊「Backup」按鈕。
    1.4.	修改.sql檔：
        o	將檔案內的「public.」全部刪除。
    1.5.	匯入supabase：
        o	左邊選單「SQL Editor」，將.sql檔內容貼上執行。
    `

**方法 B: 使用 Supabase CLI**

1.  **初始化本地專案**:
    ```bash
    supabase init
    supabase link --project-ref your-project-id
    ```

2.  **建立遷移檔案**:
    ```bash
    supabase migration new create_initial_tables
    ```

3.  **編輯遷移檔案** (在 `supabase/migrations/` 目錄):
    *   將上述 SQL 內容加入遷移檔案

4.  **推送到 Supabase**:
    ```bash
    supabase db push
    ```

### 8.6 資料遷移到 Supabase

**方法 A: 使用 Python 遷移腳本 (推薦)**

1.  **建立遷移腳本 `migrate_to_supabase.py`**:
    ```python
    import os
    import json
    import psycopg2
    from datetime import datetime
    from dotenv import load_dotenv

    load_dotenv()

    def migrate_data():
        # 連接到 Supabase PostgreSQL
        DATABASE_URL = os.getenv('DATABASE_URL')
        if not DATABASE_URL:
            print("錯誤：請在 .env 文件中設定 DATABASE_URL")
            return

        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            
            # 遷移設定資料
            print("開始遷移設定資料...")
            with open('data/settings.json', 'r', encoding='utf-8') as f:
                settings_data = json.load(f)
            
            cur.execute("""
                INSERT INTO app_settings (
                    service_types, tags, currencies, billing_cycles, 
                    equivalency_items, default_currency
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                json.dumps(settings_data.get('serviceTypes', [])),
                json.dumps(settings_data.get('tags', [])),
                json.dumps(settings_data.get('currencies', [])),
                json.dumps(settings_data.get('billingCycles', [])),
                json.dumps(settings_data.get('equivalencyItems', [])),
                settings_data.get('defaultCurrency', 'TWD')
            ))
            
            # 遷移訂閱資料
            print("開始遷移訂閱資料...")
            with open('data/subscriptions.json', 'r', encoding='utf-8') as f:
                subscriptions_data = json.load(f)
            
            for sub in subscriptions_data:
                cur.execute("""
                    INSERT INTO subscriptions (
                        service_name, service_type, price, currency, billing_cycle,
                        next_billing_date, is_active, tags, notes
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    sub.get('serviceName'),
                    sub.get('serviceType'),
                    sub.get('price'),
                    sub.get('currency', 'TWD'),
                    sub.get('billingCycle'),
                    sub.get('nextBillingDate'),
                    sub.get('isActive', True),
                    json.dumps(sub.get('tags', [])),
                    sub.get('notes')
                ))
            
            conn.commit()
            print(f"成功遷移 {len(subscriptions_data)} 筆訂閱資料")
            print("資料遷移完成！")
            
        except Exception as e:
            print(f"遷移過程中發生錯誤：{e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    if __name__ == "__main__":
        migrate_data()
    ```

2.  **安裝額外依賴** (如果尚未安裝):
    ```bash
    pip install psycopg2-binary
    pip freeze > requirements.txt
    ```

3.  **執行遷移腳本**:
    ```bash
    python migrate_to_supabase.py
    ```

**方法 B: 使用 Supabase Dashboard 手動匯入**

1.  **進入 Table Editor**:
    *   在 Supabase Dashboard 左側選單點擊「Table Editor」

2.  **選擇 app_settings 表格**:
    *   點擊「Insert」->「Insert row」
    *   手動輸入 settings.json 的內容

3.  **選擇 subscriptions 表格**:
    *   逐一新增 subscriptions.json 中的每筆資料

**方法 C: 使用 CSV 匯入**

1.  **將 JSON 轉換為 CSV 格式**
2.  **在 Supabase Dashboard 中使用匯入功能**

### 8.7 更新應用程式連線

1.  **確認應用程式能連接到 Supabase**:
    ```bash
    python -c "
    from app import create_app, db
    from app.models import Settings, Subscription
    app = create_app()
    with app.app_context():
        try:
            settings_count = Settings.query.count()
            subscriptions_count = Subscription.query.count()
            print(f'✅ 連線成功！Settings: {settings_count}, Subscriptions: {subscriptions_count}')
        except Exception as e:
            print(f'❌ 連線失敗：{e}')
    "
    ```

### 8.8 應用程式部署選項

**選項 A: 部署到 Vercel (推薦，與 Supabase 整合良好)**

1.  **安裝 Vercel CLI**:
    ```bash
    npm install -g vercel
    ```

2.  **建立 `vercel.json`**:
    ```json
    {
      "version": 2,
      "builds": [
        {
          "src": "run.py",
          "use": "@vercel/python"
        }
      ],
      "routes": [
        {
          "src": "/(.*)",
          "dest": "run.py"
        }
      ],
      "env": {
        "FLASK_ENV": "production"
      }
    }
    ```

3.  **部署到 Vercel**:
    ```bash
    vercel
    # 設定環境變數
    vercel env add DATABASE_URL
    vercel env add SECRET_KEY
    # 重新部署
    vercel --prod
    ```

**選項 B: 部署到 Netlify**

1.  **建立 `netlify.toml`**:
    ```toml
    [build]
      command = "pip install -r requirements.txt"
      functions = "netlify/functions"
      publish = "app/static"

    [[redirects]]
      from = "/api/*"
      to = "/.netlify/functions/app/:splat"
      status = 200
    ```

2.  **使用 Netlify 部署**

**選項 C: 繼續使用 Heroku (只是改用 Supabase 資料庫)**

1.  **更新 Heroku 環境變數**:
    ```bash
    heroku config:set DATABASE_URL="your-supabase-database-url"
    ```

2.  **重新部署**:
    ```bash
    git push heroku main
    ```

### 8.9 Supabase 進階功能 (可選)

**即時資料同步 (Real-time)**

1.  **啟用資料表的即時功能**:
    *   在 Supabase Dashboard > Database > Replication
    *   為 `subscriptions` 表格開啟 Realtime

2.  **在前端使用 Supabase JavaScript Client**:
    ```bash
    npm install @supabase/supabase-js
    ```

**Row Level Security (RLS)**

1.  **啟用 RLS**:
    ```sql
    ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
    ALTER TABLE app_settings ENABLE ROW LEVEL SECURITY;
    ```

2.  **建立政策** (可選，未來加入使用者認證時使用):
    ```sql
    CREATE POLICY "Allow public read access" ON subscriptions
      FOR SELECT TO public USING (true);

    CREATE POLICY "Allow public write access" ON subscriptions
      FOR ALL TO public USING (true);
    ```

### 8.10 監控與管理

1.  **查看資料庫使用量**:
    *   在 Supabase Dashboard > Settings > Usage

2.  **資料庫備份**:
    *   在 Supabase Dashboard > Settings > Database
    *   點擊「Download backup」

3.  **查看日誌**:
    *   在 Supabase Dashboard > Logs

4.  **SQL 查詢**:
    *   使用 SQL Editor 直接執行查詢

### 8.11 驗證部署

1.  **測試資料庫連線**:
    ```bash
    python -c "
    from app import create_app, db
    app = create_app()
    with app.app_context():
        result = db.session.execute('SELECT version()')
        print('PostgreSQL 版本:', result.fetchone()[0])
    "
    ```

2.  **測試 API 端點**:
    *   本地測試：`http://localhost:5000/api/settings`
    *   部署後測試：`https://your-app.vercel.app/api/settings`

3.  **檢查資料完整性**:
    *   在 Supabase Dashboard > Table Editor 中查看資料

### 8.12 Supabase vs Heroku PostgreSQL 比較

| 功能 | Supabase | Heroku PostgreSQL |
|------|----------|-------------------|
| 免費額度 | 500MB + 額外功能 | 10,000 rows 限制 |
| 管理介面 | 優秀的 Web Dashboard | 基本的 CLI 工具 |
| 即時功能 | 內建 Realtime | 需自行實作 |
| 備份 | 自動備份 + 手動下載 | 需付費計畫 |
| API | 自動生成 REST API | 需自行建立 |
| 認證 | 內建使用者認證 | 需整合第三方 |
| 部署相容性 | 適合 Vercel/Netlify | 專為 Heroku 優化 |

**Supabase 的優勢**：
- 更慷慨的免費額度
- 優秀的開發者體驗
- 內建許多現代化功能
- 與 JAMstack 部署平台整合良好

完成以上步驟後，您的 StarBaBa 應用程式就成功整合 Supabase PostgreSQL 並可部署到各種平台了！ 