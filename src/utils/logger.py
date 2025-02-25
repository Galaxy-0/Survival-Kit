"""
日志工具模块
"""
import os
import logging
import logging.config

def setup_logger(name: str) -> logging.Logger:
    """
    设置并返回一个命名的日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    # 确保日志目录存在
    os.makedirs('logs', exist_ok=True)
    
    # 加载日志配置
    config_path = os.path.join('config', 'logging', 'logging.conf')
    if os.path.exists(config_path):
        logging.config.fileConfig(config_path)
    else:
        # 使用默认配置
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    return logging.getLogger(name) 