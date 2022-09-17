
import requests
from bs4 import BeautifulSoup
import time


def naver_news_crawling(url: str):
    response = requests.get(
        url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.select("div.info_group")
    for article in articles:
        links = article.select("a.info")
        if len(links) >= 2:  # 링크가 2개 이상이면 네이버 뉴스
            url = links[1].attrs['href']
            response = requests.get(url, headers={'User-agent': 'Mozila/5.0'})
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            if "entertain" in response.url:
                title = soup.select_one(".end_tit")
                content = soup.select_one("#articeBody")
            elif "sports" in response.url:
                title = soup.select_one("h4.title")
                content = soup.select_one("#newsEndContents")
                # 불필요한 div, p 삭제
                divTags = content.select("div")
                pTags = content.select("p")
                for div in divTags:
                    div.decompose()
                for p in pTags:
                    p.decompose()
            else:
                title = soup.select_one(".media_end_head_title")
                content = soup.select_one("#newsct_article")

            print("========= 링크 ==========\n", url)
            print("========= 제목 ==========\n", title.text.strip())
            print("========= 본문 ==========\n", content.text.strip())
            time.sleep(0.3)
