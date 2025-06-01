# StarBaBa - 個人訂閱管理系統

一個現代化的個人訂閱管理 Web 應用程式，幫助您追蹤和管理各種訂閱服務。

## ✨ 功能特性 (MVP)

- **訂閱追蹤**: 記錄您的所有訂閱服務，包括服務名稱、開始日期、價格、付款週期等。
- **花費管理**: 清晰了解您在各項訂閱上的支出。
- **商品換算**: 將您的月度或年度訂閱總支出，換算成等值的日常商品 (例如：相當於多少杯星巴克、多少個大麥克)，讓支出更有感！
- **標籤分類**: 為您的訂閱加上標籤，方便分類與篩選。
- **簡易操作**: 直觀的介面，輕鬆新增、編輯、刪除訂閱項目。
- **設定彈性**: 可自訂預設服務、標籤、貨幣、商品換算項目等。

## 🛠️ 技術棧

- **後端**: Flask (Python)
- **資料庫**: PostgreSQL (SQLAlchemy ORM)
- **前端**: HTML5, TailwindCSS, JavaScript
- **部署**: Heroku

## 🚀 環境設定

### 先決條件
- Python 3.8+
- PostgreSQL 15+
- Node.js (用於 TailwindCSS)

### 安裝依賴
```bash
pip install -r requirements.txt
```

### 資料庫設定

#### 方案 A：本地 PostgreSQL
1. 安裝 PostgreSQL
2. 建立資料庫：
```sql
CREATE DATABASE starbaba;
CREATE USER starbaba_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE starbaba TO starbaba_user;
```

3. 設定環境變數：
```bash
# 方案 A: 本地資料庫
$env:DATABASE_URL="postgresql://starbaba_user:your_password@localhost:5432/starbaba"

# 或方案 B: Supabase 遠程
$env:DATABASE_URL="postgresql://postgres:password@host:5432/postgres"
```

#### 方案 B：Supabase 本地開發
```bash
# 啟動本地 Supabase (如果 Docker 問題解決)
supabase start

# 檢查狀態
supabase status
```

### 初始化資料庫
```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

### 啟動應用程式
```bash
python app.py
```

## 🧪 測試

### 資料庫連接測試
```bash
python test_db.py
```

### 連接問題診斷
```bash
python test_connection.py
```

### API 測試 (curl 指令)

#### 取得設定
```bash
curl http://localhost:5000/api/settings
```

#### 更新設定
```bash
curl -X POST http://localhost:5000/api/settings \
  -H "Content-Type: application/json" \
  -d '{"monthlyBudget": 1000, "currency": "TWD"}'
```

#### 新增訂閱
```bash
curl -X POST http://localhost:5000/api/subscriptions \
  -H "Content-Type: application/json" \
  -d '{
    "serviceName": "Netflix",
    "cost": 390,
    "billingCycle": "monthly",
    "category": "Entertainment"
  }'
```

#### 取得所有訂閱
```bash
curl http://localhost:5000/api/subscriptions
```

#### 更新訂閱
```bash
curl -X PUT http://localhost:5000/api/subscriptions/{id} \
  -H "Content-Type: application/json" \
  -d '{
    "serviceName": "Netflix Premium",
    "cost": 490,
    "isActive": true
  }'
```

#### 刪除訂閱
```bash
curl -X DELETE http://localhost:5000/api/subscriptions/{id}
```

## 🔧 故障排除

### Docker/Supabase 問題
```bash
# 清理 Docker
docker system prune -f
docker rm -f $(docker ps -aq --filter "label=com.supabase.cli.project=StarBaBa")

# 重啟 Supabase
supabase stop
supabase start
```

### 網路連接問題
```bash
# 測試 DNS 解析
nslookup your-supabase-host.supabase.co

# 測試連接
telnet your-supabase-host.supabase.co 5432
```

## 🗂️ 專案結構 (概覽)

```
StarBaBa/
├── app/
│   ├── __init__.py          # Flask 應用程式初始化
│   ├── models.py            # SQLAlchemy 資料模型
│   ├── routes.py            # API 路由
│   ├── static/              # 靜態檔案 (CSS, JS)
│   └── templates/           # HTML 模板
├── requirements.txt         # Python 依賴
├── test_db.py              # 資料庫測試
├── test_connection.py      # 連接測試
└── app.py                  # 應用程式入口點
```

## 核心功能

- ✅ 訂閱服務管理 (CRUD)
- ✅ 月度預算追蹤
- ✅ 費用計算和統計
- ✅ PostgreSQL 資料持久化
- ✅ RESTful API
- ⚠️ 分類管理 (進行中)
- 🔄 通知系統 (計劃中)
- 🔄 數據分析 (計劃中)

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