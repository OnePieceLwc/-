# 数字经济安全风险协同防控平台

## 项目简介
基于 Flask 的数字经济安全风险协同防控平台，提供风险事件的上报、监控和管理功能。系统支持多用户协同操作，实时监控风险态势，并提供直观的数据可视化界面。

## 运行说明

### 环境要求
- Python 3.7+
- pip 包管理工具

### 安装步骤
1. 克隆项目到本地
2. 安装依赖包：
```
bash
pip install -r requirements.txt
```

3. 初始化数据库：
```
bash
python init_db.py
```
4. 启动应用：
```
bash
python run.py
```
5. 访问系统：
- 打开浏览器访问：http://localhost:5000
- 默认管理员账号：admin/123456
- 测试用户账号：test/123456

## 项目结构
```
├── app/ # 应用主目录
│ ├── init.py # 应用初始化
│ ├── models.py # 数据模型
│ ├── routes/ # 路由目录
│ │ ├── auth.py # 认证相关路由
│ │ ├── main.py # 主要页面路由
│ │ ├── risk.py # 风险管理路由
│ │ └── risk_monitor.py # 风险监控路由
│ └── templates/ # 模板目录
│ ├── base.html # 基础模板
│ ├── index.html # 首页
│ ├── login.html # 登录页
│ ├── register.html # 注册页
│ ├── dashboard.html # 数据看板
│ ├── risk_list.html # 风险列表
│ └── risk_report.html # 风险上报
├── config.py # 配置文件
├── init_db.py # 数据库初始化脚本
└── run.py # 应用启动脚本
```

## 注意事项

1. 数据库相关：
   - 使用 SQLite 数据库，数据库文件位于 instance 目录
   - 首次运行必须执行 init_db.py 初始化数据库
   - 请定期备份数据库文件

2. 安全配置：
   - 生产环境部署时请修改 config.py 中的密钥
   - 建议配置 HTTPS
   - 定期更新系统和依赖包

3. 使用建议：
   - 推荐使用 Chrome、Firefox、Edge 等现代浏览器
   - 建议使用虚拟环境运行项目
   - 定期检查日志文件

## 技术支持
如遇到问题，请联系系统管理员lucianaib或提交 Issue。

