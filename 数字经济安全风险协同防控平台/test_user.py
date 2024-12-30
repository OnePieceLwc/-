from app import create_app, db
from app.models import User

def test_users():
    app = create_app()
    with app.app_context():
        # 测试管理员用户
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("管理员用户存在")
            print(f"用户名: {admin.username}")
            print(f"邮箱: {admin.email}")
            print(f"角色: {admin.role}")
            print("密码验证测试:", admin.check_password('123456'))
        else:
            print("错误：管理员用户不存在")
        
        # 测试普通用户
        test = User.query.filter_by(username='test').first()
        if test:
            print("\n测试用户存在")
            print(f"用户名: {test.username}")
            print(f"邮箱: {test.email}")
            print(f"角色: {test.role}")
            print("密码验证测试:", test.check_password('123456'))
        else:
            print("错误：测试用户不存在")

if __name__ == '__main__':
    test_users() 