import json
import uuid
from datetime import datetime, timezone
import os
from flask import current_app

# DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
# SUBSCRIPTIONS_FILE = os.path.join(DATA_DIR, 'subscriptions.json')
# SETTINGS_FILE = os.path.join(DATA_DIR, 'settings.json')

# --- 使用絕對路徑進行測試 ---
# 注意：在 Python 字串中，反斜線需要跳脫，所以用 '\\' 或 r"..."
SUBSCRIPTIONS_FILE = r"C:\D\Vibe\StarBaBa\data\subscriptions.json"
SETTINGS_FILE = r"C:\D\Vibe\StarBaBa\data\settings.json"
# --- END 絕對路徑測試 ---

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

def add_subscription(data):
    """新增一個訂閱項目。"""
    subscriptions = get_all_subscriptions()
    now = datetime.now(timezone.utc).isoformat()
    new_subscription = {
        "id": str(uuid.uuid4()),
        "createdAt": now,
        "updatedAt": now
    }
    new_subscription.update(data)
    subscriptions.append(new_subscription)
    with open(SUBSCRIPTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(subscriptions, f, ensure_ascii=False, indent=2)
    return new_subscription

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