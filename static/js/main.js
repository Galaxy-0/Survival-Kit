// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 定期刷新数据
    setInterval(refreshData, 60000); // 每分钟刷新一次
    refreshData(); // 初始加载
});

// 刷新所有数据
function refreshData() {
    fetchAlerts();
    fetchOpportunities();
    fetchFinanceSummary();
    fetchClients();
}

// 获取预警信息
function fetchAlerts() {
    fetch('/api/alerts')
        .then(response => response.json())
        .then(data => {
            const alertsContent = document.getElementById('alerts-content');
            alertsContent.innerHTML = '';
            
            data.forEach(alert => {
                const alertElement = document.createElement('div');
                alertElement.className = `p-4 mb-4 rounded ${getAlertClass(alert.level)}`;
                alertElement.innerHTML = `
                    <div class="flex items-center">
                        <div class="flex-shrink-0">
                            ${getAlertIcon(alert.level)}
                        </div>
                        <div class="ml-3">
                            <p class="text-sm">${alert.message}</p>
                            <p class="text-xs text-gray-500">${formatDate(alert.timestamp)}</p>
                        </div>
                    </div>
                `;
                alertsContent.appendChild(alertElement);
            });
        })
        .catch(error => console.error('Error fetching alerts:', error));
}

// 获取机会信息
function fetchOpportunities() {
    fetch('/api/opportunities')
        .then(response => response.json())
        .then(data => {
            const opportunitiesContent = document.getElementById('opportunities-content');
            opportunitiesContent.innerHTML = '';
            
            data.forEach(opportunity => {
                const oppElement = document.createElement('div');
                oppElement.className = 'p-4 border-b';
                oppElement.innerHTML = `
                    <div class="flex justify-between items-center">
                        <div>
                            <h3 class="text-lg font-medium">${opportunity.name}</h3>
                            <p class="text-sm text-gray-500">${opportunity.description}</p>
                        </div>
                        <div class="text-right">
                            <span class="inline-flex items-center px-3 py-0.5 rounded-full text-sm font-medium bg-green-100 text-green-800">
                                ${opportunity.platform}
                            </span>
                        </div>
                    </div>
                `;
                opportunitiesContent.appendChild(oppElement);
            });
        })
        .catch(error => console.error('Error fetching opportunities:', error));
}

// 获取财务摘要
function fetchFinanceSummary() {
    fetch('/api/finance/summary')
        .then(response => response.json())
        .then(data => {
            const financeContent = document.getElementById('finance-content');
            financeContent.innerHTML = `
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="p-4 bg-blue-50 rounded">
                        <h3 class="text-lg font-medium text-blue-800">当前余额</h3>
                        <p class="text-2xl font-bold text-blue-600">¥${formatMoney(data.current_balance)}</p>
                    </div>
                    <div class="p-4 bg-green-50 rounded">
                        <h3 class="text-lg font-medium text-green-800">预计收入</h3>
                        <p class="text-2xl font-bold text-green-600">¥${formatMoney(data.predictions[0].predicted_balance)}</p>
                    </div>
                    <div class="p-4 bg-yellow-50 rounded">
                        <h3 class="text-lg font-medium text-yellow-800">预计税费</h3>
                        <p class="text-2xl font-bold text-yellow-600">¥${formatMoney(data.tax_estimation.estimated_tax)}</p>
                    </div>
                </div>
            `;
        })
        .catch(error => console.error('Error fetching finance summary:', error));
}

// 获取客户信息
function fetchClients() {
    fetch('/api/clients')
        .then(response => response.json())
        .then(data => {
            const clientsContent = document.getElementById('clients-content');
            clientsContent.innerHTML = `
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="p-4 bg-purple-50 rounded">
                        <h3 class="text-lg font-medium text-purple-800">总客户数</h3>
                        <p class="text-2xl font-bold text-purple-600">${data.total_clients}</p>
                    </div>
                    <div class="p-4 bg-indigo-50 rounded">
                        <h3 class="text-lg font-medium text-indigo-800">活跃项目</h3>
                        <p class="text-2xl font-bold text-indigo-600">${data.active_projects}</p>
                    </div>
                </div>
            `;
        })
        .catch(error => console.error('Error fetching clients:', error));
}

// 辅助函数
function getAlertClass(level) {
    switch(level.toUpperCase()) {
        case 'EMERGENCY':
            return 'bg-red-100 text-red-800';
        case 'WARNING':
            return 'bg-yellow-100 text-yellow-800';
        default:
            return 'bg-blue-100 text-blue-800';
    }
}

function getAlertIcon(level) {
    switch(level.toUpperCase()) {
        case 'EMERGENCY':
            return '<svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>';
        case 'WARNING':
            return '<svg class="h-5 w-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>';
        default:
            return '<svg class="h-5 w-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/></svg>';
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN');
}

function formatMoney(amount) {
    return amount.toLocaleString('zh-CN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
} 