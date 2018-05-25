import time
import asyncio
import aiohttp

key = '4T6ZXUN71Y9ZBQGC'

async def aiohttp_get(url):
    """Nothing to see here, carry on ..."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def fetch_async(stock):
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=1min&apikey={}&interval=60min".format(stock, key)
    response = await aiohttp_get(url)
    print (response)

async def asynchronous(stocks):
    tasks = [asyncio.ensure_future(
        fetch_async(stock)) for stock in stocks]
    await asyncio.wait(tasks)


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous(['rht', 'aapl', 'msft']))
ioloop.close()