import asyncio
from core.bot_instance import create_bot
from core.config_loader import load_config
from core.metrics import start_metrics_server
from core.logger import setup_logging

async def main():
    config = load_config()
    setup_logging(config)
    start_metrics_server(config.getint("METRICS", "PORT", 8000))
    
    bot = create_bot(config)
    await bot.start()
    
    # Register plugins from multiple directories
    bot.plugin_loader.load_from_path("modules.general_commands")
    bot.plugin_loader.load_from_path("modules.minigames")
    
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
