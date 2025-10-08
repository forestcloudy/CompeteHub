from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config  # 我们会创建一个配置文件

# 创建SQLAlchemy实例，但先不关联app
db = SQLAlchemy()


def create_app():
    """应用工厂函数"""
    app = Flask(__name__)

    # 从config.py中加载配置
    app.config.from_object(Config)

    # 初始化数据库扩展，关联到app
    db.init_app(app)

    # 在这里注册蓝图（后面会用到）
    from app.routes import auth, competitions, teams, profiles

    app.register_blueprint(auth.bp)
    app.register_blueprint(competitions.bp)
    app.register_blueprint(teams.bp)
    app.register_blueprint(profiles.bp)

    # 注册静态文件路由
    @app.route('/')
    def index():
        return app.send_static_file('login.html')

    # 在应用上下文中创建所有数据库表
    with app.app_context():
        db.create_all()
        print(" * 所有数据库表已就绪！")

    return app