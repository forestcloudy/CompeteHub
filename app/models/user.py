from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'  # 数据库中的表名

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    # 注意：存储的是密码的哈希值，而非明文！
    password_hash = db.Column(db.String(128), nullable=False)
    university = db.Column(db.String(100))
    major = db.Column(db.String(100))
    gpa = db.Column(db.Float)
    skills = db.Column(db.Text)  # 用逗号分隔的字符串存储技能，如 "Python,Java,前端"
    experience = db.Column(db.Text)  # 过往经验描述
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系：一个用户可以创建多个组队帖子
    team_posts = db.relationship('TeamPost', backref='creator', lazy='dynamic', cascade='all, delete-orphan')

    # 关系：一个用户可以发表多篇经验分享（如果需要的话）
    # articles = db.relationship('Article', backref='author', lazy='dynamic')

    def set_password(self, password):
        """设置密码，自动进行哈希加密"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """检查密码是否正确"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'