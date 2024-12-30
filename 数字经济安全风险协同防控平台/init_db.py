from app import create_app, db
from app.models import User, RiskEvent
import random

def init_db():
    app = create_app()
    with app.app_context():
        print("开始初始化数据库...")
        
        # 确保instance目录存在
        import os
        os.makedirs('instance', exist_ok=True)
        
        # 清空数据库
        db.drop_all()
        db.create_all()
        print("数据库表创建成功")
        
        # 创建管理员用户
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('123456')
        db.session.add(admin)
        print("管理员用户创建成功")
        
        # 创建测试用户
        test_user = User(username='test', email='test@example.com', role='user')
        test_user.set_password('123456')
        db.session.add(test_user)
        print("测试用户创建成功")
        
        try:
            db.session.commit()
            print("用户数据保存成功")
            
            # 创建示例风险事件
            risk_types = ['data_leak', 'network_attack', 'system_vulnerability', 
                         'unauthorized_access', 'compliance_risk']
            
            for i in range(10):
                event = RiskEvent(
                    title=f"测试风险事件 {i+1}",
                    risk_type=random.choice(risk_types),
                    description=f"这是一个测试风险事件描述 {i+1}",
                    risk_level=random.uniform(0.1, 0.9),
                    reporter_id=admin.id,
                    status='pending'
                )
                event.set_affected_systems(['core_system', 'business_system'])
                db.session.add(event)
            
            db.session.commit()
            print("示例数据创建成功")
            
        except Exception as e:
            print(f"错误：{e}")
            db.session.rollback()
            return
        
        print("数据库初始化完成！")

if __name__ == '__main__':
    init_db() 