# 从app包中导入create_app函数，这是应用的工厂函数
from app import create_app

# 调用工厂函数创建Flask应用实例
app = create_app()

# 当此脚本被直接运行时（而不是被导入时），执行以下代码
if __name__ == '__main__':
    # 使应用可以从外部设备访问，而不仅仅是本地
    app.run(debug=True, host='0.0.0.0')
