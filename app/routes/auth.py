from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['POST'])
def register():
    """用户注册路由"""
    # 从前端接收JSON数据
    data = request.get_json()
    
    # 验证必需字段
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': '用户名、邮箱和密码是必需的'}), 400

    # 检查用户名或邮箱是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': '用户名已存在'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': '邮箱已被注册'}), 400

    # 创建新用户对象
    user = User(
        username=data['username'],
        email=data['email'],
        university=data.get('university'),
        major=data.get('major'),
        gpa=data.get('gpa'),
        skills=data.get('skills'),
        experience=data.get('experience')
    )
    # 对密码进行哈希加密处理
    user.set_password(data['password'])

    # 保存到数据库
    try:
        db.session.add(user)
        db.session.commit()
        # 返回成功响应给前端
        return jsonify({
            'message': '用户注册成功！', 
            'user_id': user.id,
            'username': user.username
        }), 201
    except Exception as e:
        # 出现错误时回滚事务
        db.session.rollback()
        return jsonify({'error': '注册失败，请稍后重试'}), 500


@bp.route('/login', methods=['POST'])
def login():
    """用户登录路由"""
    # 从前端接收JSON数据
    data = request.get_json()
    
    # 验证必需字段
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': '用户名和密码是必需的'}), 400

    # 根据用户名查找用户
    user = User.query.filter_by(username=data['username']).first()

    # 验证用户存在且密码正确
    if user and user.check_password(data['password']):
        # 登录成功，返回用户信息
        return jsonify({
            'message': '登录成功！', 
            'user_id': user.id,
            'username': user.username
        })
    else:
        # 登录失败，返回错误信息
        return jsonify({'error': '用户名或密码错误'}), 401


@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """获取用户信息路由"""
    # 根据用户ID查找用户
    user = User.query.get(user_id)
    
    # 检查用户是否存在
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 返回用户信息给前端
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'university': user.university,
        'major': user.major,
        'gpa': user.gpa,
        'skills': user.skills,
        'experience': user.experience,
        'created_at': user.created_at.isoformat() if user.created_at else None
    })


@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """更新用户信息路由"""
    # 根据用户ID查找用户
    user = User.query.get(user_id)
    
    # 检查用户是否存在
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 从前端接收JSON数据
    data = request.get_json()
    
    # 更新用户信息
    if 'university' in data:
        user.university = data['university']
    if 'major' in data:
        user.major = data['major']
    if 'gpa' in data:
        user.gpa = data['gpa']
    if 'skills' in data:
        user.skills = data['skills']
    if 'experience' in data:
        user.experience = data['experience']
    
    # 如果提供了新密码，则更新密码
    if 'password' in data:
        user.set_password(data['password'])
    
    # 保存到数据库
    try:
        db.session.commit()
        # 返回成功响应给前端
        return jsonify({
            'message': '用户信息更新成功！',
            'user_id': user.id
        })
    except Exception as e:
        # 出现错误时回滚事务
        db.session.rollback()
        return jsonify({'error': '更新失败，请稍后重试'}), 500