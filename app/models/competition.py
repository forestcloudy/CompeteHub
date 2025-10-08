from app import db


class Competition(db.Model):
    """竞赛信息模型"""
    __tablename__ = 'competitions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    organizer = db.Column(db.String(100))  # 主办方
    deadline = db.Column(db.DateTime)  # 截止日期
    description = db.Column(db.Text)  # 竞赛描述
    category = db.Column(db.String(50))  # 竞赛类别，如 "算法", "创业"
    official_link = db.Column(db.String(200))  # 官方链接

    # 关系：一个竞赛可以有多个相关的组队帖子
    team_posts = db.relationship('TeamPost', backref='competition', lazy='dynamic')

    def __repr__(self):
        return f'<Competition {self.name}>'