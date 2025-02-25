class UserRepository:
    # ... existing methods ...
    
    async def get_eligible_users(self, chat_id: int):
        return await self.conn.fetch(
            "SELECT * FROM users WHERE chat_id = $1 "
            "AND last_growth >= NOW() - INTERVAL '7 days'",
            chat_id
        )

    async def apply_daily_bonus(self, user_id: int, chat_id: int, bonus: float):
        await self.conn.execute(
            "UPDATE users SET daily_bonus = daily_bonus + $1 "
            "WHERE user_id = $2 AND chat_id = $3",
            bonus, user_id, chat_id
        )

    async def update_loan(self, user_id: int, chat_id: int, new_length: float, new_debt: float):
        await self.conn.execute(
            "UPDATE users SET length = $1, debt = $2 "
            "WHERE user_id = $3 AND chat_id = $4",
            new_length, new_debt, user_id, chat_id
        )
