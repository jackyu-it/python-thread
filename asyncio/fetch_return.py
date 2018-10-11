import asyncio
import aiohttp
from random import randint

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
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=%s&interval=1min&apikey=%s" % (
            stock, CONFIG['ALPHA_ADVANTAGE_KEYS'][0])

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
                if attempt > 0:
                    cnt = True
                else:
                    cnt = False
                asyncio.sleep(randint(sleep_min, sleep_max))

        return response

    @staticmethod
    def get_groups(group):
        # ioloop
        ioloop = asyncio.get_event_loop()
        tasks = [DataGet.fetch_async(stock) for stock in group]
        results = ioloop.run_until_complete(asyncio.gather(*tasks))
        ioloop.close()

        # check
        passed_stocks = [result['Meta Data']['2. Symbol'] for result in results]
        failed_stocks = list(set(group) - set(passed_stocks))
        if failed_stocks:
            print ("Failed: " + str(failed_stocks))
        return results, failed_stocks


def load_db(results):
    for data in results:
        if 'Time Series (1min)' in data.decode('utf-8'):
            # get symbol obj
            symbol = result['Meta Data']['2. Symbol']
            symbol_obj = Symbol.objects.get(symbol_iexact=symbol)

            # data
            d = data['Time Series (1min)']
            key = list(d.keys())[0]
            row = d[key]
            prev_close = -1

            try:
                change_percent = (float(row['4. close']) - float(prev_close)) / float(prev_close)
            except (ValueError, ZeroDivisionError):
                change_percent = 0

            if 'N/A' not in str(row):
                dict = {'symbol': symbol_obj,
                        'date': pytz.utc.localize(parser.parse(key, dayfirst=False, yearfirst=True)),
                        'defaults': {'price': row['4. close'],
                                     'change_percent': -1,
                                     'change_amount': -1,
                                     'volume': row['5. volume'],
                                     'prev_close': prev_close,
                                     'day_low': row['3. low'],
                                     'day_high': row['2. high'],
                                     'day_open': row['1. open'],
                                     'avg_volume': -1}}
                obj = Utils.dict_to_instance(Pricing, dict)


def load_daily(reset_queue=False, symbols = []):
    # log
    if reset_queue:
        Utils.reset_log(CONFIG['DAILY_API_LOG_FILE'])
    last_id = Utils.read_log(CONFIG['DAILY_API_LOG_FILE'])
    logging.info('Load daily last api ID is: %d\n' % (last_id))

    # get symbols
    symbol_objs = Utils.filter_synmbol_objs(symbols)
    symbols = [s.symbol for s in symbol_objs]

    # get chuncks
    n = 100
    chunks = [symbols[i * n:(i + 1) * n] for i in range((len(symbols) + n - 1) // n)]

    # process chunks ß
    for chunck in chunks:
        results, failed_stocks = DataGet.get_groups(chunck)
        load_db(results)




