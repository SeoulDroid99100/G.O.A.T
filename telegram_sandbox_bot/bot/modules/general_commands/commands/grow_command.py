from modules.base_module import BaseModule
from database.repositories.user_repository import UserRepository
import random

class GrowModule(BaseModule):
    @BaseModule.command('grow')
    async def grow_command(self, client, message):
        async with self.app.db_pool.acquire() as conn:
            repo = UserRepository(conn)
            user = await repo.get_user(message.from_user.id, message.chat.id)
            
            if user.can_grow_today():
                growth = self._calculate_growth(user)
                await repo.update_length(user, growth)
                await message.reply(self._growth_message(user, growth))
                
    def _calculate_growth(self, user):
        base_min = self.config.getint("ECONOMY", "BASE_GROWTH_MIN")
        base_max = self.config.getint("ECONOMY", "BASE_GROWTH_MAX")
        return random.randint(base_min, base_max) + user.debt * 0.001￼Enter
