#!/bin/bash

# 检查参数
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 backup_file.sql.gz"
    exit 1
fi

BACKUP_FILE=$1

# 检查文件是否存在
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Backup file not found: $BACKUP_FILE"
    exit 1
fi

# 解压备份文件
gunzip -c $BACKUP_FILE | docker exec -i fortune-db psql -U postgres fortune_platform

echo "Database restore completed from: $BACKUP_FILE" 