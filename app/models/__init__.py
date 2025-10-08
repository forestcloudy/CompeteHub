# 这个文件让Python将models目录视为一个包
# 从这里导入所有模型，方便其他地方使用
from app.models.user import User
from app.models.competition import Competition
from app.models.team import TeamPost