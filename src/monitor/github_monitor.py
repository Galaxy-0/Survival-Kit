import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class GitHubMonitor:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.headers = {'Authorization': f'token {self.github_token}'}
        self.base_url = "https://api.github.com"
        
        # 监控配置
        self.min_stars = 100
        self.min_forks = 20
        self.days_since_update = 30
        
        # 关键词配置
        self.keywords = [
            'ai', 'machine-learning', 'automation',
            'saas', 'api', 'sdk', 'chrome-extension',
            'discord-bot', 'telegram-bot', 'web3'
        ]
        
    def search_trending_repos(self) -> List[Dict]:
        """搜索趋势项目"""
        trending_repos = []
        
        for keyword in self.keywords:
            query = f"{keyword} stars:>{self.min_stars} forks:>{self.min_forks} pushed:>{self.days_since_update}d"
            url = f"{self.base_url}/search/repositories"
            params = {
                'q': query,
                'sort': 'stars',
                'order': 'desc'
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                for repo in data.get('items', []):
                    repo_info = self._extract_repo_info(repo)
                    if repo_info:
                        trending_repos.append(repo_info)
                        
            except Exception as e:
                print(f"Error searching for {keyword}: {str(e)}")
                
        return trending_repos
    
    def _extract_repo_info(self, repo: Dict) -> Optional[Dict]:
        """提取仓库信息"""
        try:
            return {
                'id': repo['id'],
                'name': repo['full_name'],
                'description': repo['description'],
                'url': repo['html_url'],
                'stars': repo['stargazers_count'],
                'forks': repo['forks_count'],
                'language': repo['language'],
                'license': repo.get('license', {}).get('spdx_id', 'Unknown'),
                'created_at': repo['created_at'],
                'updated_at': repo['updated_at'],
                'topics': repo.get('topics', []),
                'open_issues': repo['open_issues_count']
            }
        except KeyError:
            return None
            
    def analyze_repo_activity(self, repo_name: str) -> Dict:
        """分析仓库活跃度"""
        url = f"{self.base_url}/repos/{repo_name}/stats/commit_activity"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            # 计算最近一年的提交活跃度
            total_commits = sum(week['total'] for week in data)
            active_weeks = sum(1 for week in data if week['total'] > 0)
            
            return {
                'total_commits': total_commits,
                'active_weeks': active_weeks,
                'avg_weekly_commits': total_commits / 52 if data else 0,
                'activity_score': active_weeks / 52 if data else 0
            }
        except Exception as e:
            print(f"Error analyzing activity for {repo_name}: {str(e)}")
            return {}
            
    def get_repo_contributors(self, repo_name: str) -> List[Dict]:
        """获取贡献者信息"""
        url = f"{self.base_url}/repos/{repo_name}/contributors"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            contributors = response.json()
            
            return [{
                'username': c['login'],
                'contributions': c['contributions'],
                'profile': c['html_url']
            } for c in contributors[:10]]  # 只获取前10名贡献者
        except Exception as e:
            print(f"Error getting contributors for {repo_name}: {str(e)}")
            return []
            
    def get_repo_issues(self, repo_name: str) -> Dict:
        """分析问题和PR情况"""
        issues_url = f"{self.base_url}/repos/{repo_name}/issues"
        pulls_url = f"{self.base_url}/repos/{repo_name}/pulls"
        
        try:
            # 获取问题
            issues_response = requests.get(
                issues_url,
                headers=self.headers,
                params={'state': 'all', 'per_page': 100}
            )
            issues_response.raise_for_status()
            issues = issues_response.json()
            
            # 获取PR
            pulls_response = requests.get(
                pulls_url,
                headers=self.headers,
                params={'state': 'all', 'per_page': 100}
            )
            pulls_response.raise_for_status()
            pulls = pulls_response.json()
            
            # 分析问题和PR的状态
            return {
                'open_issues_count': len([i for i in issues if i['state'] == 'open']),
                'closed_issues_count': len([i for i in issues if i['state'] == 'closed']),
                'open_pulls_count': len([p for p in pulls if p['state'] == 'open']),
                'merged_pulls_count': len([p for p in pulls if p['state'] == 'closed'])
            }
        except Exception as e:
            print(f"Error analyzing issues for {repo_name}: {str(e)}")
            return {}
            
    def save_results(self, results: List[Dict], filename: str = 'data/github_trends.json'):
        """保存监控结果"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'results': results
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving results: {str(e)}")
            
    def run_monitor(self):
        """运行监控流程"""
        print("开始监控GitHub趋势项目...")
        
        # 获取趋势项目
        trending_repos = self.search_trending_repos()
        
        # 深入分析每个项目
        detailed_results = []
        for repo in trending_repos:
            repo_name = repo['name']
            print(f"分析项目: {repo_name}")
            
            # 获取详细信息
            activity = self.analyze_repo_activity(repo_name)
            contributors = self.get_repo_contributors(repo_name)
            issues = self.get_repo_issues(repo_name)
            
            # 合并信息
            detailed_info = {
                **repo,
                'activity': activity,
                'contributors': contributors,
                'issues': issues
            }
            
            detailed_results.append(detailed_info)
            
        # 保存结果
        self.save_results(detailed_results)
        print(f"监控完成，发现 {len(detailed_results)} 个潜在项目")
        
        return detailed_results

if __name__ == "__main__":
    monitor = GitHubMonitor()
    monitor.run_monitor() 