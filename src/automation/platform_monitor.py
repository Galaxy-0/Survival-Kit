import os
import schedule
import time
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

class PlatformMonitor:
    def __init__(self):
        self.platforms = {
            'upwork': os.getenv('UPWORK_API_KEY'),
            'fiverr': os.getenv('FIVERR_API_KEY'),
            'github': os.getenv('GITHUB_TOKEN')
        }
        self.keywords = ['AI', 'Python', 'Automation', 'Data Analysis']
        
    def check_opportunities(self):
        """检查各平台的机会"""
        opportunities = []
        for platform, api_key in self.platforms.items():
            if api_key:
                try:
                    platform_opps = self._fetch_platform_data(platform)
                    opportunities.extend(platform_opps)
                except Exception as e:
                    print(f"Error checking {platform}: {str(e)}")
        return opportunities
    
    def _fetch_platform_data(self, platform):
        """获取特定平台数据"""
        if platform == 'github':
            return self._check_github_trends()
        elif platform == 'upwork':
            return self._check_upwork_jobs()
        return []
    
    def _check_github_trends(self):
        """检查GitHub趋势项目"""
        url = "https://api.github.com/search/repositories"
        headers = {"Authorization": f"token {self.platforms['github']}"}
        
        trends = []
        for keyword in self.keywords:
            params = {
                'q': f'{keyword} in:name,description',
                'sort': 'stars',
                'order': 'desc'
            }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                trends.extend(data.get('items', [])[:5])
        
        return trends
    
    def _check_upwork_jobs(self):
        """检查Upwork最新任务"""
        # 实现Upwork API调用
        # 需要根据实际API文档实现
        return []

    def run_schedule(self):
        """运行定时任务"""
        schedule.every(1).hours.do(self.check_opportunities)
        
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    monitor = PlatformMonitor()
    monitor.run_schedule() 