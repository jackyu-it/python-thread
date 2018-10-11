import asyncio
import aiohttp
from random import randint

key = '4T6ZXUN71Y9ZBQGC'

class DataGet:
    @staticmethod
    async def aiohttp_get(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    @staticmethod
    async def fetch_async(stock, attempt=10, sleep_min=1, sleep_max=10):
        # init
        success, response = False, None
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=1min&apikey={}&interval=60min".format(stock, key)

        # get content
        cnt = True
        while cnt == True:
            attempt = attempt - 1

            try:
                print (url)
                response = await DataGet.aiohttp_get(url)
                cnt = False
                success = True
            except Exception as e:
                #print (e)
                if attempt > 0:
                    cnt = True
                else:
                    cnt = False
                asyncio.sleep(randint(sleep_min, sleep_max))

        return response

    @staticmethod
    async def asynchronous(stocks, attempt=3, sleep_min=5, sleep_max=20):
        stocks = [s.lower() for s in stocks]
        results = []

        cnt = True
        passed_stocks = []
        while cnt == True:
            attempt = attempt - 1

            futures = [DataGet.fetch_async(stock) for stock in stocks]
            for future in asyncio.as_completed(futures):
                result = await future
                try:
                    passed = result['Meta Data']['2. Symbol']
                    passed_stocks.append(passed)
                    results.append(result)
                except Exception as e:
                    #print (e)
                    pass

            # retry
            failed_stocks = list(set(stocks) - set(passed_stocks))
            if failed_stocks and attempt > 0 :
                cnt = True
                asyncio.sleep(randint(sleep_min, sleep_max))
            else:
                cnt = False

        failed_stocks = list(set(stocks) - set(passed_stocks))
        if failed_stocks:
            print ("Failed: " + str(failed_stocks))

    @staticmethod
    def get_groups(group):
        ioloop = asyncio.get_event_loop()
        ioloop.run_until_complete(DataGet.asynchronous(group))
        ioloop.close()

DataGet.get_groups(['msft', 'aapl'])