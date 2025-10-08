from flask import Blueprint, request, jsonify
from app import db
from app.models.team import TeamPost
from app.services.data_processing import create_team_post_with_validation

bp = Blueprint('teams', __name__)


@bp.route('/teams', methods=['GET'])
def get_teams():
    """获取组队帖子列表"""
    try:
        # 从数据库查询所有组队帖子
        teams = TeamPost.query.all()
        
        # 将组队帖子对象转换为字典列表
        teams_data = []
        for team in teams:
            teams_data.append({
                'id': team.id,
                'title': team.title,
                'description': team.description,
                'required_roles': team.required_roles,
                'status': team.status,
                'created_at': team.created_at.isoformat() if team.created_at else None,
                'updated_at': team.updated_at.isoformat() if team.updated_at else None,
                'creator_id': team.creator_id,
                'competition_id': team.competition_id
            })
        
        # 返回JSON格式的组队帖子列表
        return jsonify(teams_data)
    except Exception as e:
        # 发生错误时返回错误信息
        return jsonify({'error': '获取组队帖子列表失败'}), 500


@bp.route('/teams', methods=['POST'])
def create_team():
    """创建新组队帖子"""
    try:
        # 从前端请求中获取JSON数据
        data = request.get_json()
        
        # 获取用户ID（实际项目中应该从认证信息中获取）
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'error': '用户ID是必需的'}), 400
        
        # 调用服务层处理业务逻辑
        result, success = create_team_post_with_validation(data, user_id)
        
        if success:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        # 发生错误时回滚事务并返回错误信息
        db.session.rollback()
        return jsonify({'error': '创建组队帖子失败: ' + str(e)}), 500


@bp.route('/teams/<int:team_id>', methods=['GET'])
def get_team(team_id):
    """获取特定组队帖子信息"""
    try:
        # 根据ID从数据库查询组队帖子
        team = TeamPost.query.get(team_id)
        
        # 检查组队帖子是否存在
        if not team:
            return jsonify({'error': '组队帖子不存在'}), 404
        
        # 返回组队帖子信息
        return jsonify({
            'id': team.id,
            'title': team.title,
            'description': team.description,
            'required_roles': team.required_roles,
            'status': team.status,
            'created_at': team.created_at.isoformat() if team.created_at else None,
            'updated_at': team.updated_at.isoformat() if team.updated_at else None,
            'creator_id': team.creator_id,
            'competition_id': team.competition_id
        })
    except Exception as e:
        # 发生错误时返回错误信息
        return jsonify({'error': '获取组队帖子信息失败'}), 500


@bp.route('/teams/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    """更新组队帖子信息"""
    try:
        # 根据ID从数据库查询组队帖子
        team = TeamPost.query.get(team_id)
        
        # 检查组队帖子是否存在
        if not team:
            return jsonify({'error': '组队帖子不存在'}), 404
        
        # 从前端请求中获取JSON数据
        data = request.get_json()
        
        # 更新组队帖子信息
        if 'title' in data:
            team.title = data['title']
        if 'description' in data:
            team.description = data['description']
        if 'required_roles' in data:
            team.required_roles = data['required_roles']
        if 'status' in data:
            team.status = data['status']
        
        # 提交事务，将更新写入数据库
        db.session.commit()
        
        # 返回更新成功的响应
        return jsonify({
            'message': '组队帖子更新成功',
            'team': {
                'id': team.id,
                'title': team.title,
                'description': team.description,
                'required_roles': team.required_roles,
                'status': team.status,
                'created_at': team.created_at.isoformat() if team.created_at else None,
                'updated_at': team.updated_at.isoformat() if team.updated_at else None
            }
        })
    except Exception as e:
        # 发生错误时回滚事务并返回错误信息
        db.session.rollback()
        return jsonify({'error': '更新组队帖子失败: ' + str(e)}), 500


@bp.route('/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    """删除组队帖子"""
    try:
        # 根据ID从数据库查询组队帖子
        team = TeamPost.query.get(team_id)
        
        # 检查组队帖子是否存在
        if not team:
            return jsonify({'error': '组队帖子不存在'}), 404
        
        # 从数据库会话中删除组队帖子
        db.session.delete(team)
        
        # 提交事务，将删除操作写入数据库
        db.session.commit()
        
        # 返回删除成功的响应
        return jsonify({'message': '组队帖子删除成功'})
    except Exception as e:
        # 发生错误时回滚事务并返回错误信息
        db.session.rollback()
        return jsonify({'error': '删除组队帖子失败: ' + str(e)}), 500