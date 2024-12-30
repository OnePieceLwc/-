from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
from app.models import RiskEvent
from app import db
from datetime import datetime, timedelta
import pytz

bp = Blueprint('risk_monitor', __name__)

@bp.route('/api/risk/report', methods=['POST'])
@login_required
def report_risk():
    try:
        data = request.get_json()
        
        # 数据验证
        required_fields = ['title', 'type', 'risk_level', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f'缺少必要字段: {field}'
                }), 400
        
        # 创建新的风险事件
        new_risk = RiskEvent(
            title=data['title'],
            risk_type=data['type'],
            description=data['description'],
            risk_level=float(data['risk_level']),
            reporter_id=current_user.id,
            status='pending'
        )
        
        # 设置受影响系统
        if 'affected_systems' in data and data['affected_systems']:
            new_risk.set_affected_systems(data['affected_systems'])
        
        db.session.add(new_risk)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '风险事件已成功上报',
            'risk_id': new_risk.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/api/risk/list', methods=['GET'])
@login_required
def list_risks():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        risk_type = request.args.get('type')
        
        query = RiskEvent.query
        
        # 应用过滤条件
        if status:
            query = query.filter(RiskEvent.status == status)
        if risk_type:
            query = query.filter(RiskEvent.risk_type == risk_type)
            
        # 排序
        sort_by = request.args.get('sort_by', 'timestamp')
        sort_order = request.args.get('sort_order', 'desc')
        
        if sort_order == 'desc':
            query = query.order_by(getattr(RiskEvent, sort_by).desc())
        else:
            query = query.order_by(getattr(RiskEvent, sort_by).asc())
        
        # 分页
        pagination = query.paginate(page=page, per_page=per_page)
        
        risks = [{
            'id': risk.id,
            'title': risk.title,
            'type': risk.risk_type,
            'risk_level': risk.risk_level,
            'description': risk.description,
            'status': risk.status,
            'affected_systems': risk.get_affected_systems(),
            'timestamp': risk.timestamp.isoformat(),
            'reporter': risk.reporter.username if risk.reporter else None
        } for risk in pagination.items]
        
        return jsonify({
            'status': 'success',
            'data': risks,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/api/risk/statistics', methods=['GET'])
@login_required
def risk_statistics():
    try:
        # 获取时间范围
        days = request.args.get('days', 30, type=int)
        start_date = datetime.now() - timedelta(days=days)
        
        # 风险等级分布
        risk_levels = db.session.query(
            func.case(
                (RiskEvent.risk_level < 0.3, 'low'),
                (RiskEvent.risk_level < 0.7, 'medium'),
                else_='high'
            ).label('level'),
            func.count('*').label('count')
        ).filter(
            RiskEvent.timestamp >= start_date
        ).group_by('level').all()
        
        # 风险类型分布
        risk_types = db.session.query(
            RiskEvent.type,
            func.count('*').label('count')
        ).filter(
            RiskEvent.timestamp >= start_date
        ).group_by(RiskEvent.type).all()
        
        # 处理状态统计
        status_stats = db.session.query(
            RiskEvent.status,
            func.count('*').label('count')
        ).filter(
            RiskEvent.timestamp >= start_date
        ).group_by(RiskEvent.status).all()
        
        return jsonify({
            'status': 'success',
            'data': {
                'risk_levels': dict(risk_levels),
                'risk_types': dict(risk_types),
                'status_stats': dict(status_stats)
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 

@bp.route('/risk-detail/<int:risk_id>')
@login_required
def risk_detail(risk_id):
    risk = RiskEvent.query.get_or_404(risk_id)
    return render_template('risk_detail.html', risk=risk)

@bp.route('/api/risk/detail/<int:risk_id>')
@login_required
def get_risk_detail(risk_id):
    try:
        risk = RiskEvent.query.get_or_404(risk_id)
        return jsonify({
            'status': 'success',
            'data': {
                'id': risk.id,
                'title': risk.title,
                'type': risk.risk_type,
                'description': risk.description,
                'risk_level': risk.risk_level,
                'status': risk.status,
                'affected_systems': risk.get_affected_systems(),
                'timestamp': risk.timestamp.isoformat(),
                'reporter': risk.reporter.username if risk.reporter else None
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 

def get_trend_data():
    """获取最近7天的风险趋势数据"""
    # TODO: 从数据库获取实际数据
    # 这里使用模拟数据
    beijing_tz = pytz.timezone('Asia/Shanghai')
    today = datetime.now(beijing_tz)
    dates = [(today - timedelta(days=i)).strftime('%m-%d') for i in range(6, -1, -1)]
    
    return {
        'dates': dates,
        'counts': [12, 19, 15, 17, 14, 13, 16],  # 每天的风险事件数
        'high_risk': [3, 5, 2, 4, 3, 2, 4],      # 高风险事件数
        'medium_risk': [5, 8, 7, 8, 6, 6, 7],    # 中风险事件数
        'low_risk': [4, 6, 6, 5, 5, 5, 5]        # 低风险事件数
    }

def get_type_distribution():
    """获取风险类型分布数据"""
    # TODO: 从数据库获取实际数据
    return {
        'labels': ['数据泄露', '网络攻击', '系统漏洞', '未授权访问', '合规风险'],
        'data': [30, 25, 20, 15, 10],
        'colors': ['#3498db', '#e74c3c', '#f1c40f', '#2ecc71', '#9b59b6']
    }

@bp.route('/risk/monitor')
def index():
    trend_data = get_trend_data()
    type_data = get_type_distribution()
    level_data = {
        'labels': ['高风险', '中风险', '低风险'],
        'data': [30, 45, 25],
        'colors': ['#e74c3c', '#f1c40f', '#2ecc71']
    }
    
    return render_template('risk_monitor.html',
                         trend_data=trend_data,
                         type_data=type_data,
                         level_data=level_data)

@bp.route('/api/risk/trend')
def get_risk_trend():
    """获取风险趋势数据的API"""
    try:
        data = get_trend_data()
        return jsonify({
            'status': 'success',
            'data': data
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/api/risk/distribution')
def get_risk_distribution():
    """获取风险类型分布数据的API"""
    try:
        data = get_type_distribution()
        return jsonify({
            'status': 'success',
            'data': data
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 