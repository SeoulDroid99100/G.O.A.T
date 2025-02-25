CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT NOT NULL,
    chat_id BIGINT NOT NULL,
    length FLOAT NOT NULL DEFAULT 0,
    debt FLOAT NOT NULL DEFAULT 0,
    last_growth TIMESTAMP,
    last_pvp TIMESTAMP,
    daily_bonus FLOAT DEFAULT 0,
    username VARCHAR(32),
    PRIMARY KEY (user_id, chat_id)
);

CREATE INDEX idx_user_activity ON users (last_growth);
CREATE INDEX idx_chat_ranking ON users (chat_id, length DESC);
