# 从app包中导入db对象，这是SQLAlchemy的实例
from app import db


class Competition(db.Model):
    """竞赛信息模型 - 对应数据库中的competitions表"""
    # 指定数据库表名
    __tablename__ = 'competitions'

    # 竞赛ID字段，整数类型，主键（唯一标识每条记录）
    id = db.Column(db.Integer, primary_key=True)
    # 竞赛名称字段，字符串类型，最大长度200字符，不能为空
    name = db.Column(db.String(200), nullable=False)
    # 主办方字段，字符串类型，最大长度100字符，可以为空
    organizer = db.Column(db.String(100))
    # 截止日期字段，DateTime类型，可以为空
    deadline = db.Column(db.DateTime)
    # 竞赛描述字段，Text类型（长文本），可以为空
    description = db.Column(db.Text)
    # 竞赛类别字段，字符串类型，最大长度50字符，可以为空
    # 例如："算法", "创业", "数据科学"等
    category = db.Column(db.String(50))
    # 官方链接字段，字符串类型，最大长度200字符，可以为空
    official_link = db.Column(db.String(200))

    # 关系定义：一个竞赛可以有多个相关的组队帖子
    # 这建立了与TeamPost模型的外键关系
    # 'TeamPost' 是关联的模型类名
    # backref='competition' 在TeamPost模型中创建一个名为'competition'的反向引用
    # lazy='dynamic' 表示查询时不会立即加载相关对象，而是在访问时才加载
    team_posts = db.relationship('TeamPost', backref='competition', lazy='dynamic')

    def __repr__(self):
        # 定义对象的字符串表示形式，便于调试
        return f'<Competition {self.name}>'