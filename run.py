# 从app包中导入create_app函数，这是应用的工厂函数
from app import create_app

# 调用工厂函数创建Flask应用实例
app = create_app()

# 当此脚本被直接运行时（而不是被导入时），执行以下代码
if __name__ == '__main__':
    # 启动Flask开发服务器，开启调试模式
    # 调试模式下，代码更改会自动重启服务器，方便开发
    app.run(debug=True)