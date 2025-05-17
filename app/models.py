import json
import uuid
from datetime import datetime, timezone
import os
from flask import current_app

# Calculate absolute paths to data files
MODEL_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# Navigates up from 'app' dir (where models.py is) to project root, then into 'data'
PROJECT_ROOT_DIR = os.path.join(MODEL_FILE_DIR, '..')
DATA_DIR = os.path.join(PROJECT_ROOT_DIR, 'data')

SUBSCRIPTIONS_FILE = os.path.join(DATA_DIR, 'subscriptions.json')
SETTINGS_FILE = os.path.join(DATA_DIR, 'settings.json')

# def _ensure_data_files_exist():
#     """確保資料目錄存在。不再自動創建或覆寫資料檔案。"""
#     # if not os.path.exists(DATA_DIR):
#     #     current_app.logger.info(f"Data directory {DATA_DIR} not found. Creating it.")
#     #     os.makedirs(DATA_DIR)
    
#     # REMOVED: 不再自動創建空的 subscriptions.json
#     # if not os.path.exists(SUBSCRIPTIONS_FILE):
#     #     current_app.logger.warning(f"Subscriptions file {SUBSCRIPTIONS_FILE} not found. An empty one would have been created.")
#         # with open(SUBSCRIPTIONS_FILE, 'w', encoding='utf-8') as f:
#         #     json.dump([], f, ensure_ascii=False, indent=2)
            
#     # REMOVED: 不再自動創建空的 settings.json
#     # if not os.path.exists(SETTINGS_FILE):
#     #     current_app.logger.warning(f"Settings file {SETTINGS_FILE} not found. A default one would have been created.")
#         # default_settings = {"appName": "StarBaBa", "defaultCurrency": "TWD", "equivalencyItems": []}
#         # with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
#         #     json.dump(default_settings, f, ensure_ascii=False, indent=2)

# _ensure_data_files_exist() # 模組載入時即確保資料目錄存在

def get_settings():
    """讀取 settings.json 的內容。"""
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        current_app.logger.error(f"{SETTINGS_FILE} not found. Returning empty settings.")
        return {}
    except json.JSONDecodeError:
        current_app.logger.error(f"Error decoding {SETTINGS_FILE}. Returning empty settings.")
        return {}

def get_all_subscriptions():
    """讀取 subscriptions.json 的所有訂閱項目。"""
    current_app.logger.info(f"Attempting to read subscriptions from: {SUBSCRIPTIONS_FILE}")
    try:
        with open(SUBSCRIPTIONS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            current_app.logger.info(f"Successfully loaded {len(data)} subscriptions from file.")
            return data
    except FileNotFoundError:
        current_app.logger.error(f"{SUBSCRIPTIONS_FILE} not found. Returning empty list.")
        return []
    except json.JSONDecodeError:
        current_app.logger.error(f"Error decoding {SUBSCRIPTIONS_FILE}. Returning empty list.")
        return []
    except Exception as e:
        current_app.logger.error(f"An unexpected error occurred in get_all_subscriptions: {e}")
        return []

def get_subscription_by_id(subscription_id):
    """根據 ID 獲取指定的訂閱項目。"""
    subscriptions = get_all_subscriptions()
    for sub in subscriptions:
        if sub.get('id') == subscription_id:
            return sub
    return None

def add_subscription(new_subscription_data):
    """新增一個訂閱項目到 JSON 檔案中。"""
    subscriptions = get_all_subscriptions() # 取得現有列表
    
    # 為新訂閱項目準備資料
    # 確保所有前端傳來的欄位都存在於 new_item 中，即使是空值
    # 同時自動產生 id, createdAt, updatedAt
    new_item = {
        "id": str(uuid.uuid4()), # 自動產生 ID
        "createdAt": datetime.now(timezone.utc).isoformat(), # 自動產生建立時間
        "updatedAt": datetime.now(timezone.utc).isoformat(), # 自動產生更新時間
        "serviceName": new_subscription_data.get("serviceName"),
        "serviceIcon": new_subscription_data.get("serviceIcon", ""), # 提供預設空字串
        "startDate": new_subscription_data.get("startDate"),
        "billingCycle": new_subscription_data.get("billingCycle"),
        "price": new_subscription_data.get("price"),
        "currency": new_subscription_data.get("currency"),
        "paymentMethod": new_subscription_data.get("paymentMethod", ""), # 提供預設空字串
        "notes": new_subscription_data.get("notes", ""), # 提供預設空字串
        "tags": new_subscription_data.get("tags", []), # 提供預設空列表
        "isActive": new_subscription_data.get("isActive", True), # 預設為 True
        "billingDetails": new_subscription_data.get("billingDetails", {}), # 提供預設空字典
        "paymentDetails": new_subscription_data.get("paymentDetails", {}) # 提供預設空字典
    }

    subscriptions.append(new_item)
    
    try:
        with open(SUBSCRIPTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(subscriptions, f, indent=2, ensure_ascii=False)
        current_app.logger.info(f"New subscription added: {new_item.get('serviceName')}, ID: {new_item.get('id')}")
        return new_item # 回傳新增的項目，包含產生的 id
    except IOError as e:
        current_app.logger.error(f"Error writing to subscriptions file {SUBSCRIPTIONS_FILE}: {e}")
        return None # 或引發自訂異常
    except Exception as e: # 捕捉其他可能的錯誤
        current_app.logger.error(f"An unexpected error occurred in add_subscription: {e}")
        return None

def update_subscription(subscription_id, data):
    """更新指定 ID 的訂閱項目。"""
    subscriptions = get_all_subscriptions()
    for i, sub in enumerate(subscriptions):
        if sub.get('id') == subscription_id:
            now = datetime.now(timezone.utc).isoformat()
            # 保留原始的 createdAt，只更新 updatedAt 和其他資料
            original_created_at = sub.get('createdAt')
            subscriptions[i].update(data) 
            subscriptions[i]['updatedAt'] = now
            if original_created_at: # 確保 createdAt 不會被 data 中的 updatedAt 覆蓋
                 subscriptions[i]['createdAt'] = original_created_at
            if 'id' in data and data['id'] != subscription_id: # 防止 ID 被意外修改
                subscriptions[i]['id'] = subscription_id
            else:
                 subscriptions[i]['id'] = subscription_id # 確保 ID 欄位存在

            with open(SUBSCRIPTIONS_FILE, 'w', encoding='utf-8') as f:
                json.dump(subscriptions, f, ensure_ascii=False, indent=2)
            return subscriptions[i]
    return None

def delete_subscription(subscription_id):
    """刪除指定 ID 的訂閱項目。"""
    subscriptions = get_all_subscriptions()
    original_length = len(subscriptions)
    subscriptions = [sub for sub in subscriptions if sub.get('id') != subscription_id]
    if len(subscriptions) < original_length:
        with open(SUBSCRIPTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(subscriptions, f, ensure_ascii=False, indent=2)
        return True
    return False 