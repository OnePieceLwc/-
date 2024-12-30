import os

class Config:
    # 指定数据库文件的绝对路径
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'digital_economy_risk.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 安全配置
    SECRET_KEY = 'dev-key-123456'
    
    # 风险监控配置
    RISK_THRESHOLD = 0.75
    ALERT_EMAIL = 'admin@example.com' 