from datetime import datetime, timezone, date
from app import db # 從 app/__init__.py 導入 db 實例
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID # Renamed to avoid confusion
import uuid as py_uuid
from sqlalchemy import func # For server_default and onupdate

# Settings Model
# settings.json 是一個單一物件，我們將其儲存在一個名為 'app_settings' 的表中，
# 並且始終只有一條記錄 (或使用 key-value 方式儲存每個設定)。
# 為了簡單起見，先用一個 JSONB 欄位儲存整個 settings 物件。
class Settings(db.Model):
    __tablename__ = 'app_settings'
    id = db.Column(db.Integer, primary_key=True) # Matches SERIAL PRIMARY KEY
    settings_data = db.Column(JSONB, nullable=False) # Matches settings_data JSONB NOT NULL
    last_updated = db.Column(db.DateTime(timezone=True), 
                             server_default=func.current_timestamp(), # Matches DEFAULT CURRENT_TIMESTAMP
                             onupdate=func.current_timestamp(), # For ORM updates
                             nullable=False) # Assuming last_updated should not be null based on default

    def __repr__(self):
        return f"<Settings {self.id}>"

# Subscription Model
class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(PG_UUID(as_uuid=True), primary_key=True, default=py_uuid.uuid4) # Matches id UUID PRIMARY KEY DEFAULT uuid_generate_v4()
    service_name = db.Column(db.String(255), nullable=False) # Matches service_name VARCHAR(255) NOT NULL
    service_icon = db.Column(db.String(255), nullable=True) # Matches service_icon VARCHAR(255)
    tags = db.Column(JSONB, nullable=True, server_default='[]') # Matches tags JSONB DEFAULT '[]'::jsonb
    start_date = db.Column(db.Date, nullable=True) # Matches start_date DATE
    billing_cycle = db.Column(db.String(50), nullable=False) # Matches billing_cycle VARCHAR(50) NOT NULL
    billing_details = db.Column(JSONB, nullable=True) # Matches billing_details JSONB
    price = db.Column(db.Numeric(10, 2), nullable=False) # Matches price NUMERIC(10, 2) NOT NULL
    currency = db.Column(db.String(10), nullable=False) # Matches currency VARCHAR(10) NOT NULL
    notes = db.Column(db.Text, nullable=True) # Matches notes TEXT
    payment_method = db.Column(db.String(50), nullable=True) # Matches payment_method VARCHAR(50)
    payment_details = db.Column(JSONB, nullable=True) # Matches payment_details JSONB
    is_active = db.Column(db.Boolean, default=True, nullable=False) # Matches is_active BOOLEAN NOT NULL DEFAULT TRUE
    
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.current_timestamp()) # Matches created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp()) # Matches updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP. DB trigger will also handle this.

    def __repr__(self):
        return f"<Subscription '{self.service_name}'>"

    def to_dict(self):
        """將 Subscription 物件轉換為字典，API 預期 camelCase。"""
        return {
            'id': str(self.id),
            'serviceName': self.service_name,
            'serviceIcon': self.service_icon,
            'startDate': self.start_date.isoformat() if self.start_date else None,
            'billingCycle': self.billing_cycle,
            'price': str(self.price) if self.price is not None else None,
            'currency': self.currency,
            'paymentMethod': self.payment_method,
            'notes': self.notes,
            'tags': self.tags,
            'isActive': self.is_active,
            'billingDetails': self.billing_details,
            'paymentDetails': self.payment_details,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }

# --- Data Access Functions ---

def get_settings():
    """從資料庫讀取應用程式設定。"""
    settings_record = db.session.query(Settings).first()
    if settings_record:
        return settings_record.settings_data
    return {"appName": "StarBaBa (Default from Model)", "defaultCurrency": "USD", "equivalencyItems": []}


def update_settings(new_settings_data):
    """更新或創建應用程式設定。"""
    settings_record = db.session.query(Settings).first()
    if settings_record:
        settings_record.settings_data = new_settings_data
    else:
        settings_record = Settings(settings_data=new_settings_data)
        db.session.add(settings_record)
    db.session.commit()
    return settings_record.settings_data


def get_all_subscriptions():
    """從資料庫讀取所有訂閱項目。"""
    subscriptions = db.session.query(Subscription).all()
    return [sub.to_dict() for sub in subscriptions]

def get_subscription_by_id(subscription_id_str):
    """根據 ID 獲取指定的訂閱項目。"""
    try:
        sub_id_uuid = py_uuid.UUID(subscription_id_str)
    except ValueError:
        return None 
    
    subscription = db.session.query(Subscription).get(sub_id_uuid)
    return subscription.to_dict() if subscription else None

def add_subscription(data):
    """新增一個訂閱項目到資料庫中。API 使用 camelCase。"""
    start_date_obj = None
    if data.get('startDate'):
        try:
            start_date_obj = date.fromisoformat(data.get('startDate'))
        except ValueError:
            # Handle invalid date format if necessary, or let it be None
            pass

    new_sub = Subscription(
        service_name=data.get('serviceName'),
        service_icon=data.get('serviceIcon'),
        start_date=start_date_obj,
        billing_cycle=data.get('billingCycle'),
        price=data.get('price'), 
        currency=data.get('currency'),
        payment_method=data.get('paymentMethod'),
        notes=data.get('notes'),
        tags=data.get('tags', []),
        is_active=data.get('isActive', True),
        billing_details=data.get('billingDetails', {}),
        payment_details=data.get('paymentDetails', {})
    )
    db.session.add(new_sub)
    db.session.commit()
    return new_sub.to_dict()

def update_subscription(subscription_id_str, data):
    """更新指定 ID 的訂閱項目。API 使用 camelCase。"""
    try:
        sub_id_uuid = py_uuid.UUID(subscription_id_str)
    except ValueError:
        return None
        
    sub = db.session.query(Subscription).get(sub_id_uuid)
    if not sub:
        return None

    if 'serviceName' in data:
        sub.service_name = data['serviceName']
    if 'serviceIcon' in data:
        sub.service_icon = data['serviceIcon']
    if data.get('startDate'):
        try:
            sub.start_date = date.fromisoformat(data.get('startDate'))
        except ValueError:
            pass # Or handle error
    if 'billingCycle' in data:
        sub.billing_cycle = data['billingCycle']
    if data.get('price') is not None:
        sub.price = data['price']
    if 'currency' in data:
        sub.currency = data['currency']
    if 'paymentMethod' in data:
        sub.payment_method = data['paymentMethod']
    if 'notes' in data:
        sub.notes = data['notes']
    if 'tags' in data:
        sub.tags = data['tags']
    if 'isActive' in data:
        sub.is_active = data['isActive']
    if 'billingDetails' in data:
        sub.billing_details = data['billingDetails']
    if 'paymentDetails' in data:
        sub.payment_details = data['paymentDetails']
    
    db.session.commit()
    return sub.to_dict()

def delete_subscription(subscription_id_str):
    """刪除指定 ID 的訂閱項目。"""
    try:
        sub_id_uuid = py_uuid.UUID(subscription_id_str)
    except ValueError:
        return False
        
    sub = db.session.query(Subscription).get(sub_id_uuid)
    if sub:
        db.session.delete(sub)
        db.session.commit()
        return True
    return False 