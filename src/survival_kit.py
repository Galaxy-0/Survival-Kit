"""
主监控模块
"""
import os
import json
import time
from datetime import datetime
from typing import Dict, List
from src.monitor.github_monitor import GitHubMonitor
from src.analyzer.project_analyzer import ProjectAnalyzer
from src.evaluator.monetization_evaluator import MonetizationEvaluator
from src.utils.logger import setup_logger

logger = setup_logger('monitor')

class SurvivalKit:
    def __init__(self):
        self.monitor = GitHubMonitor()
        self.analyzer = ProjectAnalyzer()
        self.evaluator = MonetizationEvaluator()
        
        # 确保数据目录存在
        os.makedirs('data', exist_ok=True)
        
    def run(self):
        """运行完整的项目发现和评估流程"""
        logger.info("启动生存工具箱...")
        
        try:
            # 1. 监控GitHub项目
            logger.info("1. 开始监控GitHub项目...")
            monitored_projects = self.monitor.run_monitor()
            logger.info(f"发现 {len(monitored_projects)} 个潜在项目")
            
            if not monitored_projects:
                logger.warning("未发现符合条件的项目，请调整搜索条件后重试")
                return
                
            # 2. 分析项目
            logger.info("2. 开始分析项目...")
            analyzed_projects = self.analyzer.batch_analyze(monitored_projects)
            logger.info(f"完成 {len(analyzed_projects)} 个项目的分析")
            
            if not analyzed_projects:
                logger.error("项目分析失败，请检查分析器配置")
                return
                
            # 3. 评估变现潜力
            logger.info("3. 评估变现潜力...")
            evaluated_projects = self.evaluator.batch_evaluate(analyzed_projects)
            logger.info(f"完成 {len(evaluated_projects)} 个项目的变现评估")
            
            if not evaluated_projects:
                logger.error("变现评估失败，请检查评估器配置")
                return
                
            # 4. 生成报告
            self._generate_report(evaluated_projects)
            
        except Exception as e:
            logger.error(f"运行过程中发生错误: {str(e)}")
            raise
            
    def _generate_report(self, evaluated_projects: List[Dict]):
        """生成综合报告"""
        try:
            # 按变现潜力排序
            top_projects = sorted(
                evaluated_projects,
                key=lambda x: x.get('monetization_potential', {})
                           .get('recommended_path', {})
                           .get('potential_monthly_revenue', 0),
                reverse=True
            )[:5]  # 只取前5个项目
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'total_projects_analyzed': len(evaluated_projects),
                    'top_opportunities': len(top_projects)
                },
                'top_projects': top_projects,
                'recommendations': self._generate_recommendations(top_projects)
            }
            
            # 保存报告
            with open('data/opportunity_report.json', 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
                
            # 打印报告摘要
            self._print_report_summary(report)
            
        except Exception as e:
            logger.error(f"生成报告时发生错误: {str(e)}")
            raise
            
    def _generate_recommendations(self, top_projects: List[Dict]) -> List[Dict]:
        """生成行动建议"""
        recommendations = []
        
        for project in top_projects:
            monetization = project.get('monetization_potential', {})
            recommended_path = monetization.get('recommended_path', {})
            
            recommendations.append({
                'project_id': project['project_id'],
                'recommended_action': {
                    'path': recommended_path.get('type'),
                    'estimated_revenue': recommended_path.get('potential_monthly_revenue'),
                    'setup_time': recommended_path.get('setup_time_days'),
                    'next_steps': [
                        f"1. 克隆项目并评估代码质量",
                        f"2. 预计开发时间: {recommended_path.get('setup_time_days')} 天",
                        f"3. 预算投入: ${monetization.get('estimated_setup_cost', {}).get('total_cost', 0)}",
                        f"4. 选择平台: {', '.join([p['name'] for p in recommended_path.get('recommended_platforms', [])])}"
                    ]
                }
            })
            
        return recommendations
        
    def _print_report_summary(self, report: Dict):
        """打印报告摘要"""
        logger.info("\n=== 机会报告摘要 ===")
        logger.info(f"分析时间: {datetime.fromisoformat(report['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"分析项目总数: {report['summary']['total_projects_analyzed']}")
        logger.info(f"高潜力机会: {report['summary']['top_opportunities']}")
        
        logger.info("\n--- 顶级项目 ---")
        for project in report['top_projects']:
            monetization = project['monetization_potential']
            recommended_path = monetization['recommended_path']
            
            logger.info(f"\n项目: {project['project_id']}")
            logger.info(f"推荐变现路径: {recommended_path['type']}")
            logger.info(f"预计月收入: ${recommended_path['potential_monthly_revenue']}")
            logger.info(f"启动时间: {recommended_path['setup_time_days']} 天")
            logger.info(f"投资回报周期: {recommended_path['roi_period_months']} 个月")
            
        logger.info("\n完整报告已保存至 data/opportunity_report.json")

def main():
    kit = SurvivalKit()
    kit.run()

if __name__ == "__main__":
    main() 