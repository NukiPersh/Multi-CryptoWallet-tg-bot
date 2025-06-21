import asyncio
import asyncpg
from asyncpg.pool import Pool
import logging
from config_reader import config


# Настройки подключения и пула
POSTGRES_CONFIG = {
    'user': config.user.get_secret_value(),
    'password': config.password.get_secret_value(),
    'database': config.database.get_secret_value(),
    'host': config.host.get_secret_value(),
    'port': config.port.get_secret_value(),
    'min_size': 20,      # Минимальное количество соединений
    'max_size': 100,     # Максимальное количество соединений
    'max_inactive_connection_lifetime': 300  # Время жизни неактивного соединения
}

# Глобальный пул соединений
db_pool: Pool = None

# Логгер
logger = logging.getLogger('db')

async def create_db_pool():
    global db_pool
    db_pool = await asyncpg.create_pool(**POSTGRES_CONFIG)
    logger.info("Database connection pool created")

async def close_db_pool():
    if db_pool:
        await db_pool.close()
        logger.info("Database connection pool closed")

async def add_new_user(id_telegram):
    async with db_pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO users (id_telegram) 
            VALUES ($1) 
            ON CONFLICT (id_telegram) DO NOTHING
        """, id_telegram)
        logger.debug(f"User {id_telegram} added or already exists")

async def check_wallet_in_db(telegram_id):
    async with db_pool.acquire() as conn:
        return await conn.fetchval("""
            SELECT EXISTS(
                SELECT 1 FROM users 
                WHERE id_telegram = $1 AND address IS NOT NULL
            )
        """, telegram_id)

async def get_address(telegram_id):
    async with db_pool.acquire() as conn:
        return await conn.fetchval("""
            SELECT address FROM users 
            WHERE id_telegram = $1
        """, telegram_id)

async def get_privacy_key(telegram_id):
    async with db_pool.acquire() as conn:
        return await conn.fetchval("""
            SELECT privacykey FROM users 
            WHERE id_telegram = $1
        """, telegram_id)

async def delete_wallet_from_db(telegram_id):
    async with db_pool.acquire() as conn:
        await conn.execute("""
            UPDATE users 
            SET privacykey = NULL, address = NULL 
            WHERE id_telegram = $1
        """, telegram_id)
        logger.debug(f"Wallet deleted for user {telegram_id}")

async def add_wallet_to_db(telegram_id, private_key, address):
    async with db_pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO users (id_telegram, privacykey, address) 
            VALUES ($1, $2, $3)
            ON CONFLICT (id_telegram) DO UPDATE 
            SET privacykey = EXCLUDED.privacykey, 
                address = EXCLUDED.address
        """, telegram_id, private_key, address)
        logger.debug(f"Wallet added/updated for user {telegram_id}")