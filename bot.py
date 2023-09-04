import telegram
import asyncio
from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
import schedule
import time
import sys

token = '{본인의 Telegram token}'
bot = telegram.Bot(token=token)
chat_id = {본인의 Telegram bot chat id}
cnt = 0
def get_product_info():
    with requests.Session() as s:
        url_org = '{크롤링 할 물품 상세페이지 url}'
        url = Request(url_org, headers={'User-Agent':'Mozilla/5.0'}) #웹사이트 403 에러 방지용
        
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        p_sell = soup.select('.btnBlack.displaynone') #품절이 아닌 경우 활성화되는 클래스
        
        if len(p_sell) > 0:
            return True
        else: #soldout
            return False
			
def get_goods_info():
    with requests.Session() as s:
        url_org = '{크롤링 할 물품2 상세페이지 url}' #두 물품을 보기 위해 하나 추가
        url = Request(url_org, headers={'User-Agent':'Mozilla/5.0'})

        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        g_sell = soup.select('.btnBlack.displaynone')

        if len(g_sell) > 0:
            return True
        else: #soldout
            return False
			
async def send_msg():
    global cnt
    while True:
        text = "Gotcha!"
        if get_product_info()==True or get_goods_info()==True: #둘 중 하나라도 입고되면
            text="입고"
            cnt = 0
            await bot.sendMessage(chat_id, text=text)
        elif cnt==30: #중간중간 상황 보고(15분마다)
            text="입고 전"
            cnt = 0
            await bot.sendMessage(chat_id, text=text)
		else:
            cnt += 1
        await asyncio.sleep(30) #30초마다 체크

async def main():
    task = asyncio.create_task(send_msg())
    await task
if __name__ == "__main__":
    asyncio.run(main())
