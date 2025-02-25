# bot/core/bot_instance.py
from pyrogram import Client
from configparser import ConfigParser
from core.logger import logger
from core.plugin_loader import PluginLoader
from core.middleware import register_middleware
from core.error_handler import setup_error_handling
from database.connection import init_db_pool
from modules.general_commands.daily_election import DailyElection
from modules.general_commands.handlers.inline_handlers import InlineHandlers

def create_bot(config: ConfigParser) -> Client:
    """Factory function to create and configure the bot instance"""
    
    # Initialize Pyrogram client
    app = Client(
        name="dick_bot",
        api_id=config.getint("BOT", "API_ID"),
        api_hash=config.get("BOT", "API_HASH"),
        bot_token=config.get("BOT", "BOT_TOKEN"),
        workdir=config.get("BOT", "WORKDIR", fallback="/var/tmp"),
        plugins=dict(root="bot/modules")
    )
    
    # Initialize core components
    plugin_loader = PluginLoader(app, config)
    election_scheduler = DailyElection(app)

    @app.on_startup()
    async def startup():
        """Initialize application resources"""
        try:
            # Initialize database connection pool
            app.db_pool = await init_db_pool(config)
            logger.info("Database pool initialized with %s connections", 
                       config.getint("DATABASE", "POOL_MIN"))

            # Start background services
            await election_scheduler.start()
            logger.info("Daily election scheduler started")

            # Load plugins
            plugin_loader.load_from_path("modules.general_commands")
            plugin_loader.load_from_path("modules.minigames")
            logger.info("Plugin loading completed")

            # Register core middleware
            register_middleware(app)
            logger.info("Middleware registered")

            # Setup error handling
            setup_error_handling(app)
            logger.info("Error handlers configured")

            # Register inline query handler
            app.add_handler(InlineHandlers.handle_inline_query)
            logger.info("Inline query handler registered")

            logger.info("Bot startup sequence completed successfully")
            
        except Exception as e:
            logger.critical("Startup failed: %s", str(e))
            raise

    @app.on_shutdown()
    async def shutdown():
        """Cleanup application resources"""
        try:
            # Close database pool
            if hasattr(app, 'db_pool'):
                await app.db_pool.close()
                logger.info("Database pool closed")

            # Stop scheduler
            if election_scheduler.scheduler.running:
                election_scheduler.scheduler.shutdown()
                logger.info("Election scheduler stopped")

            logger.info("Bot shutdown sequence completed")
            
        except Exception as e:
            logger.error("Shutdown error: %s", str(e))

    return app
