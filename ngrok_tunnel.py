#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用 Ngrok 创建公网隧道访问本地 Flask 应用
"""

from pyngrok import ngrok
import threading
import time
import subprocess
import sys
import os

def start_flask_app():
    """启动 Flask 应用"""
    try:
        # 启动 Flask 应用
        os.system("python run.py")
    except KeyboardInterrupt:
        print("Flask 应用已停止")
    except Exception as e:
        print(f"启动 Flask 应用时出错: {e}")

def create_tunnel():
    """创建 Ngrok 隧道"""
    try:
        # 设置 Ngrok authtoken (可选，但建议注册获取)
        # ngrok.set_auth_token("你的_authtoken")
        
        # 创建隧道，将本地 5000 端口映射到公网
        public_url = ngrok.connect(5000)
        print(f"Ngrok 隧道已创建!")
        print(f"本地地址: http://localhost:5000")
        print(f"公网地址: {public_url}")
        print("按 Ctrl+C 停止隧道")
        
        # 保持隧道运行
        ngrok_process = ngrok.get_ngrok_process()
        ngrok_process.proc.wait()
        
    except KeyboardInterrupt:
        print("\n正在关闭 Ngrok 隧道...")
        ngrok.kill()
        print("Ngrok 隧道已关闭")
    except Exception as e:
        print(f"创建隧道时出错: {e}")
        ngrok.kill()

if __name__ == "__main__":
    print("正在启动 Ngrok 隧道...")
    
    # 创建线程启动 Flask 应用
    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    
    # 等待 Flask 应用启动
    time.sleep(3)
    
    # 创建 Ngrok 隧道
    create_tunnel()