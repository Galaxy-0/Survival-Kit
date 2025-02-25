"""
工作流集成测试
"""
import unittest
import os
import json
from src.monitor import SurvivalKit

class TestWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """测试前准备"""
        # 确保环境变量设置正确
        assert 'GITHUB_TOKEN' in os.environ, "需要设置GITHUB_TOKEN环境变量"
        
        # 创建必要的目录
        os.makedirs('data', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        
        # 初始化SurvivalKit
        cls.kit = SurvivalKit()
        
    def test_full_workflow(self):
        """测试完整工作流程"""
        # 运行完整流程
        self.kit.run()
        
        # 验证生成的文件
        self.assertTrue(os.path.exists('data/github_trends.json'))
        self.assertTrue(os.path.exists('data/project_analysis.json'))
        self.assertTrue(os.path.exists('data/monetization_evaluation.json'))
        self.assertTrue(os.path.exists('data/opportunity_report.json'))
        
        # 验证数据完整性
        with open('data/opportunity_report.json', 'r') as f:
            report = json.load(f)
            self.assertIn('timestamp', report)
            self.assertIn('summary', report)
            self.assertIn('top_projects', report)
            
    def test_data_consistency(self):
        """测试数据一致性"""
        # 读取所有生成的数据文件
        with open('data/github_trends.json', 'r') as f:
            trends = json.load(f)
            
        with open('data/project_analysis.json', 'r') as f:
            analysis = json.load(f)
            
        with open('data/monetization_evaluation.json', 'r') as f:
            evaluation = json.load(f)
            
        # 验证数据流转
        trend_projects = set(p['name'] for p in trends.get('results', []))
        analyzed_projects = set(p['project_id'] for p in analysis.get('analysis', []))
        evaluated_projects = set(p['project_id'] for p in evaluation.get('evaluation', []))
        
        # 确保没有项目在流程中丢失
        self.assertTrue(analyzed_projects.issubset(trend_projects))
        self.assertTrue(evaluated_projects.issubset(analyzed_projects))
        
    def test_error_handling(self):
        """测试错误处理"""
        # 测试无效的GitHub Token
        original_token = os.environ.get('GITHUB_TOKEN')
        os.environ['GITHUB_TOKEN'] = 'invalid_token'
        
        try:
            self.kit.run()
            self.fail("应该抛出异常")
        except Exception as e:
            self.assertIn("API", str(e))
        finally:
            # 恢复环境
            if original_token:
                os.environ['GITHUB_TOKEN'] = original_token
                
    def test_performance(self):
        """测试性能"""
        import time
        
        # 记录开始时间
        start_time = time.time()
        
        # 运行完整流程
        self.kit.run()
        
        # 计算总耗时
        total_time = time.time() - start_time
        
        # 验证性能要求（假设要求5分钟内完成）
        self.assertLess(total_time, 300, "处理时间超过5分钟")
        
    @classmethod
    def tearDownClass(cls):
        """测试后清理"""
        # 清理测试生成的文件
        test_files = [
            'data/github_trends.json',
            'data/project_analysis.json',
            'data/monetization_evaluation.json',
            'data/opportunity_report.json'
        ]
        
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
                
if __name__ == '__main__':
    unittest.main() 