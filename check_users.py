#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查数据库中的用户信息
"""

from app import create_app
from app.models.user import User


def check_users():
    """检查所有用户"""
    app = create_app()
    with app.app_context():
        users = User.query.all()
        print("数据库中的所有用户:")
        print("-" * 50)
        for user in users:
            print(f"ID: {user.id}")
            print(f"用户名: {user.username}")
            print(f"邮箱: {user.email}")
            print(f"大学: {user.university or '未填写'}")
            print(f"专业: {user.major or '未填写'}")
            print(f"创建时间: {user.created_at}")
            print("-" * 30)


def find_user(username):
    """根据用户名查找用户"""
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            print(f"找到用户 '{username}':")
            print(f"ID: {user.id}")
            print(f"用户名: {user.username}")
            print(f"邮箱: {user.email}")
            print(f"大学: {user.university or '未填写'}")
            print(f"专业: {user.major or '未填写'}")
            print(f"创建时间: {user.created_at}")
        else:
            print(f"未找到用户名为 '{username}' 的用户")


if __name__ == '__main__':
    check_users()
    
    # 如果你想查找特定用户，可以修改下面这行中的用户名
    find_user("cloudy")