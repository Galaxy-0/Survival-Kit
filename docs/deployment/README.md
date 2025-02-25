# 部署指南

## 环境要求

- Python 3.8+
- pip
- Git

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/survival-kit.git
cd survival-kit
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置信息
```

## 运行服务

### 命令行模式

```bash
python src/monitor.py
```

### Web服务模式

```bash
python src/web/app.py
```

## Docker 部署

1. 构建镜像：
```bash
docker build -t survival-kit .
```

2. 运行容器：
```bash
docker run -d -p 5000:5000 \
  --env-file .env \
  --name survival-kit \
  survival-kit
```

## 监控和日志

- 日志文件位置：`logs/survival-kit.log`
- 数据存储位置：`data/`

## 更新部署

1. 拉取最新代码：
```bash
git pull origin main
```

2. 更新依赖：
```bash
pip install -r requirements.txt
```

3. 重启服务：
```bash
# 如果使用 supervisor
sudo supervisorctl restart survival-kit

# 如果使用 systemd
sudo systemctl restart survival-kit
```

## 故障排除

### 常见问题

1. API 密钥配置问题
   - 检查 `.env` 文件中的配置是否正确
   - 确保 API 密钥有效且未过期

2. 数据目录权限问题
   - 确保应用有写入权限：
     ```bash
     chmod -R 755 data/
     chmod -R 755 logs/
     ```

3. 端口占用问题
   - 检查端口是否被占用：
     ```bash
     lsof -i :5000
     ```
   - 修改配置使用其他端口

### 性能优化

1. 调整监控间隔
   - 编辑 `config/default/config.py`
   - 根据需求调整扫描频率

2. 数据清理
   - 定期清理旧数据：
     ```bash
     # 清理30天前的数据
     find data/ -type f -mtime +30 -delete
     ``` 