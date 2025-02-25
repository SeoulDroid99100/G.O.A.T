import time
from pyrogram import filters
from pyrogram.types import Message
from prometheus_client import Counter, Histogram

class Monitoring:
    def __init__(self, metrics):
        self.metrics = metrics
        
    async def track_command(self, client, message: Message, command: str):
        start_time = time.time()
        
        try:
            yield
            duration = time.time() - start_time
            self.metrics['commands'].labels(command).inc()
            self.metrics['latency'].labels(command).observe(duration)
        except Exception as e:
            self.metrics['errors'].labels(command).inc()
            raise

def register_monitoring(app, metrics):
    monitor = Monitoring(metrics)
    app.add_handler(monitor.track_command, group=-1)
