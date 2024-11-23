# 天机阁占卜平台配置说明文档

## 环境变量配置

### 基础配置
```env
# 应用配置
SECRET_KEY=your-secret-key-here  # JWT密钥，建议使用随机生成的字符串
ENVIRONMENT=production           # 环境类型：development/testing/production
DEBUG=false                     # 是否开启调试模式

# API配置
API_V1_STR=/api/v1             # API前缀
```

### 数据库配置
```env
# PostgreSQL配置
POSTGRES_USER=postgres          # 数据库用户名
POSTGRES_PASSWORD=postgres      # 数据库密码
POSTGRES_DB=fortune_platform    # 数据库名称
DATABASE_URI=postgresql+asyncpg://postgres:postgres@db:5432/fortune_platform  # 数据库连接URI
```

### Redis配置
```env
# Redis配置
REDIS_HOST=redis               # Redis主机名
REDIS_PORT=6379               # Redis端口
REDIS_PASSWORD=               # Redis密码（如果有）
```

### AI服务配置
```env
# OpenAI配置
OPENAI_API_KEY=your-api-key-here  # OpenAI API密钥
OPENAI_MODEL=gpt-4               # 使用的模型
OPENAI_TEMPERATURE=0.7           # 生成文本的创造性程度
OPENAI_MAX_TOKENS=1000          # 生成文本的最大长度
OPENAI_API_BASE=https://api.openai.com/v1  # API基础URL
```

## Docker配置

### 容器资源限制
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M

  frontend:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### 数据卷配置
```yaml
volumes:
  postgres_data:
    driver: local
    driver_opts:
      type: none
      device: /data/postgres
      o: bind

  redis_data:
    driver: local
    driver_opts:
      type: none
      device: /data/redis
      o: bind
```

## Nginx配置

### SSL配置
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # 其他配置...
}
```

### 缓存配置
```nginx
# 静态文件缓存
location /static/ {
    expires 30d;
    add_header Cache-Control "public, no-transform";
}

# API缓存
location /api/ {
    proxy_cache api_cache;
    proxy_cache_use_stale error timeout http_500 http_502 http_503 http_504;
    proxy_cache_valid 200 1m;
    proxy_cache_valid 404 1m;
    proxy_cache_key $request_uri;
}
```

## 日志配置

### 应用日志
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

### Nginx日志
```nginx
access_log /var/log/nginx/access.log combined buffer=32k flush=5s;
error_log /var/log/nginx/error.log warn;
```

## 监控配置

### Prometheus指标
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'fortune-platform'
    scrape_interval: 15s
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'
```

### 健康检查配置
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## 安全配置

### CORS配置
```python
CORS_ORIGINS = [
    "https://your-domain.com",
    "https://www.your-domain.com",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]
```

### 安全头配置
```nginx
add_header X-Frame-Options "SAMEORIGIN";
add_header X-XSS-Protection "1; mode=block";
add_header X-Content-Type-Options "nosniff";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
```

## 性能优化配置

### 数据库连接池
```python
DATABASE_POOL_SIZE = 20
DATABASE_MAX_OVERFLOW = 10
DATABASE_POOL_TIMEOUT = 30
```

### Redis连接池
```python
REDIS_POOL_SIZE = 10
REDIS_POOL_TIMEOUT = 5
```

### 缓存配置
```python
CACHE_TTL = 3600  # 缓存过期时间（秒）
CACHE_PREFIX = "fortune:"  # 缓存键前缀
```

## 备份配置

### 数据库备份
```bash
# 每日备份配置
0 2 * * * /app/scripts/backup-db.sh

# 保留时间
BACKUP_RETENTION_DAYS=30
```

### 日志轮转
```conf
/var/log/fortune/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 fortune fortune
}
```

## 告警配置

### 系统告警阈值
```yaml
alerts:
  cpu_usage: 80
  memory_usage: 85
  disk_usage: 90
  response_time: 2000  # ms
```

### 告警通知
```yaml
notifications:
  email:
    - admin@your-domain.com
  webhook:
    - https://your-webhook-url
```

## 其他配置

### 用户配额
```python
QUOTA_SETTINGS = {
    'free': {
        'daily_limit': 3,
    },
    'vip1': {
        'daily_limit': 10,
    },
    'vip2': {
        'daily_limit': 30,
    }
}
```

### 占卜设置
```python
DIVINATION_SETTINGS = {
    'answer_book': {
        'min_length': 50,
        'max_length': 500,
    },
    'tarot': {
        'min_length': 100,
        'max_length': 1000,
    },
    'yijing': {
        'min_length': 200,
        'max_length': 1500,
    }
} 