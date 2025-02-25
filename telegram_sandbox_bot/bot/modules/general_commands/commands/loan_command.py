from pyrogram import filters
from modules.base_module import BaseModule
from database.repositories.user_repository import UserRepository

class LoanModule(BaseModule):
    @BaseModule.command('loan')
    async def handle_loan(self, client, message):
        async with self.app.db_pool.acquire() as conn:
            repo = UserRepository(conn)
            user = await repo.get_user(message.from_user.id, message.chat.id)
            
            if user.length >= 0:
                await message.reply("ℹ️ You don't need a loan!")
                return
                
            debt = abs(user.length)
            await repo.update_loan(
                user.user_id,
                user.chat_id,
                new_length=0,
                new_debt=user.debt + debt
            )
            
            await message.reply(
                f"💸 Loan approved! {debt:.1f}cm debt converted to credit.\n"
                f"Each growth will deduct {self.config.getfloat('ECONOMY', 'LOAN_RECOVERY_RATE')*100}% for repayment."
            )
