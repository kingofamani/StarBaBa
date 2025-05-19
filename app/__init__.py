import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
import logging

# 初始化 SQLAlchemy 實例，但不與特定 app 綁定
db = SQLAlchemy()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    
    # 從環境變數讀取資料庫URI
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 建議設定為 False 以節省資源

    # 初始化 db 並與 app 綁定
    db.init_app(app)

    # 設定日誌級別為 INFO
    if not app.debug:
        app.logger.setLevel(logging.INFO)

    # 移除 data 目錄和 JSON 檔案檢查的邏輯，因為資料將由資料庫管理
    # # 確保 data 目錄存在
    # data_dir = os.path.join(app.root_path, '..', 'data')
    # if not os.path.exists(data_dir):
    #     os.makedirs(data_dir)
    # 
    # # 確保 subscriptions.json 和 settings.json 存在
    # subscriptions_file = os.path.join(data_dir, 'subscriptions.json')
    # settings_file = os.path.join(data_dir, 'settings.json')
    # 
    # if not os.path.exists(subscriptions_file):
    #     # ... (原有邏輯)
    #         
    # if not os.path.exists(settings_file):
    #     # ... (原有邏輯)
    #     current_app.logger.warning(f"Settings file {settings_file} not found. Application might not work as expected.")

    # 上下文處理器，注入目前年份
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.utcnow().year}

    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    # (可選) 建立資料庫表格，如果它們還不存在的話
    # 考量到遷移工具 (如 Flask-Migrate) 通常是更好的選擇，這裡先註解掉
    # with app.app_context():
    #     db.create_all()

    return app 