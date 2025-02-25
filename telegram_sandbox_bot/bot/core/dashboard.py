from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from pyrogram import filters

def register_metrics_endpoint(app):
    @app.on_message(filters.command("metrics"))
    async def metrics_endpoint(client, message):
        if message.from_user.id != app.config.getint("BOT", "ADMIN_ID"):
            return
            
        data = generate_latest()
        await message.reply(data.decode(), parse_mode=None)
