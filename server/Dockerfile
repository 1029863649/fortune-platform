# 构建阶段
FROM python:3.9-slim as builder

# 设置工作目录
WORKDIR /app

# 安装Poetry
RUN pip install poetry

# 复制项目文件
COPY pyproject.toml poetry.lock ./
COPY app app/
COPY alembic.ini .
COPY alembic alembic/

# 配置Poetry不创建虚拟环境
RUN poetry config virtualenvs.create false

# 安装依赖
RUN poetry install --no-dev --no-interaction --no-ansi

# 运行阶段
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 从构建阶段复制依赖和代码
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app .

# 设置环境变量
ENV PYTHONPATH=/app

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 