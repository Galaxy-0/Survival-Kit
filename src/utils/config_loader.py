"""
配置加载工具
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

def load_config() -> Dict[str, Any]:
    """
    加载配置信息
    
    Returns:
        Dict[str, Any]: 配置信息字典
    """
    # 加载环境变量
    load_dotenv()
    
    # 从环境变量获取配置
    config = {
        'github_token': os.getenv('GITHUB_TOKEN'),
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'min_stars': int(os.getenv('MIN_STARS', 100)),
        'min_forks': int(os.getenv('MIN_FORKS', 20)),
        'days_since_update': int(os.getenv('DAYS_SINCE_UPDATE', 30)),
        'min_revenue_threshold': int(os.getenv('MIN_REVENUE_THRESHOLD', 500)),
        'roi_period_threshold': int(os.getenv('ROI_PERIOD_THRESHOLD', 6)),
        'data_dir': os.getenv('DATA_DIR', 'data'),
        'log_dir': os.getenv('LOG_DIR', 'logs')
    }
    
    # 验证必要的配置
    required_configs = ['github_token']
    missing_configs = [key for key in required_configs if not config.get(key)]
    if missing_configs:
        raise ValueError(f"缺少必要的配置项: {', '.join(missing_configs)}")
    
    return config 