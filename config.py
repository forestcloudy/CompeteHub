import os


class Config:
    # 密钥，用于会话安全等，生产环境务必设为随机字符串
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-hard-to-guess-string'

    # 数据库配置：使用SQLite，数据库文件将位于项目根目录的 'instance' 文件夹中
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'instance', 'competehub.sqlite')

    # 关闭动态追踪修改的警告（可选，但推荐关闭）
    SQLALCHEMY_TRACK_MODIFICATIONS = False