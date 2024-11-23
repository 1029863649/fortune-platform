#!/bin/bash

# 获取当前时间戳
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
BACKUP_DIR="backups/database"
mkdir -p $BACKUP_DIR

# 备份文件名
BACKUP_FILE="$BACKUP_DIR/fortune_platform_$TIMESTAMP.sql"

# 执行备份
docker exec fortune-db pg_dump -U postgres fortune_platform > $BACKUP_FILE

# 压缩备份文件
gzip $BACKUP_FILE

# 删除30天前的备份
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "Database backup completed: ${BACKUP_FILE}.gz" 