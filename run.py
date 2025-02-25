"""
主运行脚本
"""
import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.survival_kit import SurvivalKit
from src.utils.logger import setup_logger

logger = setup_logger('main')

def main():
    """主函数"""
    try:
        # 确保在正确的目录
        os.chdir(project_root)
        
        # 运行主程序
        logger.info("启动Survival-Kit...")
        kit = SurvivalKit()
        kit.run()
        
    except Exception as e:
        logger.error(f"运行出错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 