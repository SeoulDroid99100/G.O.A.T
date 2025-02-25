from pyrogram import filters
from core.decorators import command

class BaseModule:
    def __init__(self, app, config, metrics):
        self.app = app
        self.config = config
        self.metrics = metrics
        
    def register(self):
        """Auto-registers all decorated commands"""
        for name in dir(self):
            method = getattr(self, name)
            if hasattr(method, "_command"):
                filters, kwargs = method._command
                self.app.add_handler(method, **kwargs)
                
    @classmethod
    def command(cls, name: str, **kwargs):
        def decorator(func):
            @filters.command(name)
            async def wrapper(self, client, message):
                async with self.monitoring.track_command(client, message, name):
                    return await func(self, client, message)
            wrapper._command = (filters.command(name), kwargs)
            return wrapper
        return decorator
