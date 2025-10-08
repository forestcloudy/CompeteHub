#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
初始化数据脚本
用于向数据库中添加示例数据
"""

from app import create_app
from app.models.competition import Competition
from app.models.user import User
from app.models.team import TeamPost
from app import db
from datetime import datetime


def init_competitions():
    """初始化竞赛数据"""
    competitions_data = [
        {
            'name': 'ACM国际大学生程序设计竞赛',
            'organizer': 'ACM协会',
            'deadline': datetime(2023, 12, 31, 23, 59, 59),
            'description': '一项历史悠久的国际性编程竞赛，旨在展示大学生创新能力、团队精神和在压力下解决问题的能力。',
            'category': '算法',
            'official_link': 'https://icpc.global'
        },
        {
            'name': '全国大学生数学建模竞赛',
            'organizer': '中国工业与应用数学学会',
            'deadline': datetime(2023, 9, 15, 18, 0, 0),
            'description': '全国大学生数学建模竞赛创办于1992年，每年一届，是首批列入"高校学科竞赛排行榜"的19项竞赛之一。',
            'category': '数学建模',
            'official_link': 'http://www.mcm.edu.cn'
        },
        {
            'name': '"互联网+"大学生创新创业大赛',
            'organizer': '教育部等部委',
            'deadline': datetime(2023, 10, 20, 23, 59, 59),
            'description': '旨在深化高等教育综合改革，激发大学生的创造力，培养造就"大众创业、万众创新"的主力军。',
            'category': '创业',
            'official_link': 'https://cy.ncss.cn'
        }
    ]
    
    # 添加竞赛数据到数据库
    for comp_data in competitions_data:
        # 检查是否已存在
        existing = Competition.query.filter_by(name=comp_data['name']).first()
        if not existing:
            competition = Competition(**comp_data)
            db.session.add(competition)
            print(f"已添加竞赛: {comp_data['name']}")
        else:
            print(f"竞赛已存在: {comp_data['name']}")
    
    # 提交事务
    db.session.commit()
    print("竞赛数据初始化完成！")


def init_users():
    """初始化用户数据"""
    users_data = [
        {
            'username': 'SGA',
            'email': 'ming@example.com',
            'university': '华南师范大学',
            'major': '计算机科学与技术'
        },
        {
            'username': 'HongKongDoll',
            'email': 'HKDoll@example.com',
            'university': '香港大学',
            'major': '软件工程'
        }
    ]
    
    for user_data in users_data:
        # 检查是否已存在
        existing = User.query.filter_by(username=user_data['username']).first()
        if not existing:
            user = User(**user_data)
            user.set_password('password123')  # 设置默认密码
            db.session.add(user)
            print(f"已添加用户: {user_data['username']}")
        else:
            print(f"用户已存在: {user_data['username']}")
    
    # 提交事务
    db.session.commit()
    print("用户数据初始化完成！")


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        init_competitions()
        init_users()
        print("所有初始化数据添加完成！")