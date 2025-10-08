#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据处理服务模块
包含复杂的业务逻辑处理函数
"""

from app.models.competition import Competition
from app.models.user import User
from app.models.team import TeamPost
from app import db
from datetime import datetime


def create_competition_with_validation(competition_data):
    """
    创建竞赛（带验证的业务逻辑）
    
    Args:
        competition_data (dict): 竞赛数据
        
    Returns:
        dict: 创建结果
        bool: 是否成功
    """
    # 业务逻辑1: 验证竞赛名称唯一性
    existing = Competition.query.filter_by(name=competition_data['name']).first()
    if existing:
        return {'error': '竞赛名称已存在'}, False
    
    # 业务逻辑2: 验证截止日期不能早于当前时间
    if 'deadline' in competition_data and competition_data['deadline']:
        deadline = datetime.fromisoformat(competition_data['deadline'])
        if deadline < datetime.now():
            return {'error': '截止日期不能早于当前时间'}, False
    
    # 业务逻辑3: 验证竞赛类别
    valid_categories = ['算法', '创业', '数学建模', '数据科学', '其他']
    if 'category' in competition_data and competition_data['category'] not in valid_categories:
        return {'error': f'竞赛类别必须是以下之一: {", ".join(valid_categories)}'}, False
    
    # 创建竞赛对象
    competition = Competition(
        name=competition_data['name'],
        organizer=competition_data.get('organizer'),
        deadline=datetime.fromisoformat(competition_data['deadline']) if competition_data.get('deadline') else None,
        description=competition_data.get('description'),
        category=competition_data.get('category'),
        official_link=competition_data.get('official_link')
    )
    
    try:
        db.session.add(competition)
        db.session.commit()
        return {
            'message': '竞赛创建成功',
            'competition': {
                'id': competition.id,
                'name': competition.name,
                'organizer': competition.organizer,
                'deadline': competition.deadline.isoformat() if competition.deadline else None,
                'description': competition.description,
                'category': competition.category,
                'official_link': competition.official_link
            }
        }, True
    except Exception as e:
        db.session.rollback()
        return {'error': f'创建竞赛失败: {str(e)}'}, False


def get_competition_statistics():
    """
    获取竞赛统计信息
    
    Returns:
        dict: 统计信息
    """
    # 获取竞赛总数
    total_competitions = Competition.query.count()
    
    # 按类别统计
    categories = db.session.query(
        Competition.category, 
        db.func.count(Competition.id)
    ).group_by(Competition.category).all()
    
    # 获取最近的竞赛
    recent_competitions = Competition.query.order_by(
        Competition.created_at.desc() if hasattr(Competition, 'created_at') else Competition.id.desc()
    ).limit(5).all()
    
    return {
        'total_competitions': total_competitions,
        'categories_distribution': dict(categories),
        'recent_competitions': [
            {
                'id': comp.id,
                'name': comp.name,
                'category': comp.category
            } for comp in recent_competitions
        ]
    }


def search_competitions(keyword):
    """
    搜索竞赛
    
    Args:
        keyword (str): 搜索关键词
        
    Returns:
        list: 搜索结果
    """
    # 在名称和描述中搜索
    competitions = Competition.query.filter(
        db.or_(
            Competition.name.contains(keyword),
            Competition.description.contains(keyword)
        )
    ).all()
    
    return [
        {
            'id': comp.id,
            'name': comp.name,
            'organizer': comp.organizer,
            'deadline': comp.deadline.isoformat() if comp.deadline else None,
            'category': comp.category
        } for comp in competitions
    ]


def create_team_post_with_validation(team_data, user_id):
    """
    创建组队帖子（带验证的业务逻辑）
    
    Args:
        team_data (dict): 组队帖子数据
        user_id (int): 创建用户ID
        
    Returns:
        dict: 创建结果
        bool: 是否成功
    """
    # 验证用户是否存在
    user = User.query.get(user_id)
    if not user:
        return {'error': '用户不存在'}, False
    
    # 验证竞赛是否存在
    competition_id = team_data.get('competition_id')
    competition = Competition.query.get(competition_id) if competition_id else None
    if competition_id and not competition:
        return {'error': '指定的竞赛不存在'}, False
    
    # 验证标题
    if not team_data.get('title') or len(team_data.get('title', '')) < 5:
        return {'error': '标题至少需要5个字符'}, False
    
    # 创建组队帖子
    team_post = TeamPost(
        title=team_data['title'],
        description=team_data.get('description'),
        required_roles=team_data.get('required_roles'),
        creator_id=user_id,
        competition_id=competition_id
    )
    
    try:
        db.session.add(team_post)
        db.session.commit()
        return {
            'message': '组队帖子创建成功',
            'team_post': {
                'id': team_post.id,
                'title': team_post.title,
                'description': team_post.description,
                'status': team_post.status,
                'created_at': team_post.created_at.isoformat() if team_post.created_at else None
            }
        }, True
    except Exception as e:
        db.session.rollback()
        return {'error': f'创建组队帖子失败: {str(e)}'}, False