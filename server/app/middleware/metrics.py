from typing import Callable
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram, Gauge
import psutil

# 请求计数器
REQUEST_COUNT = Counter(
    'app_request_count',
    'Application Request Count',
    ['method', 'endpoint', 'status']
)

# 请求延迟直方图
REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Application Request Latency',
    ['method', 'endpoint']
)

# 活跃请求数
ACTIVE_REQUESTS = Gauge(
    'app_active_requests',
    'Application Active Requests'
)

# 系统资源使用
CPU_USAGE = Gauge('system_cpu_usage', 'System CPU Usage')
MEMORY_USAGE = Gauge('system_memory_usage', 'System Memory Usage')
DISK_USAGE = Gauge('system_disk_usage', 'System Disk Usage')

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        # 增加活跃请求计数
        ACTIVE_REQUESTS.inc()
        
        # 记录开始时间
        start_time = time.time()
        
        try:
            response = await call_next(request)
            
            # 记录请求延迟
            latency = time.time() - start_time
            REQUEST_LATENCY.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(latency)
            
            # 记录请求计数
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            ).inc()
            
            return response
            
        finally:
            # 减少活跃请求计数
            ACTIVE_REQUESTS.dec()

def update_system_metrics():
    """更新系统资源使用指标"""
    CPU_USAGE.set(psutil.cpu_percent())
    memory = psutil.virtual_memory()
    MEMORY_USAGE.set(memory.percent)
    disk = psutil.disk_usage('/')
    DISK_USAGE.set(disk.percent) 