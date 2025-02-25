from flask import Flask, render_template, jsonify, request
from src.automation.platform_monitor import PlatformMonitor
from src.crm.client_manager import ClientManager
from src.finance.cash_flow_manager import CashFlowManager
import threading
import os

app = Flask(__name__)

# 初始化各个管理器
platform_monitor = PlatformMonitor()
client_manager = ClientManager()
cash_flow_manager = CashFlowManager()

# 启动平台监控
monitor_thread = threading.Thread(target=platform_monitor.run_schedule, daemon=True)
monitor_thread.start()

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@app.route('/api/opportunities')
def get_opportunities():
    """获取最新机会"""
    return jsonify(platform_monitor.check_opportunities())

@app.route('/api/clients')
def get_clients():
    """获取客户列表"""
    return jsonify(client_manager.generate_report())

@app.route('/api/finance/summary')
def get_finance_summary():
    """获取财务摘要"""
    current_balance = cash_flow_manager.get_current_balance()
    predictions = cash_flow_manager.predict_cash_flow()
    tax_info = cash_flow_manager.get_tax_estimation()
    
    return jsonify({
        'current_balance': current_balance,
        'predictions': predictions,
        'tax_estimation': tax_info
    })

@app.route('/api/alerts')
def get_alerts():
    """获取所有预警信息"""
    all_alerts = []
    
    # 合并来自不同模块的预警
    if hasattr(cash_flow_manager, 'alerts'):
        all_alerts.extend(cash_flow_manager.alerts)
        
    return jsonify(all_alerts)

if __name__ == '__main__':
    app.run(debug=True) 