"""
Time utility functions for the lottery system.
"""

from datetime import datetime

# Constants for countdown messages
# Note: These are in Chinese to match the rest of the application
# For internationalization, these could be moved to a config or i18n module
DEADLINE_PASSED_MESSAGE = "已截止"
URGENT_THRESHOLD_SECONDS = 1800  # 30 minutes


def calculate_countdown(deadline_hour, deadline_minute):
    """
    计算倒计时
    
    Args:
        deadline_hour: 截止小时
        deadline_minute: 截止分钟
        
    Returns:
        倒计时字符串和是否紧急
    """
    now = datetime.now()
    deadline_today = now.replace(hour=deadline_hour, minute=deadline_minute, second=0, microsecond=0)
    
    if now < deadline_today:
        time_left = deadline_today - now
        hours = time_left.seconds // 3600
        minutes = (time_left.seconds % 3600) // 60
        seconds = time_left.seconds % 60
        
        # 如果剩余时间少于30分钟，标记为紧急
        is_urgent = time_left.total_seconds() < URGENT_THRESHOLD_SECONDS
        
        if hours > 0:
            countdown = f"{hours}小时{minutes}分钟"
        elif minutes > 0:
            countdown = f"{minutes}分{seconds}秒"
        else:
            countdown = f"{seconds}秒"
            
        return countdown, is_urgent
    else:
        return DEADLINE_PASSED_MESSAGE, False
