"""
评估标准配置
"""

# 收入目标
DAILY_INCOME_TARGET = 50.0  # 每天目标收入（美元）
MONTHLY_INCOME_TARGET = DAILY_INCOME_TARGET * 30  # 每月目标收入

# 成本限制
MAX_SETUP_COST = 500.0  # 最大启动成本（美元）
MAX_MONTHLY_COST = 100.0  # 最大月度运营成本（美元）

# 评分权重
WEIGHTS = {
    'setup_cost': 0.3,        # 启动成本权重（越低越好）
    'monthly_cost': 0.2,      # 月度成本权重（越低越好）
    'income_potential': 0.2,   # 收入潜力权重
    'passive_level': 0.15,    # 被动收入程度权重
    'time_investment': 0.15,  # 时间投入权重（越低越好）
}

# 时间投入评估（小时/周）
TIME_INVESTMENT_LEVELS = {
    'minimal': 5,    # 每周5小时以下
    'low': 10,       # 每周5-10小时
    'medium': 20,    # 每周10-20小时
    'high': 40       # 每周20小时以上
}

# 项目评分阈值
MIN_SCORE_THRESHOLD = 0.6  # 最低可接受评分

# 变现路径优先级
MONETIZATION_PRIORITIES = [
    'template_sales',      # 模板销售（低成本，快速启动）
    'plugin_marketplace',  # 插件市场（中等成本，稳定收入）
    'consulting',         # 咨询服务（低启动成本，需要时间投入）
    'saas',              # SaaS服务（较高启动成本，长期收益）
]

# 平台选择标准
PLATFORM_CRITERIA = {
    'gumroad': {
        'fee_percentage': 0.09,  # 9% 手续费
        'setup_cost': 0,         # 无启动成本
        'monthly_cost': 0        # 无月费
    },
    'github_marketplace': {
        'fee_percentage': 0.25,  # 25% 手续费
        'setup_cost': 0,         # 无启动成本
        'monthly_cost': 0        # 无月费
    },
    'producthunt': {
        'fee_percentage': 0,     # 无手续费
        'setup_cost': 0,         # 无启动成本
        'monthly_cost': 0        # 无月费
    }
}

# ROI 期望
MAX_ROI_PERIOD_MONTHS = 2  # 最大投资回报期望（月）

# 风险评估标准
RISK_LEVELS = {
    'low': 0.8,    # 低风险项目得分
    'medium': 0.5,  # 中等风险项目得分
    'high': 0.2    # 高风险项目得分
} 