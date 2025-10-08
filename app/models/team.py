from app import db
from datetime import datetime


class TeamPost(db.Model):
    """组队帖子模型"""
    __tablename__ = 'team_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)  # 帖子详细描述
    required_roles = db.Column(db.Text)  # 需要的角色/技能，如 "前端开发*1, 后端开发*2"
    status = db.Column(db.String(20), default='recruiting')  # recruiting, full, closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 外键：关联到用户表（发布者）
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # 外键：关联到竞赛表（这个组队帖子是关于哪个竞赛的）
    competition_id = db.Column(db.Integer, db.ForeignKey('competitions.id'), nullable=False)

    def __repr__(self):
        return f'<TeamPost {self.title}>'