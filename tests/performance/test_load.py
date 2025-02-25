"""
性能测试模块
"""
import unittest
import time
import concurrent.futures
from typing import List, Dict
from src.monitor.github_monitor import GitHubMonitor
from src.analyzer.project_analyzer import ProjectAnalyzer
from src.evaluator.monetization_evaluator import MonetizationEvaluator

class TestPerformance(unittest.TestCase):
    def setUp(self):
        """测试前准备"""
        self.monitor = GitHubMonitor()
        self.analyzer = ProjectAnalyzer()
        self.evaluator = MonetizationEvaluator()
        
    def test_monitor_performance(self):
        """测试监控模块性能"""
        start_time = time.time()
        
        # 执行监控
        results = self.monitor.search_trending_repos()
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # 验证性能指标
        self.assertLess(processing_time, 30, "监控模块处理时间超过30秒")
        self.assertGreater(len(results), 0, "没有找到任何项目")
        
    def test_analyzer_performance(self):
        """测试分析模块性能"""
        # 准备测试数据
        test_projects = self._generate_test_projects(100)
        
        start_time = time.time()
        
        # 执行分析
        results = self.analyzer.batch_analyze(test_projects)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # 验证性能指标
        self.assertLess(processing_time, 60, "分析模块处理时间超过60秒")
        self.assertEqual(len(results), 100, "部分项目未完成分析")
        
    def test_evaluator_performance(self):
        """测试评估模块性能"""
        # 准备测试数据
        test_analyses = self._generate_test_analyses(100)
        
        start_time = time.time()
        
        # 执行评估
        results = self.evaluator.batch_evaluate(test_analyses)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # 验证性能指标
        self.assertLess(processing_time, 45, "评估模块处理时间超过45秒")
        self.assertEqual(len(results), 100, "部分项目未完成评估")
        
    def test_parallel_processing(self):
        """测试并行处理性能"""
        # 准备测试数据
        test_projects = self._generate_test_projects(200)
        
        start_time = time.time()
        
        # 并行处理
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            # 将项目分成4批
            batch_size = len(test_projects) // 4
            batches = [test_projects[i:i + batch_size] for i in range(0, len(test_projects), batch_size)]
            
            # 并行执行分析
            future_to_batch = {executor.submit(self.analyzer.batch_analyze, batch): batch for batch in batches}
            
            # 收集结果
            results = []
            for future in concurrent.futures.as_completed(future_to_batch):
                results.extend(future.result())
                
        end_time = time.time()
        processing_time = end_time - start_time
        
        # 验证性能指标
        self.assertLess(processing_time, 120, "并行处理时间超过120秒")
        self.assertEqual(len(results), 200, "部分项目未完成处理")
        
    def test_memory_usage(self):
        """测试内存使用"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # 执行大量数据处理
        test_projects = self._generate_test_projects(500)
        _ = self.analyzer.batch_analyze(test_projects)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # 验证内存使用
        self.assertLess(memory_increase, 500, "内存使用增长超过500MB")
        
    def _generate_test_projects(self, count: int) -> List[Dict]:
        """生成测试项目数据"""
        return [
            {
                'id': i,
                'name': f'test/repo-{i}',
                'description': f'Test repository {i}',
                'stars': 1000 + i,
                'forks': 100 + i,
                'language': 'Python',
                'license': 'MIT',
                'created_at': '2024-01-01T00:00:00Z',
                'updated_at': '2024-02-01T00:00:00Z',
                'topics': ['ai', 'machine-learning'],
                'open_issues': 10
            }
            for i in range(count)
        ]
        
    def _generate_test_analyses(self, count: int) -> List[Dict]:
        """生成测试分析结果数据"""
        return [
            {
                'project_id': f'test/repo-{i}',
                'evaluation': {
                    'technical_score': 0.8,
                    'market_score': 0.7,
                    'monetization_score': 0.6,
                    'overall_score': 0.7
                }
            }
            for i in range(count)
        ]
        
if __name__ == '__main__':
    unittest.main() 