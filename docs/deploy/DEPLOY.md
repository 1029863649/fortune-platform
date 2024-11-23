# 天机阁占卜平台部署文档

## 部署架构

### 系统架构
```
                                    [负载均衡器]
                                         |
                    +-------------------+-------------------+
                    |                   |                   |
              [前端服务器1]       [前端服务器2]       [前端服务器3]
                    |                   |                   |
                    +-------------------+-------------------+
                                         |
                                   [后端服务集群]
                                         |
                    +-------------------+-------------------+
                    |                   |                   |
              [PostgreSQL]          [Redis]           [监控系统]
```

## 环境要求

### 硬件要求
- CPU: 4核心以上
- 内存: 8GB以上
- 磁盘: 100GB以上
- 网络: 100Mbps以上

### 软件要求
- Docker 20.10+
- Docker Compose 2.0+
- Nginx 1.18+
- PostgreSQL 14+
- Redis 6+

## 部署步骤

### 1. 准备工作

#### 1.1 创建部署目录
```bash
mkdir -p /opt/fortune-platform
cd /opt/fortune-platform
```

#### 1.2 配置环境变量
```bash
# 复制环境变量文件
cp .env.example .env

# 编辑环境变量
nano .env

# 配置以下必要变量
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
POSTGRES_PASSWORD=your-db-password
REDIS_PASSWORD=your-redis-password
```

### 2. 数据库部署

#### 2.1 初始化数据库
```bash
# 创建数据目录
mkdir -p /data/postgres
mkdir -p /data/redis

# 设置权限
chown -R 999:999 /data/postgres
chown -R 999:999 /data/redis
```

#### 2.2 配置数据库备份
```bash
# 创建备份目录
mkdir -p /backup/postgres

# 设置备份定时任务
crontab -e

# 添加以下内容
0 2 * * * /opt/fortune-platform/scripts/backup-db.sh >> /var/log/backup.log 2>&1
```

### 3. 服务部署

#### 3.1 构建服务
```bash
# 构建所有服务
docker-compose build

# 或者单独构建
docker-compose build backend
docker-compose build frontend
```

#### 3.2 启动服务
```bash
# 启动所有服务
docker-compose up -d

# 检查服务状态
docker-compose ps
```

#### 3.3 初始化数据
```bash
# 执行数据库迁移
docker-compose exec backend poetry run alembic upgrade head

# 创建初始管理员用户
docker-compose exec backend poetry run python -m scripts.create_admin
```

### 4. Nginx配置

#### 4.1 安装Nginx
```bash
apt update
apt install nginx
```

#### 4.2 配置SSL证书
```bash
# 安装certbot
apt install certbot python3-certbot-nginx

# 获取证书
certbot --nginx -d your-domain.com
```

#### 4.3 配置Nginx
```nginx
# /etc/nginx/sites-available/fortune-platform

upstream backend {
    server localhost:8000;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL配置
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # 前端文件
    location / {
        root /var/www/fortune-platform;
        try_files $uri $uri/ /index.html;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # API代理
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 静态文件缓存
    location /static/ {
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
}
```

### 5. 监控配置

#### 5.1 配置Prometheus
```yaml
# /etc/prometheus/prometheus.yml
scrape_configs:
  - job_name: 'fortune-platform'
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

#### 5.2 配置Grafana
- 导入监控面板
- 配置告警规则
- 设置通知渠道

### 6. 日志配置

#### 6.1 配置日志轮转
```conf
# /etc/logrotate.d/fortune-platform
/var/log/fortune-platform/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 fortune fortune
}
```

#### 6.2 配置日志收集
- 配置ELK或其他日志收集系统
- 设置日志格式和过滤规则
- 配置日志保留策略

## 维护操作

### 1. 更新部署
```bash
# 拉取最新代码
git pull

# 重新构建服务
docker-compose build

# 重启服务
docker-compose up -d
```

### 2. 数据备份
```bash
# 手动备份数据库
./scripts/backup-db.sh

# 恢复数据库
./scripts/restore-db.sh backups/database/backup_file.sql.gz
```

### 3. 日志查看
```bash
# 查看服务日志
docker-compose logs -f

# 查看Nginx日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 4. 性能调优
- 调整数据库连接池
- 优化Redis缓存配置
- 调整Nginx工作进程数
- 配置系统资源限制

## 故障处理

### 1. 服务不可用
- 检查服务状态
- 查看错误日志
- 检查系统资源
- 重启相关服务

### 2. 数据库问题
- 检查连接状态
- 查看错误日志
- 检查磁盘空间
- 执行数据库维护

### 3. 缓存问题
- 检查Redis状态
- 清理过期缓存
- 检查内存使用
- 重启缓存服务

## 安全加固

### 1. 系统安全
- 更新系统补丁
- 配置防火墙规则
- 禁用不必要服务
- 限制SSH访问

### 2. 应用安全
- 启用HTTPS
- 配置安全头
- 限制API访问
- 加密敏感数据

### 3. 数据安全
- 定期备份数据
- 加密备份文件
- 限制数据库访问
- 监控数据操作

## 监控告警

### 1. 系统监控
- CPU使用率 > 80%
- 内存使用率 > 85%
- 磁盘使用率 > 90%
- 网络带宽 > 80%

### 2. 应用监控
- API响应时间 > 2s
- 错误率 > 1%
- 并发连接数 > 1000
- 请求队列 > 100

### 3. 告警通知
- 配置邮件通知
- 配置短信通知
- 配置微信通知
- 设置告警升级

## 联系支持

- 技术支持：support@example.com
- 运维团队：ops@example.com
- 紧急联系：emergency@example.com
- 值班电话：+86-xxx-xxxx-xxxx 