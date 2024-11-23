# 天机阁占卜平台开发者指南

## 项目概述

天机阁占卜平台是一个基于现代技术栈构建的在线占卜服务平台。本指南旨在帮助开发者快速理解项目架构并参与开发。

## 技术栈

### 后端技术栈
- Python 3.9+
- FastAPI
- PostgreSQL
- Redis
- SQLAlchemy
- Alembic
- Poetry

### 前端技术栈
- Vue 3
- TypeScript
- TailwindCSS
- Pinia
- Vue Router
- Vite

## 开发环境搭建

### 1. 后端环境配置
```bash
# 安装 Python 3.9+
# 安装 Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 克隆项目
git clone https://github.com/your-username/fortune-platform.git
cd fortune-platform/server

# 安装依赖
poetry install

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置必要的环境变量

# 启动开发服务器
poetry run uvicorn app.main:app --reload
```

### 2. 前端环境配置
```bash
# 安装 Node.js 18+
# 安装 pnpm
npm install -g pnpm

# 进入前端目录
cd fortune-platform/web

# 安装依赖
pnpm install

# 配置环境变量
cp .env.example .env

# 启动开发服务器
pnpm dev
```

## 项目结构

### 后端结构
```
server/
├── app/
│   ├── api/              # API路由和端点
│   ├── core/             # 核心配置和工具
│   ├── models/           # 数据库模型
│   ├── schemas/          # Pydantic模型
│   ├── services/         # 业务逻辑
│   └── middleware/       # 中间件
├── tests/                # 测试文件
├── alembic/              # 数据库迁移
└── pyproject.toml        # 项目配置
```

### 前端结构
```
web/
├── src/
│   ├── api/             # API请求
│   ├── components/      # 通用组件
│   ├── views/           # 页面组件
│   ├── stores/          # 状态管理
│   ├── utils/           # 工具函数
│   └── types/           # TypeScript类型
├── public/              # 静态资源
└── package.json         # 项目配置
```

## 开发规范

### 1. 代码风格
- 后端遵循 PEP 8 规范
- 前端使用 ESLint + Prettier
- 使用 TypeScript 严格模式
- 组件使用 Composition API

### 2. 提交规范
```bash
# 提交格式
<type>(<scope>): <subject>

# 示例
feat(auth): 添加用户注册功能
fix(api): 修复登录接口错误处理
docs(readme): 更新安装说明
```

### 3. 分支管理
- main: 主分支，用于生产环境
- develop: 开发分支
- feature/*: 功能分支
- bugfix/*: 修复分支
- release/*: 发布分支

## API开发指南

### 1. 创建新API端点
```python
# app/api/v1/endpoints/example.py
from fastapi import APIRouter, Depends
from app.api import deps
from app.schemas.example import ExampleCreate, Example

router = APIRouter()

@router.post("/", response_model=Example)
async def create_example(
    example_in: ExampleCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    # 实现API逻辑
    pass
```

### 2. 添加数据库模型
```python
# app/models/example.py
from app.models.base import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class Example(Base):
    __tablename__ = "examples"
    
    title = Column(String, index=True)
    description = Column(String)
    user_id = Column(UUID, ForeignKey("users.id"))
    user = relationship("User", back_populates="examples")
```

### 3. 创建Schema
```python
# app/schemas/example.py
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ExampleBase(BaseModel):
    title: str
    description: str

class ExampleCreate(ExampleBase):
    pass

class Example(ExampleBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

## 前端开发指南

### 1. 创建新组件
```vue
<!-- src/components/ExampleComponent.vue -->
<template>
  <div class="example-component">
    <h1>{{ title }}</h1>
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  title: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'update', value: string): void
}>()
</script>
```

### 2. 添加API服务
```typescript
// src/api/example.ts
import http from '../utils/http'
import type { Example } from '../types'

export async function createExample(data: {
  title: string
  description: string
}): Promise<Example> {
  return http.post('/examples', data)
}

export async function getExamples(): Promise<Example[]> {
  return http.get('/examples')
}
```

### 3. 状态管理
```typescript
// src/stores/example.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Example } from '../types'
import * as api from '../api/example'

export const useExampleStore = defineStore('example', () => {
  const examples = ref<Example[]>([])
  
  async function fetchExamples() {
    examples.value = await api.getExamples()
  }
  
  return {
    examples,
    fetchExamples
  }
})
```

## 测试指南

### 1. 后端测试
```python
# tests/api/test_example.py
import pytest
from httpx import AsyncClient

async def test_create_example(
    client: AsyncClient,
    normal_user_token_headers: dict[str, str]
) -> None:
    data = {
        "title": "Test Example",
        "description": "Test Description"
    }
    response = await client.post(
        "/api/v1/examples/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 201
    content = response.json()
    assert content["title"] == data["title"]
```

### 2. 前端测试
```typescript
// tests/components/ExampleComponent.spec.ts
import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import ExampleComponent from '@/components/ExampleComponent.vue'

describe('ExampleComponent', () => {
  it('renders properly', () => {
    const wrapper = mount(ExampleComponent, {
      props: {
        title: 'Test Title'
      }
    })
    expect(wrapper.text()).toContain('Test Title')
  })
})
```

## 部署指南

### 1. 构建项目
```bash
# 后端
cd server
poetry install --no-dev
poetry run alembic upgrade head

# 前端
cd web
pnpm build
```

### 2. Docker部署
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d
```

## 常见问题

### 1. 开发环境问题
- 确保所有依赖都已正确安装
- 检查环境变量配置
- 确保数据库和Redis服务正常运行

### 2. 测试问题
- 使用正确的测试数据库
- 确保测试环境变量配置正确
- 测试前清理测试数据

### 3. 部署问题
- 检查Docker配置
- 确保所有环境变量都已设置
- 检查网络和防火墙配置

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request
5. 等待审核

## 联系方式

- 技术支持：dev@example.com
- 问题反馈：issues@example.com
- 开发群：123456789 