import json
from datetime import datetime, timedelta
import pandas as pd

class ClientManager:
    def __init__(self, db_path='data/clients.json'):
        self.db_path = db_path
        self.clients = self._load_clients()
        
    def _load_clients(self):
        """从JSON文件加载客户数据"""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
            
    def _save_clients(self):
        """保存客户数据到JSON文件"""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.clients, f, ensure_ascii=False, indent=2)
            
    def add_client(self, client_id, info):
        """添加新客户"""
        if client_id not in self.clients:
            self.clients[client_id] = {
                'info': info,
                'projects': [],
                'created_at': datetime.now().isoformat(),
                'last_contact': datetime.now().isoformat(),
                'status': 'active'
            }
            self._save_clients()
            return True
        return False
        
    def update_client(self, client_id, info):
        """更新客户信息"""
        if client_id in self.clients:
            self.clients[client_id]['info'].update(info)
            self.clients[client_id]['last_contact'] = datetime.now().isoformat()
            self._save_clients()
            return True
        return False
        
    def add_project(self, client_id, project_info):
        """添加项目记录"""
        if client_id in self.clients:
            project = {
                'id': len(self.clients[client_id]['projects']) + 1,
                'info': project_info,
                'status': 'active',
                'created_at': datetime.now().isoformat()
            }
            self.clients[client_id]['projects'].append(project)
            self._save_clients()
            return project['id']
        return None
        
    def get_inactive_clients(self, days=30):
        """获取长期未联系的客户"""
        inactive = []
        now = datetime.now()
        for client_id, data in self.clients.items():
            last_contact = datetime.fromisoformat(data['last_contact'])
            if (now - last_contact).days >= days:
                inactive.append(client_id)
        return inactive
        
    def generate_report(self):
        """生成客户分析报告"""
        df = pd.DataFrame.from_dict(self.clients, orient='index')
        
        # 基础统计
        total_clients = len(df)
        active_projects = sum(len(c['projects']) for c in self.clients.values())
        
        # 客户来源分析
        sources = df['info'].apply(lambda x: x.get('source', 'unknown')).value_counts()
        
        return {
            'total_clients': total_clients,
            'active_projects': active_projects,
            'client_sources': sources.to_dict()
        }
        
    def predict_churn_risk(self, client_id):
        """预测客户流失风险"""
        if client_id in self.clients:
            client = self.clients[client_id]
            last_contact = datetime.fromisoformat(client['last_contact'])
            days_since_contact = (datetime.now() - last_contact).days
            
            # 简单风险评估逻辑
            risk_factors = {
                'days_inactive': min(days_since_contact / 30, 1.0),  # 超过30天算高风险
                'project_completion': len([p for p in client['projects'] if p['status'] == 'completed']) / max(len(client['projects']), 1),
                'communication_frequency': 1.0 if days_since_contact > 14 else 0.0  # 两周未联系算高风险
            }
            
            risk_score = sum(risk_factors.values()) / len(risk_factors)
            return {
                'score': risk_score,
                'level': 'high' if risk_score > 0.7 else 'medium' if risk_score > 0.3 else 'low',
                'factors': risk_factors
            }
        return None 