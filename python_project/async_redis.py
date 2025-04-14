import logging
from logging.handlers import TimedRotatingFileHandler
from contextlib import asynccontextmanager

# 日志配置
log_handler = TimedRotatingFileHandler(
    'async_redis_log.log', when='midnight', interval=1, backupCount=7, encoding='utf-8'
)
log_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)


from redis import asyncio as aioredis

class AsyncRedisServer:
    def __init__(self):
        self.redis_url = "redis://:abcd@127.0.0.1:6379/4"
        self.redis = None
        
    async def connect(self):
        """
        连接Redis服务器
        @returns {None}
        """
        if self.redis is None:
            self.redis = await aioredis.from_url(self.redis_url)
            logger.info("Redis连接已建立")

    async def close(self):
        """
        关闭Redis连接
        @returns {None}
        """
        if self.redis is not None:
            await self.redis.close()
            self.redis = None
            logger.info("Redis连接已关闭")
            
    @asynccontextmanager
    async def get_redis(self):
        """
        获取Redis连接的异步上下文管理器
        @returns {aioredis.Redis} Redis连接实例
        """
        await self.connect()
        try:
            yield self.redis
        finally:
            await self.close()

# 创建全局实例
async_redis_server = AsyncRedisServer()
