from flask import Blueprint, render_template
from flask_login import login_required
from app.models import RiskEvent
from datetime import datetime, timedelta

# 创建蓝图
bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    # 获取风险统计数据
    high_risk_count = RiskEvent.query.filter(RiskEvent.risk_level >= 0.7).count()
    medium_risk_count = RiskEvent.query.filter(RiskEvent.risk_level.between(0.3, 0.7)).count()
    low_risk_count = RiskEvent.query.filter(RiskEvent.risk_level < 0.3).count()
    
    # 获取最新预警
    latest_alerts = RiskEvent.query.order_by(RiskEvent.timestamp.desc()).limit(5).all()
    
    return render_template('index.html',
                         high_risk_count=high_risk_count,
                         medium_risk_count=medium_risk_count,
                         low_risk_count=low_risk_count,
                         latest_alerts=latest_alerts)

@bp.route('/dashboard')
@login_required
def dashboard():
    # 模拟数据
    data = {
        'total_risks': 2547,
        'active_risks': 183,
        'risk_rate': 92.5,
        'avg_response': 15,
        'latest_events': [
            {
                'time': '10:24:35',
                'type': '数据泄露',
                'description': '检测到敏感数据异常访问'
            },
            {
                'time': '10:15:22',
                'type': '网络攻击',
                'description': 'DDoS攻击预警'
            },
            {
                'time': '10:05:18',
                'type': '系统漏洞',
                'description': '发现高危系统漏洞'
            },
            # 添加更多实时事件...
        ]
    }
    return render_template('dashboard.html', **data)

@bp.route('/risk-report')
@login_required
def risk_report():
    return render_template('risk_report.html')

@bp.route('/risk-list')
@login_required
def risk_list():
    return render_template('risk_list.html')

@bp.route('/analysis')
@login_required
def analysis():
    return render_template('analysis.html') 