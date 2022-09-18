
from urllib.parse import quote
from email import header
from dotenv import load_dotenv
import os
import hmac
import hashlib
import requests
import json
from time import gmtime, strftime
import pyautogui

keyword = (pyautogui.prompt('키워드를 입력하세요'))
limit = pyautogui.prompt('갯수를 입력하세요')
keyword = quote(keyword)

REQUEST_METHOD = "GET"
DOMAIN = "https://api-gateway.coupang.com"
URL = f"/v2/providers/affiliate_open_api/apis/openapi/v1/products/search?keyword={keyword}&limit={limit}"

load_dotenv()
ACCESS_KEY = os.environ.get('COUPANG_ACCESS_KEY')
SECRET_KEY = os.environ.get('COUPANG_SECRET_KEY')

REQUEST = {"coupangUrls": [
    "https://www.coupang.com/np/search?component=&q=good&channel=user",
    "https://www.coupang.com/np/coupangglobal"
]}


def generateHmac(method, url, secretKey, accessKey):
    path, *query = url.split("?")
    datetimeGMT = strftime('%y%m%d', gmtime()) + 'T' + \
        strftime('%H%M%S', gmtime()) + 'Z'
    message = datetimeGMT + method + path + (query[0] if query else "")

    signature = hmac.new(bytes(secretKey, "utf-8"),
                         message.encode("utf-8"),
                         hashlib.sha256).hexdigest()

    return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(accessKey, datetimeGMT, signature)


authorization = generateHmac(REQUEST_METHOD, URL, SECRET_KEY, ACCESS_KEY)
headers = {
    "Authorization": authorization,
    "Content-Type": "application/json"
}
url = "{}{}".format(DOMAIN, URL)
response = requests.request(method=REQUEST_METHOD, url=url,
                            headers={
                                "Authorization": authorization,
                                "Content-Type": "application/json"
                            }
                            )

result = response.json()
productData = result['data']['productData']

for i in range(int(limit)):
    productName = productData[i]["productName"]
    productPrice = productData[i]["productPrice"]
    productImage = productData[i]["productImage"]
    print("=============이름============")
    print(productName)
    print("=============가격============")
    print(productPrice)
    print("=============사진============")
    print(productImage)
