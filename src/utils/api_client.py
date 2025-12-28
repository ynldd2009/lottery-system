"""
彩票API客户端模块
用于与外部彩票数据API进行交互
"""

import requests
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

class LotteryAPIClient:
    """彩票API客户端"""
    
    # API配置
    API_CONFIG = {
        "base_url": "https://www.mxnzp.com/api/lottery/common",
        "endpoints": {
            "aim_lottery": "/aim_lottery",      # 指定期号
            "latest": "/latest",                # 最新开奖
            "history": "/history",              # 历史开奖
            "types": "/types",                  # 彩种类型
            "check": "/check"                   # 中奖查询
        }
    }
    
    # 彩票类型映射（系统内部名称 -> API代码）
    LOTTERY_TYPE_MAP = {
        "双色球": "ssq",
        "大乐透": "dlt",
        "快乐8": "kl8",
        "七乐彩": "qlc",
        "3D": "sd",
        "福彩3D": "fc3d",
        "排列三": "pl3",
        "排列五": "pl5",
        "七星彩": "qxc"
    }
    
    def __init__(self, app_id: str = "", app_secret: str = ""):
        """
        初始化API客户端
        
        Args:
            app_id: API应用ID
            app_secret: API密钥
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict]:
        """
        发送API请求
        
        Args:
            endpoint: API端点
            params: 请求参数
            
        Returns:
            API响应数据，失败返回None
        """
        try:
            # 添加认证参数
            params['app_id'] = self.app_id
            params['app_secret'] = self.app_secret
            
            url = self.API_CONFIG["base_url"] + endpoint
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # 检查API返回码
            if data.get('code') == 1:
                return data.get('data')
            else:
                print(f"API错误: {data.get('msg', '未知错误')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
            return None
        except Exception as e:
            print(f"未知错误: {e}")
            return None
    
    def get_latest_draw(self, lottery_type: str) -> Optional[Dict]:
        """
        获取最新开奖结果
        
        Args:
            lottery_type: 彩票类型（如"双色球"、"大乐透"）
            
        Returns:
            开奖结果数据，包含期号、开奖号码、开奖日期等
        """
        api_code = self.LOTTERY_TYPE_MAP.get(lottery_type)
        if not api_code:
            print(f"不支持的彩票类型: {lottery_type}")
            return None
        
        endpoint = self.API_CONFIG["endpoints"]["latest"]
        params = {'code': api_code}
        
        return self._make_request(endpoint, params)
    
    def get_draw_by_period(self, lottery_type: str, expect: str) -> Optional[Dict]:
        """
        获取指定期号的开奖结果
        
        Args:
            lottery_type: 彩票类型
            expect: 期号
            
        Returns:
            开奖结果数据
        """
        api_code = self.LOTTERY_TYPE_MAP.get(lottery_type)
        if not api_code:
            return None
        
        endpoint = self.API_CONFIG["endpoints"]["aim_lottery"]
        params = {'code': api_code, 'expect': expect}
        
        return self._make_request(endpoint, params)
    
    def get_history_draws(self, lottery_type: str, size: int = 30) -> Optional[List[Dict]]:
        """
        获取历史开奖记录
        
        Args:
            lottery_type: 彩票类型
            size: 获取数量（默认30期）
            
        Returns:
            历史开奖记录列表
        """
        api_code = self.LOTTERY_TYPE_MAP.get(lottery_type)
        if not api_code:
            return None
        
        endpoint = self.API_CONFIG["endpoints"]["history"]
        params = {'code': api_code, 'size': size}
        
        data = self._make_request(endpoint, params)
        if data and isinstance(data, dict):
            return data.get('list', [])
        return None
    
    def check_prize(self, lottery_type: str, numbers: str, expect: str = "") -> Optional[Dict]:
        """
        检查中奖情况
        
        Args:
            lottery_type: 彩票类型
            numbers: 投注号码（格式根据彩票类型而定）
            expect: 期号（可选，不填则检查最新一期）
            
        Returns:
            中奖结果数据
        """
        api_code = self.LOTTERY_TYPE_MAP.get(lottery_type)
        if not api_code:
            return None
        
        endpoint = self.API_CONFIG["endpoints"]["check"]
        params = {'code': api_code, 'number': numbers}
        
        if expect:
            params['expect'] = expect
        
        return self._make_request(endpoint, params)
    
    def get_lottery_types(self) -> Optional[List[Dict]]:
        """
        获取所有支持的彩票类型
        
        Returns:
            彩票类型列表
        """
        endpoint = self.API_CONFIG["endpoints"]["types"]
        params = {}
        
        return self._make_request(endpoint, params)
    
    def format_draw_result(self, lottery_type: str, draw_data: Dict) -> Dict:
        """
        格式化开奖结果为统一格式
        
        Args:
            lottery_type: 彩票类型
            draw_data: API返回的原始数据
            
        Returns:
            格式化后的结果
        """
        if not draw_data:
            return {}
        
        result = {
            'lottery_type': lottery_type,
            'period': draw_data.get('expect', ''),
            'draw_date': draw_data.get('openTime', ''),
            'numbers': [],
            'extra_numbers': []
        }
        
        # 根据彩票类型解析号码
        if lottery_type == "双色球":
            opencode = draw_data.get('openCode', '')
            if opencode:
                parts = opencode.split('+')
                if len(parts) == 2:
                    result['numbers'] = [int(n) for n in parts[0].split(',')]
                    result['extra_numbers'] = [int(parts[1])]
        
        elif lottery_type == "大乐透":
            opencode = draw_data.get('openCode', '')
            if opencode:
                parts = opencode.split('+')
                if len(parts) == 2:
                    result['numbers'] = [int(n) for n in parts[0].split(',')]
                    result['extra_numbers'] = [int(n) for n in parts[1].split(',')]
        
        elif lottery_type in ["快乐8", "七乐彩", "3D", "福彩3D", "排列三", "排列五", "七星彩"]:
            opencode = draw_data.get('openCode', '')
            if opencode:
                result['numbers'] = [int(n) for n in opencode.split(',')]
        
        return result
    
    def is_configured(self) -> bool:
        """检查API是否已配置"""
        return bool(self.app_id and self.app_secret)


# 创建全局API客户端实例（需要配置后才能使用）
api_client = LotteryAPIClient()


def configure_api(app_id: str, app_secret: str):
    """
    配置API客户端
    
    Args:
        app_id: API应用ID
        app_secret: API密钥
    """
    global api_client
    api_client = LotteryAPIClient(app_id, app_secret)
    return api_client


def load_api_config(config_path: Path, logger: Optional[logging.Logger] = None) -> bool:
    """
    从配置文件加载API配置
    
    This function loads API credentials from a JSON configuration file and configures
    the global API client. The config file should contain:
    {
        "app_id": "your_app_id",
        "app_secret": "your_app_secret"
    }
    
    If the config file doesn't exist or is invalid, the system will fall back to
    using sample data for demonstration purposes.
    
    Args:
        config_path: API配置文件路径 (Path to the API config JSON file)
        logger: 日志记录器（可选）(Optional logger for status messages)
        
    Returns:
        是否成功加载配置 (True if config loaded successfully, False if using fallback)
    
    Example:
        >>> logger = setup_logger()
        >>> config_path = Path('api_config.json')
        >>> success = load_api_config(config_path, logger)
        >>> if success:
        ...     # API client is now configured with real credentials
        ...     pass
        ... else:
        ...     # Using sample data for demonstration
        ...     pass
    """
    try:
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                api_config = json.load(f)
                configure_api(api_config.get('app_id', ''), api_config.get('app_secret', ''))
                if logger:
                    logger.info("API client configured successfully")
                return True
        else:
            if logger:
                logger.warning(
                    f"API config file not found at {config_path}. Using sample data. "
                    f"Create {config_path.name} from {config_path.name}.example with your API credentials "
                    f"to enable real lottery data integration."
                )
            return False
    except Exception as e:
        if logger:
            logger.warning(f"Failed to configure API client: {e}. Using sample data.")
        return False


def get_api_client() -> LotteryAPIClient:
    """获取API客户端实例"""
    return api_client
