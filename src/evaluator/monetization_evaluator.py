import json
from typing import Dict, List, Optional
from datetime import datetime
import requests
from bs4 import BeautifulSoup

class MonetizationEvaluator:
    def __init__(self):
        # 变现模式评分标准
        self.monetization_models = {
            'SaaS': {
                'min_revenue': 500,
                'setup_time': 60,  # 天
                'maintenance_cost': 0.3,  # 收入比例
                'scalability': 0.9,
                'passive_income': 0.8
            },
            'API_Service': {
                'min_revenue': 300,
                'setup_time': 30,
                'maintenance_cost': 0.2,
                'scalability': 0.8,
                'passive_income': 0.7
            },
            'Premium_Template': {
                'min_revenue': 200,
                'setup_time': 14,
                'maintenance_cost': 0.1,
                'scalability': 0.6,
                'passive_income': 0.9
            },
            'Support_Consulting': {
                'min_revenue': 1000,
                'setup_time': 7,
                'maintenance_cost': 0.5,
                'scalability': 0.4,
                'passive_income': 0.2
            }
        }
        
        # 市场平台评分
        self.platform_scores = {
            'gumroad': 0.9,
            'github_marketplace': 0.8,
            'producthunt': 0.7,
            'chrome_store': 0.75
        }
        
    def evaluate_monetization(self, project_analysis: Dict) -> Dict:
        """评估项目的变现潜力"""
        try:
            # 获取基础评分
            base_score = project_analysis['evaluation']['monetization_score']
            
            # 评估每个变现路径
            evaluated_paths = []
            for path in project_analysis.get('monetization_paths', []):
                path_evaluation = self._evaluate_path(path, base_score)
                if path_evaluation:
                    evaluated_paths.append(path_evaluation)
                    
            # 选择最佳变现路径
            best_path = max(evaluated_paths, key=lambda x: x['potential_monthly_revenue'])
            
            return {
                'project_id': project_analysis['project_id'],
                'monetization_potential': {
                    'score': base_score,
                    'evaluated_paths': evaluated_paths,
                    'recommended_path': best_path,
                    'estimated_setup_cost': self._estimate_setup_cost(best_path),
                    'market_analysis': self._analyze_market(project_analysis)
                }
            }
            
        except Exception as e:
            print(f"Error evaluating monetization for {project_analysis.get('project_id', 'unknown')}: {str(e)}")
            return {}
            
    def _evaluate_path(self, path: Dict, base_score: float) -> Optional[Dict]:
        """评估具体变现路径"""
        try:
            path_type = path['type'].replace(' ', '_')
            model = self.monetization_models.get(path_type)
            
            if not model:
                return None
                
            # 计算潜在月收入
            potential_monthly_revenue = self._calculate_potential_revenue(
                model['min_revenue'],
                base_score,
                model['scalability']
            )
            
            # 计算净收入（考虑维护成本）
            net_monthly_revenue = potential_monthly_revenue * (1 - model['maintenance_cost'])
            
            # 计算投资回报周期
            roi_period = self._calculate_roi_period(
                setup_cost=self._estimate_setup_cost({'type': path_type}),
                monthly_revenue=net_monthly_revenue
            )
            
            return {
                'type': path['type'],
                'difficulty': path['difficulty'],
                'setup_time_days': model['setup_time'],
                'potential_monthly_revenue': round(potential_monthly_revenue, 2),
                'net_monthly_revenue': round(net_monthly_revenue, 2),
                'maintenance_cost_percentage': model['maintenance_cost'] * 100,
                'scalability_score': model['scalability'],
                'passive_income_potential': model['passive_income'],
                'roi_period_months': round(roi_period, 1),
                'recommended_platforms': self._recommend_platforms(path_type)
            }
            
        except Exception as e:
            print(f"Error evaluating path {path.get('type', 'unknown')}: {str(e)}")
            return None
            
    def _calculate_potential_revenue(self, base_revenue: float, score: float, scalability: float) -> float:
        """计算潜在月收入"""
        market_factor = 1 + (score - 0.5) * 2  # 将评分转换为市场因子
        scale_factor = 1 + scalability * 0.5  # 可扩展性影响
        return base_revenue * market_factor * scale_factor
        
    def _estimate_setup_cost(self, path: Dict) -> Dict:
        """估算启动成本"""
        base_costs = {
            'SaaS': {
                'development': 3000,
                'infrastructure': 500,
                'marketing': 1000
            },
            'API_Service': {
                'development': 2000,
                'infrastructure': 300,
                'marketing': 700
            },
            'Premium_Template': {
                'development': 1000,
                'infrastructure': 100,
                'marketing': 500
            },
            'Support_Consulting': {
                'development': 500,
                'infrastructure': 100,
                'marketing': 300
            }
        }
        
        path_type = path['type'].replace(' ', '_')
        costs = base_costs.get(path_type, {})
        
        return {
            'development_cost': costs.get('development', 0),
            'infrastructure_cost': costs.get('infrastructure', 0),
            'marketing_cost': costs.get('marketing', 0),
            'total_cost': sum(costs.values())
        }
        
    def _calculate_roi_period(self, setup_cost: Dict, monthly_revenue: float) -> float:
        """计算投资回报周期（月）"""
        total_cost = setup_cost['total_cost']
        return total_cost / monthly_revenue if monthly_revenue > 0 else float('inf')
        
    def _recommend_platforms(self, path_type: str) -> List[Dict]:
        """推荐销售平台"""
        platforms = []
        
        if path_type == 'SaaS':
            platforms.extend([
                {'name': 'gumroad', 'score': self.platform_scores['gumroad']},
                {'name': 'github_marketplace', 'score': self.platform_scores['github_marketplace']}
            ])
        elif path_type == 'Premium_Template':
            platforms.extend([
                {'name': 'gumroad', 'score': self.platform_scores['gumroad']},
                {'name': 'producthunt', 'score': self.platform_scores['producthunt']}
            ])
            
        return sorted(platforms, key=lambda x: x['score'], reverse=True)
        
    def _analyze_market(self, project_analysis: Dict) -> Dict:
        """分析市场情况"""
        return {
            'market_size': 'medium',  # 可以通过API获取更准确的市场规模数据
            'competition_level': 'moderate',
            'growth_potential': 'high' if project_analysis['evaluation']['market_score'] > 0.7 else 'medium',
            'target_audience': self._identify_target_audience(project_analysis)
        }
        
    def _identify_target_audience(self, project_analysis: Dict) -> List[str]:
        """识别目标用户群体"""
        audiences = []
        topics = project_analysis.get('topics', [])
        
        if 'enterprise' in str(topics).lower():
            audiences.append('Enterprise')
        if 'developer-tools' in str(topics).lower():
            audiences.append('Developers')
        if 'automation' in str(topics).lower():
            audiences.append('DevOps')
            
        return audiences or ['General Developers']
        
    def save_evaluation(self, evaluation: Dict, filename: str = 'data/monetization_evaluation.json'):
        """保存评估结果"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'evaluation': evaluation
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving evaluation: {str(e)}")
            
    def batch_evaluate(self, analyzed_projects: List[Dict]) -> List[Dict]:
        """批量评估项目"""
        results = []
        for project in analyzed_projects:
            evaluation = self.evaluate_monetization(project)
            if evaluation:
                results.append(evaluation)
                
        # 按潜在收入排序
        results.sort(
            key=lambda x: x.get('monetization_potential', {})
                         .get('recommended_path', {})
                         .get('potential_monthly_revenue', 0),
            reverse=True
        )
        
        return results

if __name__ == "__main__":
    # 测试评估器
    evaluator = MonetizationEvaluator()
    
    # 读取分析数据
    try:
        with open('data/project_analysis.json', 'r', encoding='utf-8') as f:
            analyzed_data = json.load(f)
            results = evaluator.batch_evaluate(analyzed_data.get('analysis', []))
            evaluator.save_evaluation(results)
            print(f"评估完成，处理了 {len(results)} 个项目")
    except Exception as e:
        print(f"Error reading project analysis: {str(e)}") 