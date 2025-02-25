from pyrogram import filters
from modules.base_module import BaseModule
from database.repositories.user_repository import UserRepository

class ImportModule(BaseModule):
    @BaseModule.command('import')
    async def handle_import(self, client, message):
        if not message.reply_to_message:
            await message.reply("Reply to a bot's message to import data")
            return

        target_msg = message.reply_to_message
        supported_bots = self.config.get("BOT", "SUPPORTED_IMPORT_BOTS").split(',')
        
        if target_msg.from_user.username not in supported_bots:
            await message.reply("❌ Unsupported bot for import")
            return

        if not await self._has_admin_rights(client, message):
            await message.reply("⚠️ Bot needs admin rights to import data")
            return

        parsed_data = await self.parse_import_message(target_msg.text)
        
        async with self.app.db_pool.acquire() as conn:
            repo = UserRepository(conn)
            for user_data in parsed_data:
                user = await repo.get_by_username(user_data['username'], message.chat.id)
                if user:
                    await repo.update_length(
                        user.user_id,
                        user.chat_id,
                        user.length + user_data['length']
                    )

        await message.reply("✅ Successfully imported historical data!")

    async def _has_admin_rights(self, client, message):
        chat_member = await client.get_chat_member(message.chat.id, "me")
        return chat_member.privileges.can_read_messages
