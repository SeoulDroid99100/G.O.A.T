from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.repositories.user_repository import UserRepository

class DailyElection:
    def __init__(self, app):
        self.app = app
        self.scheduler = AsyncIOScheduler()

    async def start(self):
        self.scheduler.add_job(self.run_elections, 'cron', hour=0)
        self.scheduler.start()

    async def run_elections(self):
        async with self.app.db_pool.acquire() as conn:
            repo = UserRepository(conn)
            all_chats = await repo.get_all_chats()
            
            for chat in all_chats:
                candidates = await repo.get_eligible_users(chat.id)
                if candidates:
                    winner = random.choice(candidates)
                    bonus = random.uniform(1.0, 5.0)
                    await repo.apply_daily_bonus(winner.user_id, chat.id, bonus)
                    
                    await self.app.send_message(
                        chat.id,
                        f"🎉 Daily Dick of the Day: {winner.username}\n"
                        f"➕ Received bonus: {bonus:.1f}cm!"
                    )
