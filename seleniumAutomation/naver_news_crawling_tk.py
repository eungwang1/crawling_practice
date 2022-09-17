from tkinter import *
from tkinter import ttk
import naver_news_crawling

root = Tk()
root.geometry("800x800")
frm = ttk.Frame(root, padding=10)


def crawling():
    try:
        keyword = input_keyword.get()
        lastPage = int(input_page.get())
        # 0 - 1페이지, 11- 2페이지
        for i in range(lastPage):
            itemCount = str(i*10 + 1)
            url = f"https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query={keyword}&start={itemCount}"
            naver_news_crawling.naver_news_crawling(url)
    except ValueError as e:
        print(e)
        print('입력값을 확인하세요')


# page 라벨
label_page = Label(root)
label_page.config(text="page")
label_page.pack()

# page 입력창
input_page = Entry(root)
input_page.pack()

# keyword 라벨
label_keyword = Label(root)
label_keyword.config(text="keyword")
label_keyword.pack()

# keyword 입력창
input_keyword = Entry(root)
input_keyword.pack()


# 실행 버튼
btn1 = Button(root)
btn1.config(text="crawling")
btn1.config(command=crawling)
btn1.pack()

root.mainloop()
