# 天机阁占卜平台部署指南

## 系统要求

- Docker 20.10+
- Docker Compose 2.0+
- 2GB+ RAM
- 20GB+ 磁盘空间
- Ubuntu 20.04+ / CentOS 8+

## 安装步骤

### 1. 安装Docker和Docker Compose

```bash
# 安装Docker
curl -fsSL https://get.docker.com | sh

# 启动Docker服务
sudo systemctl start docker
sudo systemctl enable docker

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. 克隆项目代码

```bash
git clone https://github.com/your-username/fortune-platform.git
cd fortune-platform
```

### 3. 配置环境变量

复制环境变量示例文件并修改配置：

```bash
cp .env.example .env
```

编辑 .env 文件，设置以下必要的环境变量：
- SECRET_KEY：应用密钥
- OPENAI_API_KEY：OpenAI API密钥
- 其他数据库和Redis相关配置

### 4. 启动服务

```bash
# 构建镜像并启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f
```

### 5. 初始化数据库

数据库会在首次启动时自动初始化，无需手动操作。

### 6. 配置Nginx（可选）

如果需要配置域名访问，可以安装Nginx：

```bash
sudo apt install nginx

# 配置Nginx
sudo nano /etc/nginx/sites-available/fortune-platform
```

添加以下配置：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

启用站点配置：

```bash
sudo ln -s /etc/nginx/sites-available/fortune-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 维护操作

### 数据库备份

```bash
# 执行备份
./scripts/backup-db.sh

# 查看备份文件
ls -l backups/database/
```

### 数据库恢复

```bash
# 恢复数据库
./scripts/restore-db.sh backups/database/backup_file.sql.gz
```

### 更新应用

```bash
# 拉取最新代码
git pull

# 重新构建并启动服务
docker-compose up -d --build
```

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 监控和告警

### 1. 系统监控

访问 http://your-domain.com/monitor 查看系统监控数据。

### 2. 健康检查

访问 http://your-domain.com/health 检查系统健康状态。

### 3. Prometheus指标

访问 http://your-domain.com/metrics 查看Prometheus指标。

## 故障排除

### 1. 服务无法启动

检查以下内容：
- Docker服务是否正常运行
- 端口是否被占用
- 环境变量是否配置正确
- 查看服务日志获取详细错误信息

### 2. 数据库连接失败

检查以下内容：
- 数据库服务是否正常运行
- 数据库连接配置是否正确
- 数据库用户权限是否正确

### 3. Redis连接失败

检查以下内容：
- Redis服务是否正常运行
- Redis连接配置是否正确
- Redis内存使用情况

## 安全建议

1. 修改默认密码
2. 限制数据库和Redis访问
3. 配置防火墙规则
4. 定期更新系统和依赖
5. 启用HTTPS
6. 定期备份数据

## 性能优化

1. 配置合适的缓存策略
2. 优化数据库查询
3. 配置合适的连接池大小
4. 使用CDN加速静态资源
5. 开启Nginx缓存

## 联系支持

如果遇到问题，请通过以下方式获取支持：
- 提交GitHub Issue
- 发送邮件至support@example.com
- 加入技术支持群：123456789 