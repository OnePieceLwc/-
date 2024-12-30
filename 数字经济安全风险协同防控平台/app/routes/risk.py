from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import pytz  # 添加时区支持

bp = Blueprint('risk', __name__)

def get_beijing_time():
    """获取北京时间"""
    beijing_tz = pytz.timezone('Asia/Shanghai')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    beijing_now = utc_now.astimezone(beijing_tz)
    return beijing_now.strftime('%Y-%m-%d %H:%M:%S')

@bp.route('/api/risk/report', methods=['POST'])
def report_risk():
    try:
        # 获取JSON数据
        data = request.get_json()
        
        # 获取表单数据
        title = data.get('title')
        risk_type = data.get('type')
        risk_level = float(data.get('risk_level', 0))
        description = data.get('description')
        affected_systems = data.get('affected_systems')
        
        # 如果affected_systems是字符串，需要解析JSON
        if isinstance(affected_systems, str):
            affected_systems = json.loads(affected_systems)

        # 数据验证
        if not all([title, risk_type, description, affected_systems]):
            return jsonify({
                'status': 'error',
                'message': '请填写所有必填字段'
            }), 400

        # TODO: 保存到数据库
        # 这里添加保存到数据库的代码
        
        # 使用北京时间
        created_at = get_beijing_time()
        
        # 模拟保存成功
        return jsonify({
            'status': 'success',
            'message': '风险事件上报成功',
            'data': {
                'id': 1,  # 这里应该是数据库生成的ID
                'title': title,
                'type': risk_type,
                'level': risk_level,
                'description': description,
                'affected_systems': affected_systems,
                'created_at': created_at
            }
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/api/risk/<int:risk_id>', methods=['GET'])
def get_risk_detail(risk_id):
    try:
        # TODO: 从数据库获取风险详情
        # 这里暂时返回模拟数据
        risk_detail = {
            'id': risk_id,
            'title': '示例风险事件',
            'type': 'data_leak',
            'level': 0.8,
            'description': '这是一个示例风险事件的详细描述...',
            'affected_systems': ['core_system', 'business_system'],
            'status': 'processing',
            'created_at': get_beijing_time()  # 使用北京时间
        }
        
        return jsonify({
            'status': 'success',
            'data': risk_detail
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 