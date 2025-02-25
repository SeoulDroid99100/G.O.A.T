from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    chat_id: int
    length: float = 0.0
    debt: float = 0.0
    last_growth: datetime = None
    last_pvp: datetime = None
    daily_bonus: float = 0.0
    username: str = None

    def can_grow_today(self):
        return not self.last_growth or \
            (datetime.now() - self.last_growth).days >= 1

    def eligible_for_daily_election(self):
        return self.last_growth and \
            (datetime.now() - self.last_growth).days <= 7
