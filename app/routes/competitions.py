from flask import Blueprint, request, jsonify
from app import db
from app.models.competition import Competition
from datetime import datetime

# 创建竞赛模块的蓝图，命名为'competitions'
bp = Blueprint('competitions', __name__)


@bp.route('/competitions', methods=['GET'])
def get_competitions():
    """获取竞赛列表"""
    try:
        # 从数据库查询所有竞赛
        competitions = Competition.query.all()
        
        # 将竞赛对象转换为字典列表
        competitions_data = []
        for competition in competitions:
            competitions_data.append({
                'id': competition.id,
                'name': competition.name,
                'organizer': competition.organizer,
                'deadline': competition.deadline.isoformat() if competition.deadline else None,
                'description': competition.description,
                'category': competition.category,
                'official_link': competition.official_link
            })
        
        # 返回JSON格式的竞赛列表
        return jsonify(competitions_data)
    except Exception as e:
        # 发生错误时返回错误信息
        return jsonify({'error': '获取竞赛列表失败'}), 500


@bp.route('/competitions', methods=['POST'])
def create_competition():
    """创建新竞赛"""
    try:
        # 从前端请求中获取JSON数据
        data = request.get_json()
        
        # 验证必需字段
        if not data or not data.get('name'):
            return jsonify({'error': '竞赛名称是必需的'}), 400
        
        # 创建新的竞赛对象
        competition = Competition(
            name=data['name'],
            organizer=data.get('organizer'),
            deadline=datetime.fromisoformat(data['deadline']) if data.get('deadline') else None,
            description=data.get('description'),
            category=data.get('category'),
            official_link=data.get('official_link')
        )
        
        # 添加到数据库会话
        db.session.add(competition)
        
        # 提交事务，将数据写入数据库
        db.session.commit()
        
        # 返回创建成功的响应
        return jsonify({
            'message': '竞赛创建成功',
            'competition': {
                'id': competition.id,
                'name': competition.name,
                'organizer': competition.organizer,
                'deadline': competition.deadline.isoformat() if competition.deadline else None,
                'description': competition.description,
                'category': competition.category,
                'official_link': competition.official_link
            }
        }), 201
    except Exception as e:
        # 发生错误时回滚事务并返回错误信息
        db.session.rollback()
        return jsonify({'error': '创建竞赛失败'}), 500


@bp.route('/competitions/<int:competition_id>', methods=['GET'])
def get_competition(competition_id):
    """获取特定竞赛信息"""
    try:
        # 根据ID从数据库查询竞赛
        competition = Competition.query.get(competition_id)
        
        # 检查竞赛是否存在
        if not competition:
            return jsonify({'error': '竞赛不存在'}), 404
        
        # 返回竞赛信息
        return jsonify({
            'id': competition.id,
            'name': competition.name,
            'organizer': competition.organizer,
            'deadline': competition.deadline.isoformat() if competition.deadline else None,
            'description': competition.description,
            'category': competition.category,
            'official_link': competition.official_link
        })
    except Exception as e:
        # 发生错误时返回错误信息
        return jsonify({'error': '获取竞赛信息失败'}), 500


@bp.route('/competitions/<int:competition_id>', methods=['PUT'])
def update_competition(competition_id):
    """更新竞赛信息"""
    try:
        # 根据ID从数据库查询竞赛
        competition = Competition.query.get(competition_id)
        
        # 检查竞赛是否存在
        if not competition:
            return jsonify({'error': '竞赛不存在'}), 404
        
        # 从前端请求中获取JSON数据
        data = request.get_json()
        
        # 更新竞赛信息
        if 'name' in data:
            competition.name = data['name']
        if 'organizer' in data:
            competition.organizer = data['organizer']
        if 'deadline' in data:
            competition.deadline = datetime.fromisoformat(data['deadline']) if data['deadline'] else None
        if 'description' in data:
            competition.description = data['description']
        if 'category' in data:
            competition.category = data['category']
        if 'official_link' in data:
            competition.official_link = data['official_link']
        
        # 提交事务，将更新写入数据库
        db.session.commit()
        
        # 返回更新成功的响应
        return jsonify({
            'message': '竞赛更新成功',
            'competition': {
                'id': competition.id,
                'name': competition.name,
                'organizer': competition.organizer,
                'deadline': competition.deadline.isoformat() if competition.deadline else None,
                'description': competition.description,
                'category': competition.category,
                'official_link': competition.official_link
            }
        })
    except Exception as e:
        # 发生错误时回滚事务并返回错误信息
        db.session.rollback()
        return jsonify({'error': '更新竞赛失败'}), 500


@bp.route('/competitions/<int:competition_id>', methods=['DELETE'])
def delete_competition(competition_id):
    """删除竞赛"""
    try:
        # 根据ID从数据库查询竞赛
        competition = Competition.query.get(competition_id)
        
        # 检查竞赛是否存在
        if not competition:
            return jsonify({'error': '竞赛不存在'}), 404
        
        # 从数据库会话中删除竞赛
        db.session.delete(competition)
        
        # 提交事务，将删除操作写入数据库
        db.session.commit()
        
        # 返回删除成功的响应
        return jsonify({'message': '竞赛删除成功'})
    except Exception as e:
        # 发生错误时回滚事务并返回错误信息
        db.session.rollback()
        return jsonify({'error': '删除竞赛失败'}), 500