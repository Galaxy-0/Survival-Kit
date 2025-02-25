"""
GitHub监控模块单元测试
"""
import unittest
from unittest.mock import patch, MagicMock
from src.monitor.github_monitor import GitHubMonitor

class TestGitHubMonitor(unittest.TestCase):
    def setUp(self):
        """测试前准备"""
        self.monitor = GitHubMonitor()
        
    @patch('requests.get')
    def test_search_trending_repos(self, mock_get):
        """测试趋势项目搜索"""
        # 模拟API响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'items': [
                {
                    'id': 1,
                    'full_name': 'test/repo',
                    'description': 'Test repo',
                    'html_url': 'https://github.com/test/repo',
                    'stargazers_count': 1000,
                    'forks_count': 100,
                    'language': 'Python',
                    'created_at': '2024-01-01T00:00:00Z',
                    'updated_at': '2024-02-01T00:00:00Z',
                    'topics': ['ai', 'machine-learning'],
                    'open_issues_count': 10
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # 执行测试
        results = self.monitor.search_trending_repos()
        
        # 验证结果
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'test/repo')
        self.assertEqual(results[0]['stars'], 1000)
        
    @patch('requests.get')
    def test_analyze_repo_activity(self, mock_get):
        """测试仓库活跃度分析"""
        # 模拟API响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'total': 10, 'week': 1},
            {'total': 20, 'week': 2}
        ]
        mock_get.return_value = mock_response
        
        # 执行测试
        activity = self.monitor.analyze_repo_activity('test/repo')
        
        # 验证结果
        self.assertIn('total_commits', activity)
        self.assertIn('active_weeks', activity)
        self.assertEqual(activity['total_commits'], 30)
        
    def test_extract_repo_info(self):
        """测试仓库信息提取"""
        # 测试数据
        repo_data = {
            'id': 1,
            'full_name': 'test/repo',
            'description': 'Test repo',
            'html_url': 'https://github.com/test/repo',
            'stargazers_count': 1000,
            'forks_count': 100,
            'language': 'Python',
            'license': {'spdx_id': 'MIT'},
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-02-01T00:00:00Z',
            'topics': ['ai', 'machine-learning'],
            'open_issues_count': 10
        }
        
        # 执行测试
        result = self.monitor._extract_repo_info(repo_data)
        
        # 验证结果
        self.assertEqual(result['name'], 'test/repo')
        self.assertEqual(result['stars'], 1000)
        self.assertEqual(result['forks'], 100)
        self.assertEqual(result['language'], 'Python')
        self.assertEqual(result['license'], 'MIT')
        
    def test_save_results(self):
        """测试结果保存"""
        # 测试数据
        results = [
            {
                'name': 'test/repo',
                'stars': 1000,
                'forks': 100
            }
        ]
        
        # 执行测试
        self.monitor.save_results(results, 'test_results.json')
        
        # 验证文件是否创建（这里可以添加文件读取和内容验证）
        
if __name__ == '__main__':
    unittest.main() 