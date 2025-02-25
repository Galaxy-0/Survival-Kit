# 模块文档

## 项目结构

```
survival-kit/
├── src/
│   ├── monitor/          # GitHub项目监控模块
│   ├── analyzer/         # 项目分析模块
│   ├── evaluator/        # 变现评估模块
│   ├── web/             # Web应用模块
│   └── utils/           # 工具模块
├── config/              # 配置文件
├── data/               # 数据存储
├── docs/               # 文档
└── tests/              # 测试
```

## 核心模块说明

### 监控模块 (monitor)

负责监控GitHub上的潜在项目，主要功能：
- 趋势项目搜索
- 活跃度分析
- 贡献者分析
- 问题和PR分析

关键类：
- `GitHubMonitor`: 核心监控类

### 分析模块 (analyzer)

对项目进行多维度分析，主要功能：
- 技术维度评分
- 市场维度评分
- 变现维度评分

关键类：
- `ProjectAnalyzer`: 核心分析类

### 评估模块 (evaluator)

评估项目的变现潜力，主要功能：
- 变现路径评估
- 收入预测
- 成本估算
- ROI计算

关键类：
- `MonetizationEvaluator`: 核心评估类

### Web模块 (web)

提供Web界面，主要功能：
- RESTful API
- 数据可视化
- 用户交互

关键文件：
- `app.py`: Web应用入口
- `templates/`: HTML模板
- `static/`: 静态资源

### 工具模块 (utils)

提供通用工具，主要功能：
- 日志管理
- 配置加载
- 数据持久化

关键文件：
- `logger.py`: 日志工具
- `config_loader.py`: 配置加载器

## 数据流

1. 数据采集
   ```
   GitHubMonitor -> data/github_trends.json
   ```

2. 数据分析
   ```
   ProjectAnalyzer -> data/project_analysis.json
   ```

3. 变现评估
   ```
   MonetizationEvaluator -> data/monetization_evaluation.json
   ```

4. 结果展示
   ```
   Web Interface <- data/*.json
   ```

## 配置说明

### 环境变量
- `GITHUB_TOKEN`: GitHub API访问令牌
- `OPENAI_API_KEY`: OpenAI API密钥（可选）
- `MIN_STARS`: 最小星标数
- `MIN_FORKS`: 最小分叉数

### 配置文件
- `config/default/config.py`: 默认配置
- `config/logging/logging.conf`: 日志配置

## 扩展开发

### 添加新的监控源
1. 在 `src/monitor/` 下创建新的监控类
2. 实现标准接口方法
3. 在 `monitor.py` 中集成

### 自定义评分规则
1. 修改 `config/default/config.py` 中的权重
2. 在相应的分析器中添加新的评分维度

### 添加新的变现模式
1. 在 `MonetizationEvaluator` 中添加新的模式
2. 更新评估逻辑和收入预测 