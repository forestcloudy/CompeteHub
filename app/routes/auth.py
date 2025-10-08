from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['POST'])
def register():
    """用户注册路由"""
    data = request.get_json()

    # 检查用户名或邮箱是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': '用户名已存在'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': '邮箱已被注册'}), 400

    # 创建新用户
    user = User(
        username=data['username'],
        email=data['email'],
        university=data.get('university'),
        major=data.get('major')
    )
    user.set_password(data['password'])  # 加密密码

    # 保存到数据库
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': '用户注册成功！', 'user_id': user.id}), 201


@bp.route('/login', methods=['POST'])
def login():
    """用户登录路由"""
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        return jsonify({'message': '登录成功！', 'user_id': user.id})
    else:
        return jsonify({'error': '用户名或密码错误'}), 401