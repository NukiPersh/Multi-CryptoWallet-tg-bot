import asyncio
import asyncpg
from asyncpg.exceptions import InvalidCatalogNameError, DuplicateDatabaseError

async def create_database():
    admin_conn = await asyncpg.connect(
        user='postgres',
        password='ваш_пароль_postgres',  # пароль суперпользователя
        host='localhost',
        database='postgres'  # подключаемся к стандартной БД
    )
    try:
        await admin_conn.execute('CREATE DATABASE crypto_wallet')
        print("База данных crypto_wallet создана")
    except DuplicateDatabaseError:
        print("База данных уже существует")
    finally:
        await admin_conn.close()

async def create_tables(pool):
    async with pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                id_telegram BIGINT UNIQUE NOT NULL,
                privacykey TEXT,
                address TEXT
            )
        ''')
        
async def create_db_pool():
    """Создает пул подключений с обработкой ошибок"""
    try:
        pool = await asyncpg.create_pool(
            user='crypto_user',
            password='ваш_пароль',
            database='crypto_wallet',
            host='localhost',
            min_size=1,
            max_size=5
        )
        return pool
    except InvalidCatalogNameError:
        print("База данных не существует, пытаемся создать...")
        await create_database()
        return await create_db_pool()
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        raise


async def main():
    try:
        # Создаем или подключаемся к базе данных
        pool = await create_db_pool()
        
        # Создаем таблицы
        await create_tables(pool)
        
        # Тестовое подключение
        async with pool.acquire() as conn:
            version = await conn.fetchval('SELECT version()')
            print(f"Подключение успешно. Версия PostgreSQL: {version.split(',')[0]}")
            
    except Exception as e:
        print(f"Критическая ошибка: {e}")
    finally:
        if 'pool' in locals():
            await pool.close()

if __name__ == "__main__":
    asyncio.run(main())