from asyncpg import create_pool
from contextlib import asynccontextmanager

class ConnectionPool:
    def __init__(self, config):
        self.config = config
        self.pool = None
        
    async def connect(self):
        self.pool = await create_pool(
            dsn=self.config["DATABASE"]["DSN"],
            min_size=self.config.getint("DATABASE", "POOL_MIN"),
            max_size=self.config.getint("DATABASE", "POOL_MAX"),
            timeout=30,
            command_timeout=5
        )
        
    @asynccontextmanager
    async def acquire(self):
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                yield conn
