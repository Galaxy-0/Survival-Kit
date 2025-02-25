# API 文档

## 监控模块 API

### GitHubMonitor

#### `search_trending_repos()`
搜索趋势项目。

**返回值：**
- `List[Dict]`: 趋势项目列表

#### `analyze_repo_activity(repo_name: str)`
分析仓库活跃度。

**参数：**
- `repo_name`: 仓库名称

**返回值：**
- `Dict`: 活跃度分析结果

## 分析模块 API

### ProjectAnalyzer

#### `analyze_project(project_data: Dict)`
分析项目并生成评分。

**参数：**
- `project_data`: 项目数据

**返回值：**
- `Dict`: 项目分析结果

## 评估模块 API

### MonetizationEvaluator

#### `evaluate_monetization(project_analysis: Dict)`
评估项目的变现潜力。

**参数：**
- `project_analysis`: 项目分析结果

**返回值：**
- `Dict`: 变现评估结果

## Web API

### 项目监控

```http
GET /api/opportunities
```

**响应：**
```json
{
    "timestamp": "2024-02-24T12:00:00Z",
    "results": [
        {
            "id": "repo-id",
            "name": "username/repo",
            "description": "项目描述",
            "stars": 1000,
            "forks": 200
        }
    ]
}
```

### 项目分析

```http
GET /api/analysis/{project_id}
```

**响应：**
```json
{
    "project_id": "username/repo",
    "evaluation": {
        "technical_score": 8.5,
        "market_score": 7.8,
        "monetization_score": 6.9
    }
}
``` 