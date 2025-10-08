from flask import Blueprint, request, jsonify

bp = Blueprint('profiles', __name__)


@bp.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    """获取用户资料"""
    # 这里应该从数据库获取指定用户的信息
    # 目前返回空对象作为示例
    return jsonify({})


@bp.route('/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    """更新用户资料"""
    # 这里应该处理更新用户资料的逻辑
    # 目前返回空对象作为示例
    return jsonify({})