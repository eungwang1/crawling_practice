
from bz2 import compress
from turtle import st
from bs4 import BeautifulSoup
from urllib.parse import quote
from dotenv import load_dotenv
import os
import requests
import json
import time
import pyautogui
from util import generateHmac
import pyperclip

load_dotenv()
ACCESS_KEY = os.environ.get('COUPANG_ACCESS_KEY')
SECRET_KEY = os.environ.get('COUPANG_SECRET_KEY')
COUPANG_DOMAIN = os.environ.get('COUPANG_DOMAIN')
COUPANG_API_DEEPLINK = os.environ.get('COUPANG_API_DEEPLINK')

user_header = {
    'Host': 'www.coupang.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
}


page = 1
count = 0
content = ''
keyword = pyautogui.prompt('검색어를 입력해주세요.')
total_count = int(pyautogui.prompt('상품의 갯수를 입력해주세요.'))
while True:
    if count == total_count:
        break
    response = requests.get(
        f'https://www.coupang.com/np/search?component=&q={keyword}&channel=user&page={page}', headers=user_header)
    page = page + 1
    html_page = response.text
    soup_page = BeautifulSoup(html_page, 'html.parser')
    products = soup_page.select(".search-product-link")
    for product in products:
        if count == total_count:
            break
        isAd = product.select_one(".ad-badge-text")
        isBestSeller = product.select_one(".best-seller-search-product-wrap")
        if isAd or isBestSeller:
            continue
        product_url = product.attrs['href']
        response = requests.get(
            f"https://www.coupang.com{product_url}", headers=user_header)
        product_url = response.url
        html_detail = response.text
        soup_detail = BeautifulSoup(html_detail, "html.parser")
        star_width = soup_detail.select_one(".rating-star-num").attrs['style']
        startIndex = star_width.index(": ") + 1
        endIndex = star_width.index(".")
        star_width = star_width[startIndex:endIndex]
        score = int(star_width)*5/100
        score_count = soup_detail.select_one("span.count").text.strip()
        brand_name = soup_detail.select_one(".prod-brand-name").text.strip()
        product_name = soup_detail.select_one(
            ".prod-buy-header__title").text.strip()
        proudct_price = soup_detail.select_one(".total-price").text.strip()

        REQUEST = {"coupangUrls": [product_url]}
        authorization = generateHmac(
            "POST", COUPANG_API_DEEPLINK, SECRET_KEY, ACCESS_KEY)
        partners_header = {
            "Authorization": authorization,
            "Content-Type": "application/json"
        }
        url = "{}{}".format(COUPANG_DOMAIN, COUPANG_API_DEEPLINK)
        try:
            response = requests.request(
                method="POST", url=url, headers=partners_header, data=json.dumps(REQUEST))
            result = response.json()
            partners_url = result['data'][0]['shortenUrl']
            count = count + 1
            content += f"{str(count)}.{product_name}\n별점:{score}({score_count})\n{partners_url}\n\n"
            time.sleep(0.3)
        except KeyError:
            print(f'error : {KeyError}')
            print(f'url : {response.url}')
content += '\n포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.'
pyperclip.copy(content)
print(content)
