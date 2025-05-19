from flask import Blueprint, jsonify, request, render_template, current_app
from . import models
from .services import calculate_statistics

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/api/settings', methods=['GET'])
def get_settings_api():
    settings = models.get_settings()
    if not settings: # 雖然 models.get_settings() 現在有預設值，但保留此檢查以防萬一
        current_app.logger.warning("Settings could not be loaded from the database or default settings are empty.")
        return jsonify({ "error": "Application settings are currently unavailable." }), 500
    return jsonify(settings)

@main_bp.route('/api/subscriptions', methods=['GET'])
def get_subscriptions_api():
    current_app.logger.info("API endpoint /api/subscriptions (GET) called.")
    subscriptions = models.get_all_subscriptions()
    current_app.logger.info(f"Data received from models.get_all_subscriptions: {len(subscriptions)} items.")
    if isinstance(subscriptions, list):
        current_app.logger.info(f"First item if exists: {subscriptions[0] if subscriptions else 'None'}")
    else:
        current_app.logger.warning(f"Data from models is not a list: {type(subscriptions)}")
    return jsonify(subscriptions)

@main_bp.route('/api/subscriptions', methods=['POST'])
def add_subscription_api():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    
    # 這裡可以加入更詳細的欄位驗證
    required_fields = ['serviceName', 'price', 'currency', 'billingCycle', 'startDate']
    for field in required_fields:
        if field not in data or data[field] == '': # 也檢查空字串
            return jsonify({"error": f"Missing or empty required field: {field}"}), 400
    
    try:
        # 確保 price 是數字
        data['price'] = float(data['price'])
    except ValueError:
        return jsonify({"error": "Price must be a valid number"}), 400
    
    # isActive 預設值處理
    if 'isActive' not in data:
        data['isActive'] = True # 預設為啟用
        
    new_subscription = models.add_subscription(data)
    if new_subscription:
        return jsonify(new_subscription), 201
    else:
        # 如果 add_subscription 可能因為某些原因 (例如資料庫錯誤但未引發異常) 回傳 None
        return jsonify({"error": "Failed to create subscription."}), 500

@main_bp.route('/api/subscriptions/<string:subscription_id>', methods=['GET'])
def get_subscription_api(subscription_id):
    subscription = models.get_subscription_by_id(subscription_id)
    if subscription:
        return jsonify(subscription)
    return jsonify({"error": "Subscription not found"}), 404

@main_bp.route('/api/subscriptions/<string:subscription_id>', methods=['PUT'])
def update_subscription_api(subscription_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    # 移除 routes.py 中的 price 轉換，讓模型層處理或依賴 SQLAlchemy 的類型轉換
    # if 'price' in data:
    #     try:
    #         data['price'] = float(data['price'])
    #     except ValueError:
    #         return jsonify({"error": "Price must be a valid number"}), 400
            
    updated_subscription = models.update_subscription(subscription_id, data)
    if updated_subscription:
        return jsonify(updated_subscription)
    # 根據 models.update_subscription 的回傳邏輯，它在找不到或失敗時回傳 None
    return jsonify({"error": "Subscription not found or update failed"}), 404

@main_bp.route('/api/subscriptions/<string:subscription_id>', methods=['DELETE'])
def delete_subscription_api(subscription_id):
    if models.delete_subscription(subscription_id):
        return '', 204 # 成功刪除，回傳 204 No Content
    return jsonify({"error": "Subscription not found or delete failed"}), 404

@main_bp.route('/api/stats', methods=['GET'])
def get_stats_api():
    subscriptions = models.get_all_subscriptions()
    settings = models.get_settings()
    
    if not settings or 'equivalencyItems' not in settings or 'defaultCurrency' not in settings:
        current_app.logger.error("Stats calculation failed: settings.json is missing or incomplete.")
        # 提供更具體的錯誤訊息給前端可能會更好，但也要注意不要洩漏過多內部細節
        return jsonify({"error": "Application settings for statistics calculation are missing or incomplete. Please check server logs."}), 500
        
    # 呼叫 services.py 中的 calculate_statistics 函式
    stats = calculate_statistics(subscriptions, settings)
    
    return jsonify(stats) 