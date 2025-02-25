from pyrogram import filters
from modules.base_module import BaseModule
from database.repositories.user_repository import UserRepository

class PvPModule(BaseModule):
    @BaseModule.command('pvp')
    async def handle_pvp(self, client, message):
        args = message.text.split()
        if len(args) != 3:
            await message.reply("Usage: /pvp @username <amount>")
            return

        target_username = args[1].lstrip('@')
        try:
            bet = float(args[2])
        except ValueError:
            await message.reply("Invalid bet amount")
            return

        async with self.app.db_pool.acquire() as conn:
            repo = UserRepository(conn)
            challenger = await repo.get_user(message.from_user.id, message.chat.id)
            target_user = await repo.get_by_username(target_username, message.chat.id)

            if not self._validate_bet(challenger, target_user, bet):
                return

            # 50/50 chance battle
            if random.random() < 0.5:
                winner, loser = challenger, target_user
            else:
                winner, loser = target_user, challenger

            await repo.update_length(winner.user_id, winner.chat_id, winner.length + bet)
            await repo.update_length(loser.user_id, loser.chat_id, loser.length - bet)

            await message.reply(
                f"🏆 {winner.username} won {bet}cm!\n"
                f"📉 {loser.username} lost {bet}cm!"
            )

    def _validate_bet(self, challenger, target, bet):
        if challenger.length < bet:
            await message.reply("Your length is too small for this bet!")
            return False
        if target.length < bet:
            await message.reply("Opponent's length is too small for this bet!")
            return False
        if challenger.last_pvp and (datetime.now() - challenger.last_pvp).hours < 1:
            await message.reply("You can only fight once per hour!")
            return False
        return True
