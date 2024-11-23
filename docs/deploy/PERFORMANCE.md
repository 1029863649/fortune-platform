# 天机阁占卜平台性能优化指南

## 数据库优化

### 1. 索引优化
```sql
-- 检查缺失的索引
SELECT 
    schemaname || '.' || relname as table,
    seq_scan,
    seq_tup_read,
    idx_scan,
    idx_tup_fetch
FROM 
    pg_stat_user_tables 
WHERE 
    seq_scan > 0 
ORDER BY 
    seq_scan DESC;

-- 添加常用查询的索引
CREATE INDEX idx_divination_records_created_at 
ON divination_records(created_at DESC);

CREATE INDEX idx_user_quotas_date_type 
ON user_quotas(quota_date, type);
```

### 2. 查询优化
```sql
-- 使用EXPLAIN ANALYZE分析查询性能
EXPLAIN ANALYZE 
SELECT * FROM divination_records 
WHERE user_id = 'xxx' 
ORDER BY created_at DESC 
LIMIT 10;

-- 优化大表分页查询
SELECT * FROM divination_records 
WHERE id > (
    SELECT id FROM divination_records 
    ORDER BY id 
    LIMIT 1 OFFSET 10000
) 
LIMIT 10;
```

### 3. 连接池配置
```python
# 数据库连接池配置
DATABASE_POOL_SIZE = 20
DATABASE_MAX_OVERFLOW = 10
DATABASE_POOL_TIMEOUT = 30

# SQLAlchemy配置
engine = create_async_engine(
    DATABASE_URI,
    pool_size=DATABASE_POOL_SIZE,
    max_overflow=DATABASE_MAX_OVERFLOW,
    pool_timeout=DATABASE_POOL_TIMEOUT,
    pool_pre_ping=True
)
```

## 缓存优化

### 1. Redis缓存策略
```python
# 缓存装饰器配置
@cache("user", 3600)  # 用户信息缓存1小时
async def get_user_by_id(user_id: str):
    pass

@cache("divination", 1800)  # 占卜记录缓存30分钟
async def get_divination_history(user_id: str):
    pass

# 缓存预热
async def warm_up_cache():
    users = await get_active_users()
    for user in users:
        await get_user_stats(user.id)
```

### 2. 缓存键设计
```python
# 缓存键前缀设计
CACHE_KEY_PREFIXES = {
    'user': 'fortune:user:',
    'divination': 'fortune:divination:',
    'quota': 'fortune:quota:',
    'stats': 'fortune:stats:'
}

# 缓存键生成
def generate_cache_key(prefix: str, *args):
    return f"{CACHE_KEY_PREFIXES[prefix]}{':'.join(args)}"
```

### 3. 缓存失效策略
```python
# 缓存自动过期
CACHE_TTL = {
    'user': 3600,        # 用户信息1小时
    'divination': 1800,  # 占卜记录30分钟
    'quota': 300,        # 配额信息5分钟
    'stats': 600         # 统计数据10分钟
}

# 主动清理缓存
async def clear_user_cache(user_id: str):
    keys = await redis.keys(f"{CACHE_KEY_PREFIXES['user']}*{user_id}*")
    if keys:
        await redis.delete(*keys)
```

## API性能优化

### 1. 异步处理
```python
# 使用异步任务处理耗时操作
@router.post("/divination")
async def create_divination(
    request: DivinationCreate,
    background_tasks: BackgroundTasks
):
    # 异步生成答案
    background_tasks.add_task(
        generate_divination_answer,
        request.type,
        request.question
    )
    return {"status": "processing"}
```

### 2. 数据分页
```python
# 使用游标分页
@router.get("/history")
async def get_history(
    cursor: Optional[str] = None,
    limit: int = 10
):
    query = select(DivinationRecord)
    if cursor:
        query = query.where(DivinationRecord.id < cursor)
    query = query.order_by(DivinationRecord.id.desc()).limit(limit)
    return await db.execute(query)
```

### 3. 响应压缩
```python
# 配置响应压缩
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000  # 超过1KB的响应进行压缩
)
```

## 前端优化

### 1. 资源加载
```nginx
# Nginx缓存配置
location /static/ {
    expires 30d;
    add_header Cache-Control "public, no-transform";
}

# 开启gzip压缩
gzip on;
gzip_types text/plain text/css application/json application/javascript;
gzip_min_length 1000;
```

### 2. 代码分割
```typescript
// 路由懒加载
const routes = [
  {
    path: '/divination',
    component: () => import('@/views/Divination.vue')
  }
]

// 组件异步加载
const AsyncComponent = defineAsyncComponent(() =>
  import('@/components/Heavy.vue')
)
```

### 3. 状态管理
```typescript
// 使用Pinia持久化
const useStore = defineStore('main', {
  state: () => ({
    user: null,
    settings: null
  }),
  persist: {
    enabled: true,
    strategies: [
      {
        key: 'user',
        storage: localStorage,
        paths: ['user']
      }
    ]
  }
})
```

## 系统优化

### 1. 容器资源限制
```yaml
# Docker资源限制
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
```

### 2. 负载均衡
```nginx
# Nginx负载均衡配置
upstream backend {
    server backend1:8000 weight=3;
    server backend2:8000 weight=2;
    server backend3:8000 weight=1 backup;
}
```

### 3. 监控指标
```python
# Prometheus指标
REQUEST_LATENCY = Histogram(
    'http_request_latency_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

# 记录请求延迟
@app.middleware("http")
async def monitor_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(latency)
    return response
```

## 性能测试

### 1. 负载测试
```bash
# 使用wrk进行负载测试
wrk -t12 -c400 -d30s http://localhost/api/v1/divination

# 使用ab进行并发测试
ab -n 1000 -c 100 http://localhost/api/v1/health
```

### 2. 性能分析
```python
# 使用cProfile进行性能分析
python -m cProfile -o output.prof app/main.py

# 使用memory_profiler分析内存使用
@profile
def memory_heavy_function():
    pass
```

### 3. 监控告警
```yaml
# Prometheus告警规则
groups:
- name: performance
  rules:
  - alert: HighLatency
    expr: http_request_latency_seconds > 2
    for: 5m
    labels:
      severity: warning
    annotations:
      description: "API响应时间超过2秒"
```

## 优化建议

1. 定期进行性能审计
2. 监控关键性能指标
3. 根据监控数据调整配置
4. 进行性能压力测试
5. 制定性能优化计划
6. 记录性能优化效果
7. 持续优化和改进 