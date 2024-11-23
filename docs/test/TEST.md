# 天机阁占卜平台测试文档

## 测试环境配置

### 1. 后端测试环境
```bash
# 安装测试依赖
poetry install --with test

# 配置测试数据库
export DATABASE_URI=postgresql+asyncpg://postgres:postgres@localhost:5432/fortune_platform_test
export REDIS_HOST=localhost
export REDIS_PORT=6379
export SECRET_KEY=test_secret_key
export ENVIRONMENT=test
```

### 2. 前端测试环境
```bash
# 安装测试依赖
pnpm install --save-dev @vue/test-utils vitest @testing-library/vue

# 配置测试环境变量
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env.test
```

## 单元测试

### 1. 后端单元测试

#### API测试
```python
# test_auth.py
async def test_register(client):
    response = await client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"

# test_divination.py
async def test_create_divination(client, token):
    response = await client.post(
        "/divination",
        json={
            "type": "answer_book",
            "question": "今天会下雨吗？"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["type"] == "answer_book"
    assert data["question"] == "今天会下雨吗？"
    assert "answer" in data
```

#### 服务测试
```python
# test_user_service.py
async def test_create_user(db):
    user = await create_user(db, UserCreate(
        email="test@example.com",
        username="testuser",
        password="password123"
    ))
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert verify_password("password123", user.hashed_password)

# test_divination_service.py
async def test_generate_answer():
    answer = await generate_answer("answer_book", "今天会下雨吗？")
    assert answer is not None
    assert len(answer) > 0
```

### 2. 前端单元测试

#### 组件测试
```typescript
// test_login.spec.ts
import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import Login from '../views/auth/Login.vue'

describe('Login.vue', () => {
  it('renders login form', () => {
    const wrapper = mount(Login)
    expect(wrapper.find('form').exists()).toBe(true)
    expect(wrapper.find('input[type="text"]').exists()).toBe(true)
    expect(wrapper.find('input[type="password"]').exists()).toBe(true)
  })

  it('submits form with credentials', async () => {
    const wrapper = mount(Login)
    await wrapper.find('input[type="text"]').setValue('testuser')
    await wrapper.find('input[type="password"]').setValue('password123')
    await wrapper.find('form').trigger('submit')
    // 验证表单提交
  })
})

// test_divination.spec.ts
describe('Divination.vue', () => {
  it('renders divination types', () => {
    const wrapper = mount(Divination)
    expect(wrapper.findAll('.divination-type').length).toBe(3)
  })

  it('submits divination request', async () => {
    const wrapper = mount(Divination)
    await wrapper.find('.divination-type').trigger('click')
    await wrapper.find('textarea').setValue('今天会下雨吗？')
    await wrapper.find('form').trigger('submit')
    // 验证占卜请求
  })
})
```

#### Store测试
```typescript
// test_user_store.spec.ts
import { setActivePinia, createPinia } from 'pinia'
import { useUserStore } from '../stores/user'

describe('User Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('logs in user', async () => {
    const store = useUserStore()
    await store.login({
      username: 'testuser',
      password: 'password123'
    })
    expect(store.user).not.toBeNull()
    expect(store.isLoggedIn).toBe(true)
  })

  it('logs out user', () => {
    const store = useUserStore()
    store.logout()
    expect(store.user).toBeNull()
    expect(store.isLoggedIn).toBe(false)
  })
})
```

## 集成测试

### 1. API集成测试
```python
# test_integration.py
async def test_user_flow(client):
    # 注册
    register_response = await client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123"
    })
    assert register_response.status_code == 201

    # 登录
    login_response = await client.post("/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # 创建占卜
    divination_response = await client.post(
        "/divination",
        json={
            "type": "answer_book",
            "question": "今天会下雨吗？"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert divination_response.status_code == 201
    divination_id = divination_response.json()["id"]

    # 收藏占卜
    favorite_response = await client.post(
        "/favorites",
        json={"record_id": divination_id},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert favorite_response.status_code == 201
```

### 2. 前端集成测试
```typescript
// test_user_flow.spec.ts
describe('User Flow', () => {
  it('completes user journey', async () => {
    // 访问首页
    const home = mount(Home)
    expect(home.find('h1').text()).toBe('天机阁')

    // 注册新用户
    const register = mount(Register)
    await register.find('input[name="email"]').setValue('test@example.com')
    await register.find('input[name="username"]').setValue('testuser')
    await register.find('input[name="password"]').setValue('password123')
    await register.find('form').trigger('submit')

    // 登录
    const login = mount(Login)
    await login.find('input[name="username"]').setValue('testuser')
    await login.find('input[name="password"]').setValue('password123')
    await login.find('form').trigger('submit')

    // 进行占卜
    const divination = mount(Divination)
    await divination.find('.divination-type').trigger('click')
    await divination.find('textarea').setValue('今天会下雨吗？')
    await divination.find('form').trigger('submit')

    // 查看历史记录
    const history = mount(History)
    expect(history.findAll('.record').length).toBeGreaterThan(0)
  })
})
```

## 性能测试

### 1. 负载测试
```bash
# 使用wrk进行负载测试
wrk -t12 -c400 -d30s http://localhost:8000/api/v1/health

# 使用ab进行并发测试
ab -n 1000 -c 100 http://localhost:8000/api/v1/health
```

### 2. 压力测试
```python
# test_stress.py
async def test_concurrent_requests():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(100):
            task = asyncio.create_task(
                session.post(
                    "http://localhost:8000/api/v1/divination",
                    json={
                        "type": "answer_book",
                        "question": "今天会下雨吗？"
                    }
                )
            )
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        success_count = sum(1 for r in responses if r.status == 201)
        assert success_count > 90  # 90%成功率
```

## 测试报告

### 1. 测试覆盖率
```bash
# 后端测试覆盖率
poetry run pytest --cov=app --cov-report=html

# 前端测试覆盖率
pnpm test:coverage
```

### 2. 测试结果分析
- 单元测试通过率
- 集成测试通过率
- 性能测试结果
- 发现的问题和解决方案

## 自动化测试

### 1. CI/CD集成
```yaml
# GitHub Actions配置
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Tests
        run: |
          poetry install
          poetry run pytest
```

### 2. 定期测试
```bash
# 创建定时任务
0 2 * * * cd /path/to/project && poetry run pytest >> /var/log/test.log 2>&1
```

## 测试注意事项

1. 每次提交代码前运行测试
2. 保持测试数据库独立
3. 及时更新测试用例
4. 定期检查测试覆盖率
5. 记录并跟踪测试问题 