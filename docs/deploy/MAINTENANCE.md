# 天机阁占卜平台维护手册

## 日常维护

### 1. 系统监控
- 定期检查系统监控指标
  ```bash
  # 查看系统状态
  curl http://your-domain.com/monitor/health
  
  # 查看Prometheus指标
  curl http://your-domain.com/monitor/metrics
  ```

- 关注以下关键指标：
  - CPU使用率 (阈值: 80%)
  - 内存使用率 (阈值: 85%)
  - 磁盘使用率 (阈值: 90%)
  - API响应时间 (阈值: 2000ms)
  - 错误率 (阈值: 1%)

### 2. 数据库维护
- 定期备份数据库
  ```bash
  # 手动执行备份
  ./scripts/backup-db.sh
  
  # 检查备份状态
  ls -l backups/database/
  ```

- 清理过期备份
  ```bash
  # 清理30天前的备份
  find backups/database/ -name "*.sql.gz" -mtime +30 -delete
  ```

- 检查数据库性能
  ```sql
  -- 检查慢查询
  SELECT * FROM pg_stat_activity WHERE state = 'active' ORDER BY duration DESC;
  
  -- 检查表大小
  SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
  FROM pg_catalog.pg_statio_user_tables
  ORDER BY pg_total_relation_size(relid) DESC;
  ```

### 3. 日志管理
- 检查日志文件
  ```bash
  # 查看应用日志
  tail -f logs/app.log
  
  # 查看错误日志
  tail -f logs/error.log
  
  # 查看访问日志
  tail -f logs/access.log
  ```

- 日志轮转
  ```bash
  # 手动触发日志轮转
  logrotate -f /etc/logrotate.d/fortune
  ```

### 4. 缓存维护
- 检查Redis状态
  ```bash
  # 连接Redis
  redis-cli
  
  # 查看内存使用情况
  INFO memory
  
  # 查看键统计
  INFO keyspace
  ```

- 清理缓存（必要时）
  ```bash
  # 清理特定前缀的缓存
  redis-cli KEYS "fortune:*" | xargs redis-cli DEL
  ```

## 故障处理

### 1. 服务不可用
1. 检查服务状态
   ```bash
   docker-compose ps
   ```

2. 查看服务日志
   ```bash
   docker-compose logs -f backend
   docker-compose logs -f frontend
   ```

3. 重启服务
   ```bash
   docker-compose restart backend
   docker-compose restart frontend
   ```

### 2. 数据库问题
1. 检查数据库连接
   ```bash
   docker-compose exec db pg_isready -U postgres
   ```

2. 数据库恢复
   ```bash
   # 从最近的备份恢复
   ./scripts/restore-db.sh backups/database/latest.sql.gz
   ```

3. 修复数据库索引
   ```sql
   REINDEX DATABASE fortune_platform;
   ```

### 3. 缓存问题
1. 检查Redis连接
   ```bash
   docker-compose exec redis redis-cli ping
   ```

2. 重置Redis
   ```bash
   docker-compose restart redis
   ```

### 4. 性能问题
1. 检查系统资源
   ```bash
   # 查看容器资源使用情况
   docker stats
   ```

2. 清理磁盘空间
   ```bash
   # 清理Docker资源
   docker system prune -a
   
   # 清理日志文件
   find /var/log/fortune -name "*.gz" -mtime +30 -delete
   ```

3. 优化数据库
   ```sql
   -- 分析表
   ANALYZE verbose;
   
   -- 清理死连接
   SELECT pg_terminate_backend(pid) 
   FROM pg_stat_activity 
   WHERE state = 'idle' AND state_change < current_timestamp - interval '1 hour';
   ```

## 系统更新

### 1. 代码更新
```bash
# 拉取最新代码
git pull

# 重新构建并启动服务
docker-compose up -d --build
```

### 2. 数据库迁移
```bash
# 执行数据库迁移
docker-compose exec backend alembic upgrade head
```

### 3. 配置更新
1. 更新环境变量
   ```bash
   # 编辑环境变量文件
   nano .env
   
   # 重启服务使配置生效
   docker-compose restart
   ```

2. 更新Nginx配置
   ```bash
   # 编辑Nginx配置
   nano web/nginx.conf
   
   # 重新构建前端
   docker-compose up -d --build frontend
   ```

## 安全维护

### 1. 证书更新
```bash
# 更新SSL证书
certbot renew

# 复制新证书到Nginx配置目录
cp /etc/letsencrypt/live/your-domain.com/* /etc/nginx/ssl/
```

### 2. 密码更新
- 定期更新数据库密码
- 更新API密钥
- 轮换JWT密钥

### 3. 安全检查
- 定期检查系统日志中的异常访问
- 检查未授权的API调用
- 监控异常的用户行为

## 性能优化

### 1. 数据库优化
- 定期更新统计信息
- 清理过期数据
- 优化慢查询

### 2. 缓存优化
- 调整缓存过期时间
- 监控缓存命中率
- 优化缓存策略

### 3. 应用优化
- 监控API响应时间
- 优化大量请求的接口
- 调整并发连接数

## 备份策略

### 1. 数据库备份
- 每日自动备份
- 定期验证备份有效性
- 异地备份重要数据

### 2. 配置备份
- 备份环境变量配置
- 备份Nginx配置
- 备份SSL证书

### 3. 日志备份
- 归档重要日志
- 备份审计日志
- 保存错误日志

## 监控告警

### 1. 设置告警规则
- CPU使用率超过80%
- 内存使用率超过85%
- 磁盘使用率超过90%
- API错误率超过1%
- 响应时间超过2秒

### 2. 告警通知
- 配置邮件通知
- 配置短信通知
- 配置webhook通知

### 3. 告警处理
- 制定告警响应流程
- 记录告警处理过程
- 定期复查告警原因 