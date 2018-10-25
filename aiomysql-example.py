import asyncio
from aiomysql import create_pool
import time
import pymysql


async def create_mysql_pool(loop):
    pool = await create_pool(host='', port=3306,
                       user='', password='',
                       db='', loop=loop)

    return pool


async def close_mysql_pool(pool):
    pool.close()
    await pool.wait_closed()

async def test_example(pool,sql):

    print(pool)
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql)
            data = await cur.fetchall()
    return data



if __name__ == '__main__':
    t1 = time.time()
    loop = asyncio.get_event_loop()
    pool = loop.run_until_complete(create_mysql_pool(loop))
    to_do = [test_example(pool,'SELECT * FROM table'),test_example(pool,'SELECT * FROM table'),test_example(pool,'SELECT * FROM table'),test_example(pool,'SELECT * FROM table')]
    wait_coro = asyncio.wait(to_do)
    res,_ = loop.run_until_complete(wait_coro)
    loop.run_until_complete(close_mysql_pool(pool))
    
    print((time.time() - t1))
