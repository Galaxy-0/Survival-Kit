import json
from typing import Dict, List, Optional
from datetime import datetime

class ProjectAnalyzer:
    def __init__(self):
        # 评分权重配置
        self.weights = {
            'technical': {
                'code_quality': 0.1,
                'activity': 0.1,
                'tech_stack': 0.1
            },
            'market': {
                'demand': 0.15,
                'competition': 0.1,
                'user_feedback': 0.15
            },
            'monetization': {
                'license': 0.1,
                'complexity': 0.1,
                'maintenance': 0.1
            }
        }
        
        # 许可证评分
        self.license_scores = {
            'MIT': 1.0,
            'Apache-2.0': 0.9,
            'BSD-3-Clause': 0.8,
            'GPL-3.0': 0.4,
            'AGPL-3.0': 0.3,
            'Unknown': 0.1
        }
        
        # 技术栈评分
        self.tech_stack_scores = {
            'Python': 0.9,
            'JavaScript': 0.8,
            'TypeScript': 0.85,
            'Java': 0.7,
            'Go': 0.8,
            'Rust': 0.75
        }
        
    def analyze_project(self, project_data: Dict) -> Dict:
        """分析项目并生成评分"""
        try:
            # 计算各维度得分
            technical_score = self._calculate_technical_score(project_data)
            market_score = self._calculate_market_score(project_data)
            monetization_score = self._calculate_monetization_score(project_data)
            
            # 计算总分
            overall_score = (
                technical_score * sum(self.weights['technical'].values()) +
                market_score * sum(self.weights['market'].values()) +
                monetization_score * sum(self.weights['monetization'].values())
            )
            
            # 生成变现路径建议
            monetization_paths = self._suggest_monetization_paths(project_data)
            
            return {
                'project_id': project_data['name'],
                'evaluation': {
                    'technical_score': round(technical_score, 2),
                    'market_score': round(market_score, 2),
                    'monetization_score': round(monetization_score, 2),
                    'overall_score': round(overall_score, 2)
                },
                'monetization_paths': monetization_paths,
                'recommendations': self._generate_recommendations(project_data)
            }
            
        except Exception as e:
            print(f"Error analyzing project {project_data.get('name', 'unknown')}: {str(e)}")
            return {}
            
    def _calculate_technical_score(self, project: Dict) -> float:
        """计算技术维度得分"""
        # 代码质量得分
        code_quality = min(1.0, (project['stars'] / 1000) * 0.7 + (project['forks'] / 200) * 0.3)
        
        # 活跃度得分
        activity = project.get('activity', {})
        activity_score = activity.get('activity_score', 0)
        
        # 技术栈得分
        tech_stack = self.tech_stack_scores.get(project['language'], 0.5)
        
        return (
            code_quality * self.weights['technical']['code_quality'] +
            activity_score * self.weights['technical']['activity'] +
            tech_stack * self.weights['technical']['tech_stack']
        ) / sum(self.weights['technical'].values())
        
    def _calculate_market_score(self, project: Dict) -> float:
        """计算市场维度得分"""
        # 市场需求得分（基于stars和forks）
        demand = min(1.0, (project['stars'] / 5000) * 0.6 + (project['forks'] / 1000) * 0.4)
        
        # 竞争情况（基于类似项目数量，这里使用简化计算）
        competition = 0.7  # 默认中等竞争
        
        # 用户反馈（基于issues）
        issues = project.get('issues', {})
        if issues:
            total_issues = issues.get('open_issues_count', 0) + issues.get('closed_issues_count', 0)
            if total_issues > 0:
                resolution_rate = issues.get('closed_issues_count', 0) / total_issues
                user_feedback = min(1.0, resolution_rate * 0.7 + 0.3)
            else:
                user_feedback = 0.5
        else:
            user_feedback = 0.5
            
        return (
            demand * self.weights['market']['demand'] +
            competition * self.weights['market']['competition'] +
            user_feedback * self.weights['market']['user_feedback']
        ) / sum(self.weights['market'].values())
        
    def _calculate_monetization_score(self, project: Dict) -> float:
        """计算变现维度得分"""
        # 许可证评分
        license_score = self.license_scores.get(project['license'], 0.1)
        
        # 复杂度评分（基于项目规模和依赖）
        complexity = 0.7  # 默认中等复杂度
        
        # 维护成本（基于活跃度和问题数量）
        activity = project.get('activity', {})
        maintenance_score = 1.0 - (activity.get('activity_score', 0.5) * 0.5)  # 活跃度越高，维护成本越高
        
        return (
            license_score * self.weights['monetization']['license'] +
            complexity * self.weights['monetization']['complexity'] +
            maintenance_score * self.weights['monetization']['maintenance']
        ) / sum(self.weights['monetization'].values())
        
    def _suggest_monetization_paths(self, project: Dict) -> List[Dict]:
        """生成变现路径建议"""
        paths = []
        
        # 分析项目特征
        is_tool = any(kw in str(project.get('topics', [])).lower() for kw in ['tool', 'utility', 'automation'])
        is_api = any(kw in str(project.get('topics', [])).lower() for kw in ['api', 'service', 'server'])
        is_ui = any(kw in str(project.get('topics', [])).lower() for kw in ['ui', 'frontend', 'web'])
        
        # 根据特征推荐变现路径
        if is_tool:
            paths.append({
                'type': 'SaaS',
                'difficulty': 'medium',
                'estimated_time': '2-3 months',
                'potential_revenue': 'high',
                'description': '将工具转化为在线服务，提供免费和付费版本'
            })
            
        if is_api:
            paths.append({
                'type': 'API Service',
                'difficulty': 'low',
                'estimated_time': '1-2 months',
                'potential_revenue': 'medium',
                'description': '提供API即服务，按调用次数收费'
            })
            
        if is_ui:
            paths.append({
                'type': 'Premium Template',
                'difficulty': 'low',
                'estimated_time': '2-4 weeks',
                'potential_revenue': 'medium',
                'description': '开发高级主题和模板进行销售'
            })
            
        # 通用变现路径
        paths.append({
            'type': 'Support & Consulting',
            'difficulty': 'medium',
            'estimated_time': 'ongoing',
            'potential_revenue': 'variable',
            'description': '提供技术支持和咨询服务'
        })
        
        return paths
        
    def _generate_recommendations(self, project: Dict) -> List[str]:
        """生成具体建议"""
        recommendations = []
        
        # 许可证建议
        if project['license'] == 'Unknown':
            recommendations.append("添加明确的开源许可证（建议使用MIT或Apache 2.0）")
            
        # 文档建议
        if 'documentation' not in str(project.get('topics', [])).lower():
            recommendations.append("完善项目文档，特别是快速启动指南")
            
        # 部署建议
        if 'docker' not in str(project.get('topics', [])).lower():
            recommendations.append("添加Docker支持，简化部署流程")
            
        # 功能建议
        recommendations.append("开发企业版功能，如高级配置、批量处理等")
        
        # 社区建议
        if project.get('activity', {}).get('activity_score', 0) < 0.5:
            recommendations.append("提高项目活跃度，定期更新和维护")
            
        return recommendations
        
    def save_analysis(self, analysis: Dict, filename: str = 'data/project_analysis.json'):
        """保存分析结果"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'analysis': analysis
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving analysis: {str(e)}")
            
    def batch_analyze(self, projects: List[Dict]) -> List[Dict]:
        """批量分析项目"""
        results = []
        for project in projects:
            analysis = self.analyze_project(project)
            if analysis:
                results.append(analysis)
                
        # 按总分排序
        results.sort(
            key=lambda x: x.get('evaluation', {}).get('overall_score', 0),
            reverse=True
        )
        
        return results

if __name__ == "__main__":
    # 测试分析器
    analyzer = ProjectAnalyzer()
    
    # 读取监控数据
    try:
        with open('data/github_trends.json', 'r', encoding='utf-8') as f:
            monitored_data = json.load(f)
            results = analyzer.batch_analyze(monitored_data.get('results', []))
            analyzer.save_analysis(results)
            print(f"分析完成，发现 {len(results)} 个潜在项目")
    except Exception as e:
        print(f"Error reading monitored data: {str(e)}") 