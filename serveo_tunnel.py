#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用 Serveo 创建公网隧道访问本地 Flask 应用
注意：此方法需要系统安装了 SSH 客户端
"""

import subprocess
import sys
import os

def create_serveo_tunnel():
    """创建 Serveo 隧道"""
    try:
        print("正在创建 Serveo 隧道...")
        print("请在提示时选择 '是' 来确认 SSH 连接")
        print("隧道创建成功后，会显示一个公网 URL")
        print("按 Ctrl+C 可以停止隧道")
        print("")
        
        # 使用 SSH 创建隧道
        # 这会将本地 5000 端口映射到公网
        command = "ssh -R 80:localhost:5000 serveo.net"
        process = subprocess.Popen(command, shell=True)
        process.wait()
        
    except KeyboardInterrupt:
        print("\n正在关闭 Serveo 隧道...")
        print("Serveo 隧道已关闭")
    except Exception as e:
        print(f"创建隧道时出错: {e}")

if __name__ == "__main__":
    print("Serveo 隧道创建工具")
    print("=" * 30)
    print("说明：")
    print("1. 此方法需要系统安装了 SSH 客户端")
    print("2. 首次连接时可能会提示确认密钥")
    print("3. 生成的网址每次运行都会变化")
    print("")
    
    # 确认是否继续
    response = input("是否继续创建隧道？(y/n): ")
    if response.lower() in ['y', 'yes', '是']:
        create_serveo_tunnel()
    else:
        print("已取消操作")