import pandas as pd
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional

class CashFlowManager:
    def __init__(self, config_path: str = 'config/finance_config.json'):
        self.config = self._load_config(config_path)
        self.transactions = []
        self.alerts = []
        
    def _load_config(self, config_path: str) -> Dict:
        """加载财务配置"""
        default_config = {
            'emergency_threshold': 5000,
            'warning_threshold': 10000,
            'allocation': {
                'tax': 0.2,
                'savings': 0.3,
                'operating': 0.3,
                'personal': 0.2
            }
        }
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return default_config
            
    def add_transaction(self, amount: float, category: str, description: str, date: Optional[str] = None):
        """添加交易记录"""
        if date is None:
            date = datetime.now().isoformat()
            
        transaction = {
            'date': date,
            'amount': amount,
            'category': category,
            'description': description
        }
        
        self.transactions.append(transaction)
        self._check_thresholds()
        
    def _check_thresholds(self):
        """检查是否触发预警阈值"""
        balance = self.get_current_balance()
        
        if balance < self.config['emergency_threshold']:
            self._add_alert('EMERGENCY', f'余额低于紧急阈值！当前余额: {balance}')
        elif balance < self.config['warning_threshold']:
            self._add_alert('WARNING', f'余额低于警告阈值！当前余额: {balance}')
            
    def _add_alert(self, level: str, message: str):
        """添加预警信息"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message
        }
        self.alerts.append(alert)
        
    def get_current_balance(self) -> float:
        """获取当前余额"""
        return sum(t['amount'] for t in self.transactions)
        
    def generate_monthly_report(self, year: int, month: int) -> Dict:
        """生成月度财务报告"""
        df = pd.DataFrame(self.transactions)
        df['date'] = pd.to_datetime(df['date'])
        
        # 筛选指定月份的数据
        monthly_data = df[
            (df['date'].dt.year == year) & 
            (df['date'].dt.month == month)
        ]
        
        # 收入支出统计
        income = monthly_data[monthly_data['amount'] > 0]['amount'].sum()
        expenses = abs(monthly_data[monthly_data['amount'] < 0]['amount'].sum())
        
        # 分类统计
        category_stats = monthly_data.groupby('category')['amount'].sum()
        
        return {
            'year': year,
            'month': month,
            'total_income': income,
            'total_expenses': expenses,
            'net_income': income - expenses,
            'category_breakdown': category_stats.to_dict(),
            'alert_count': len([a for a in self.alerts if a['timestamp'].startswith(f"{year}-{month:02d}")])
        }
        
    def predict_cash_flow(self, months: int = 3) -> List[Dict]:
        """预测未来现金流"""
        df = pd.DataFrame(self.transactions)
        df['date'] = pd.to_datetime(df['date'])
        
        # 计算月平均收支
        monthly_avg = df.groupby(
            [df['date'].dt.year, df['date'].dt.month]
        )['amount'].sum().mean()
        
        predictions = []
        current_balance = self.get_current_balance()
        
        for i in range(months):
            month_prediction = {
                'month': (datetime.now() + timedelta(days=30*i)).strftime('%Y-%m'),
                'predicted_balance': current_balance + monthly_avg * (i+1),
                'confidence': max(0.9 - (i * 0.1), 0.6)  # 预测信心随时间递减
            }
            predictions.append(month_prediction)
            
        return predictions
        
    def get_tax_estimation(self) -> Dict:
        """估算税务情况"""
        df = pd.DataFrame(self.transactions)
        
        # 计算应纳税所得额
        taxable_income = df[df['amount'] > 0]['amount'].sum()
        
        # 简单累进税率计算（示例）
        tax_rates = [
            (0, 36000, 0.03),
            (36000, 144000, 0.1),
            (144000, 300000, 0.2),
            (300000, 420000, 0.25),
            (420000, 660000, 0.3),
            (660000, 960000, 0.35),
            (960000, float('inf'), 0.45)
        ]
        
        estimated_tax = 0
        for lower, upper, rate in tax_rates:
            if taxable_income > lower:
                taxable_amount = min(taxable_income - lower, upper - lower)
                estimated_tax += taxable_amount * rate
                
        return {
            'taxable_income': taxable_income,
            'estimated_tax': estimated_tax,
            'effective_rate': estimated_tax / taxable_income if taxable_income > 0 else 0
        } 