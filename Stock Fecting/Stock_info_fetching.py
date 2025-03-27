import requests as req
import pandas as pd
import time
import schedule

def get_stock():
    res = req.get('https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL')
    data = res.json()
    df = pd.DataFrame(data)
    
    localtime = time.localtime()
    now = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
    df.to_csv(f"{now}.csv", encoding='utf_8_sig', index=False)
    print(f'{now} 取得股票資訊')

schedule.every(5).seconds.do(get_stock)

while True:
    schedule.run_pending()
    time.sleep(1)