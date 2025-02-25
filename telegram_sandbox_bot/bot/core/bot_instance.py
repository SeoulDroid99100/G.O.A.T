def create_bot(config):
    # Initialize Pyrogram client with configuration
    app = Client(
        name="dick_bot",
        api_id=config.getint("BOT", "API_ID"),
        api_hash=config.get("BOT", "API_HASH"),
        bot_token=config.get("BOT", "BOT_TOKEN"),
        workdir=config.get("BOT", "WORKDIR", fallback="/tmp"),
        plugins=dict(root="bot/modules")
    )
    
    # Initialize core components
    election = DailyElection(app)
    plugin_loader = PluginLoader(app, config)
    
    @app.on_startup()
    async def startup():
        # Initialize database connection pool
        app.db_pool = await init_db_pool(config)
        
        # Start daily election scheduler
        await election.start()
        
        # Load all plugins automatically
        plugin_loader.load_from_path("modules.general_commands")
        plugin_loader.load_from_path("modules.minigames")
        
        # Register core middleware
        from core.middleware import register_middleware
        register_middleware(app)
        
        # Initialize error handling
        from core.error_handler import setup_error_handling
        setup_error_handling(app)
        
        # Register inline query handler
        from modules.general_commands.handlers.inline_handlers import InlineHandlers
        app.add_handler(InlineHandlers.handle_inline_query)
        
        logger.info("Bot startup completed")

    @app.on_shutdown()
    async def shutdown():
        # Cleanup resources
        await app.db_pool.close()
        election.scheduler.shutdown()
        logger.info("Bot shutdown completed")

    return app
