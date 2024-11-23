# 天机阁占卜平台 API 文档

## 基础信息

- 基础URL: `http://your-domain.com/api/v1`
- 所有请求都需要包含 `Content-Type: application/json` 头
- 认证请求需要包含 `Authorization: Bearer {token}` 头

## 认证相关

### 用户注册

```http
POST /auth/register

Request:
{
    "email": "user@example.com",
    "username": "username",
    "password": "password123"
}

Response: 201 Created
{
    "id": "uuid",
    "email": "user@example.com",
    "username": "username",
    "is_active": true,
    "is_superuser": false,
    "vip_level": 0,
    "created_at": "2024-03-21T10:00:00Z",
    "updated_at": "2024-03-21T10:00:00Z"
}
```

### 用户登录

```http
POST /auth/login

Request:
{
    "username": "username",
    "password": "password123"
}

Response: 200 OK
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "token_type": "bearer"
}
```

## 用户相关

### 获取当前用户信息

```http
GET /users/me

Response: 200 OK
{
    "id": "uuid",
    "email": "user@example.com",
    "username": "username",
    "is_active": true,
    "is_superuser": false,
    "vip_level": 0,
    "created_at": "2024-03-21T10:00:00Z",
    "updated_at": "2024-03-21T10:00:00Z"
}
```

### 更新用户信息

```http
PUT /users/me

Request:
{
    "email": "new@example.com",
    "username": "newusername"
}

Response: 200 OK
{
    "id": "uuid",
    "email": "new@example.com",
    "username": "newusername",
    ...
}
```

### 修改密码

```http
POST /users/me/password

Request:
{
    "current_password": "oldpassword",
    "new_password": "newpassword"
}

Response: 200 OK
{
    "message": "密码修改成功"
}
```

## 占卜相关

### 创建占卜

```http
POST /divination

Request:
{
    "type": "answer_book",  // answer_book, tarot, yijing
    "question": "我今天会遇到好事吗？"
}

Response: 201 Created
{
    "id": "uuid",
    "type": "answer_book",
    "question": "我今天会遇到好事吗？",
    "answer": "今天运势不错，很可能会有好事发生...",
    "created_at": "2024-03-21T10:00:00Z",
    "updated_at": "2024-03-21T10:00:00Z"
}
```

### 获取占卜历史

```http
GET /divination/me?skip=0&limit=10

Response: 200 OK
{
    "total": 100,
    "items": [
        {
            "id": "uuid",
            "type": "answer_book",
            "question": "问题",
            "answer": "答案",
            "created_at": "2024-03-21T10:00:00Z",
            "updated_at": "2024-03-21T10:00:00Z"
        },
        ...
    ]
}
```

## 收藏相关

### 添加收藏

```http
POST /favorites

Request:
{
    "record_id": "uuid"
}

Response: 201 Created
{
    "id": "uuid",
    "user_id": "uuid",
    "record_id": "uuid",
    "created_at": "2024-03-21T10:00:00Z",
    "updated_at": "2024-03-21T10:00:00Z"
}
```

### 获取收藏列表

```http
GET /favorites/me?skip=0&limit=10

Response: 200 OK
{
    "total": 50,
    "items": [
        {
            "id": "uuid",
            "record": {
                "id": "uuid",
                "type": "answer_book",
                "question": "问题",
                "answer": "答案",
                "created_at": "2024-03-21T10:00:00Z"
            },
            "created_at": "2024-03-21T10:00:00Z"
        },
        ...
    ]
}
```

### 取消收藏

```http
DELETE /favorites/{record_id}

Response: 204 No Content
```

## 配额相关

### 获取配额信息

```http
GET /quota/me

Response: 200 OK
{
    "daily_limit": 10,
    "used_today": 3,
    "remaining": 7,
    "reset_time": "2024-03-22T00:00:00Z"
}
```

## 统计相关

### 获取用户统计

```http
GET /stats/me

Response: 200 OK
{
    "total_divinations": 100,
    "type_stats": {
        "answer_book": 50,
        "tarot": 30,
        "yijing": 20
    },
    "favorites_count": 20
}
```

### 获取趋势数据

```http
GET /stats/trends?days=7

Response: 200 OK
{
    "dates": ["2024-03-15", "2024-03-16", ...],
    "counts": [10, 15, 8, 12, 20, 18, 25]
}
```

## 错误响应

所有API可能返回的错误响应格式如下：

```http
Response: 4xx/5xx
{
    "detail": "错误信息描述"
}
```

常见错误码：
- 400: 请求参数错误
- 401: 未认证或认证失败
- 403: 权限不足
- 404: 资源不存在
- 429: 请求过于频繁
- 500: 服务器内部错误

## 请求限制

- 未认证用户: 60次/小时
- 普通用户: 1000次/小时
- VIP用户: 5000次/小时

## 数据格式

### 时间格式
所有时间字段使用ISO 8601格式：`YYYY-MM-DDTHH:mm:ssZ`

### ID格式
所有ID字段使用UUID v4格式

## 安全说明

1. 所有API请求都应使用HTTPS
2. 认证token有效期为30分钟
3. 密码必须包含字母、数字，长度至少8位
4. 敏感数据传输时需要加密 