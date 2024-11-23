# 天机阁占卜平台安全加固指南

## 系统安全

### 1. 服务器加固
```bash
# 更新系统包
apt update && apt upgrade -y

# 配置防火墙
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp
ufw enable

# 禁用root远程登录
sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart sshd
```

### 2. Docker安全配置
```yaml
# docker-compose.yml 安全配置
services:
  backend:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 3. 容器隔离
```yaml
# 网络隔离配置
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # 内部网络，不允许外部访问
```

## 应用安全

### 1. 认证安全
```python
# JWT配置
JWT_SETTINGS = {
    'ALGORITHM': 'HS256',
    'ACCESS_TOKEN_EXPIRE_MINUTES': 30,
    'REFRESH_TOKEN_EXPIRE_DAYS': 7,
    'ROTATE_REFRESH_TOKENS': True,
}

# 密码哈希配置
PASSWORD_SETTINGS = {
    'HASH_ALGORITHM': 'bcrypt',
    'SALT_ROUNDS': 12,
}
```

### 2. 请求安全
```python
# 请求限制中间件
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    if await is_rate_limited(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests")
    return await call_next(request)

# CORS配置
CORS_SETTINGS = {
    'ALLOW_ORIGINS': [
        'https://your-domain.com',
    ],
    'ALLOW_METHODS': ['GET', 'POST', 'PUT', 'DELETE'],
    'ALLOW_HEADERS': ['*'],
    'ALLOW_CREDENTIALS': True,
    'MAX_AGE': 600,
}
```

### 3. 数据安全
```python
# 敏感数据加密
def encrypt_sensitive_data(data: str) -> str:
    key = Fernet.generate_key()
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

# 数据脱敏
def mask_sensitive_data(data: str) -> str:
    if len(data) <= 4:
        return '*' * len(data)
    return data[:2] + '*' * (len(data) - 4) + data[-2:]
```

## 数据库安全

### 1. 访问控制
```sql
-- 创建只读用户
CREATE USER 'readonly_user'@'%' IDENTIFIED BY 'password';
GRANT SELECT ON fortune_platform.* TO 'readonly_user'@'%';

-- 创建应用用户
CREATE USER 'app_user'@'%' IDENTIFIED BY 'password';
GRANT SELECT, INSERT, UPDATE, DELETE ON fortune_platform.* TO 'app_user'@'%';
```

### 2. 数据加密
```sql
-- 创建加密函数
CREATE OR REPLACE FUNCTION encrypt_data(data text, key text)
RETURNS text AS $$
BEGIN
    RETURN pgp_sym_encrypt(data, key);
END;
$$ LANGUAGE plpgsql;

-- 创建解密函数
CREATE OR REPLACE FUNCTION decrypt_data(encrypted_data text, key text)
RETURNS text AS $$
BEGIN
    RETURN pgp_sym_decrypt(encrypted_data::bytea, key);
END;
$$ LANGUAGE plpgsql;
```

### 3. 审计日志
```sql
-- 创建审计日志表
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    record_id UUID NOT NULL,
    old_data JSONB,
    new_data JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 创建审计触发器
CREATE OR REPLACE FUNCTION audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_logs (
        user_id, action, table_name, record_id,
        old_data, new_data
    ) VALUES (
        current_user_id(), TG_OP, TG_TABLE_NAME,
        COALESCE(NEW.id, OLD.id),
        row_to_json(OLD), row_to_json(NEW)
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

## 缓存安全

### 1. Redis安全配置
```conf
# redis.conf
requirepass your_strong_password
rename-command FLUSHALL ""
rename-command FLUSHDB ""
rename-command CONFIG ""
maxmemory 1gb
maxmemory-policy allkeys-lru
```

### 2. 缓存数据保护
```python
# 缓存键加密
def generate_cache_key(prefix: str, *args) -> str:
    key = f"{prefix}:{':'.join(args)}"
    return hashlib.sha256(key.encode()).hexdigest()

# 缓存数据加密
def encrypt_cache_data(data: str) -> str:
    return encrypt_sensitive_data(data)
```

## 日志安全

### 1. 日志配置
```python
# 日志脱敏
class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        sensitive_fields = ['password', 'token', 'credit_card']
        for field in sensitive_fields:
            if hasattr(record, field):
                setattr(record, field, mask_sensitive_data(getattr(record, field)))
        return True

# 日志格式化
LOG_FORMAT = (
    '%(asctime)s - %(name)s - %(levelname)s - '
    '%(remote_addr)s - %(user_id)s - %(message)s'
)
```

### 2. 日志存储
```python
# 日志轮转配置
LOGGING = {
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'detailed',
            'filters': ['sensitive_data'],
        },
    },
}
```

## 监控告警

### 1. ���全事件监控
```python
# 异常登录监控
async def monitor_login_attempts(user_id: str, ip: str):
    key = f"login_attempts:{user_id}:{ip}"
    attempts = await redis.incr(key)
    await redis.expire(key, 3600)  # 1小时过期
    
    if attempts > 5:
        await send_security_alert(
            f"检测到用户 {user_id} 从 {ip} 多次登录失败"
        )
```

### 2. 系统监控
```python
# 系统资源监控
async def monitor_system_resources():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    
    if cpu_usage > 80 or memory_usage > 85 or disk_usage > 90:
        await send_system_alert(
            f"系统资源告警: CPU {cpu_usage}%, "
            f"内存 {memory_usage}%, "
            f"磁盘 {disk_usage}%"
        )
```

## 安全检查清单

### 1. 定期检查
- [ ] 系统包更新
- [ ] 安全补丁安装
- [ ] SSL证书有效期
- [ ] 密码策略合规性
- [ ] 防火墙规则审查

### 2. 安全审计
- [ ] 用户权限审计
- [ ] 数据访问审计
- [ ] API调用审计
- [ ] 系统日志审计
- [ ] 安全事件回顾

### 3. 应急响应
1. 建立应急响应团队
2. 制定应急响应流程
3. 准备应急响应工具
4. 定期进行应急演练
5. 记��和总结安全事件 