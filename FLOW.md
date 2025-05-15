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
        *   **後端 (`app/models.py`)**: 讀取 `data/settings.json` 檔案內容。
        *   **後端**: 將 `settings.json` 內容以 JSON 格式回傳。
        *   **前端 (`main.js`)**: 收到設定資料，用於後續填充表單下拉選單 (例如：貨幣、標籤、預設服務等)。
    *   **非同步請求訂閱**: 發送 `GET /api/subscriptions` 請求。
        *   **後端 (`app/routes.py`)**: 處理 `/api/subscriptions`，呼叫 `app/models.py` 中的 `get_all_subscriptions()` 函式。
        *   **後端 (`app/models.py`)**: 讀取 `data/subscriptions.json` 檔案內容。
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
    *   為新的訂閱記錄生成一個唯一的 `id` (例如使用 `uuid.uuid4()`)。
    *   設定 `createdAt` 和 `updatedAt` 時間戳。
    *   將新的訂閱物件添加到從 `subscriptions.json` 讀取的現有訂閱列表中。
    *   將更新後的訂閱列表寫回 `data/subscriptions.json` 檔案。
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
    *   根據 `id` 找到對應的訂閱記錄。
    *   更新該記錄的欄位值。
    *   更新 `updatedAt` 時間戳。
    *   將更新後的訂閱列表寫回 `data/subscriptions.json`。
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
    *   根據 `id` 從訂閱列表中移除對應的記錄。
    *   將更新後的訂閱列表寫回 `data/subscriptions.json`。
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
    *   所有訂閱項目: 從 `/api/subscriptions` 獲取，或從前端 `main.js` 維護的當前訂閱列表獲取。
    *   商品換算設定: 從 `/api/settings` 獲取的 `equivalencyItems` 和 `defaultCurrency`。
3.  **計算邏輯 (`main.js` 請求 `/api/stats`，後端在 `app/routes.py` 中計算)**:
    *   篩選 `isActive: true` 的訂閱項目。
    *   根據 `billingCycle` 和 `price` 計算總月費和總年費 (需要將不同週期的費用統一轉換，例如年繳費用除以12得到月費)。
    *   (MVP階段假設所有訂閱和商品都是 `defaultCurrency`，未來可擴展貨幣轉換)。
    *   遍歷 `equivalencyItems`，用計算出的總花費 (例如總月費) 除以每個商品的 `price`，得到可換算的商品數量。
4.  **前端 (`main.js`)**: 將計算出的總月費、總年費以及各商品的換算數量更新到 `index.html` 中指定的統計區域。 