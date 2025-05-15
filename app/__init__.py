import os
from flask import Flask
from dotenv import load_dotenv
from datetime import datetime
import logging # 新增 logging 模組

def create_app():
    load_dotenv() # 自動從 .env 檔案載入環境變數

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    # 你可以在這裡加入其他的應用程式設定，例如:
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    # 設定日誌級別為 INFO
    if not app.debug: # 只有在非 debug 模式下才特別設定，debug 模式通常已經夠詳細
        # 或者即使是 debug 模式也強制設定，確保 INFO 訊息出現
        # app.logger.setLevel(logging.INFO) # 方法一：直接設定 app.logger
        
        # 方法二：設定更通用的 handler (推薦)
        # 移除預設的 handler，如果有的話 (通常 flask run 會自己加 handler)
        # for handler in app.logger.handlers[:]: 
        #     app.logger.removeHandler(handler)
        
        # 設定日誌格式和級別
        # stdout_handler = logging.StreamHandler()
        # stdout_handler.setFormatter(logging.Formatter(
        #     '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        # stdout_handler.setLevel(logging.INFO)
        # app.logger.addHandler(stdout_handler)
        app.logger.setLevel(logging.INFO) # 簡化處理，直接設定 app.logger 的級別

    # 確保 data 目錄存在
    data_dir = os.path.join(app.root_path, '..', 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # 確保 subscriptions.json 和 settings.json 存在
    subscriptions_file = os.path.join(data_dir, 'subscriptions.json')
    settings_file = os.path.join(data_dir, 'settings.json')

    # REMOVED: 不再自動創建空的 subscriptions.json，以防止意外覆寫
    # if not os.path.exists(subscriptions_file):
    #     with open(subscriptions_file, 'w', encoding='utf-8') as f:
    #         f.write('[]') 
            
    if not os.path.exists(settings_file):
        # 你可以選擇在此處填入一個預設的 settings.json 結構，以防檔案遺失
        # 但根據我們的流程，它應該已經由使用者或之前的步驟建立
        # 為了安全起見，也暫不自動創建空的 settings.json
        current_app.logger.warning(f"Settings file {settings_file} not found. Application might not work as expected.")
        # pass 

    # 上下文處理器，注入目前年份
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.utcnow().year}

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app 