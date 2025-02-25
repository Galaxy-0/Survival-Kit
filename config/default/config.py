"""
默认配置文件
"""

# GitHub监控配置
GITHUB_MONITOR_CONFIG = {
    'min_stars': 100,
    'min_forks': 20,
    'days_since_update': 30,
    'keywords': [
        'ai', 'machine-learning', 'automation',
        'saas', 'api', 'sdk', 'chrome-extension',
        'discord-bot', 'telegram-bot', 'web3'
    ]
}

# 项目分析配置
PROJECT_ANALYZER_CONFIG = {
    'weights': {
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
}

# 变现评估配置
MONETIZATION_EVALUATOR_CONFIG = {
    'min_revenue_threshold': 500,
    'roi_period_threshold': 6,
    'platform_scores': {
        'gumroad': 0.9,
        'github_marketplace': 0.8,
        'producthunt': 0.7,
        'chrome_store': 0.75
    }
}

# Web应用配置
WEB_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': False,
    'secret_key': 'your-secret-key-here'
} 