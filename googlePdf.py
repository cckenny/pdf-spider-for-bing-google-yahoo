# -*- coding: <utf-8> -*-
import requests
import re
import sys
import io
import os
import time
from bs4 import BeautifulSoup
from random import randint
import random

class googlePdf():
    def __init__(self, search_list, download_dir=None, pages=5, start_date=None, end_date=None, filetype='pdf'):
        self.search_list = search_list
        self.pages = pages
        self.start_date = start_date
        self.end_date = end_date
        self.titlelist = []

        if download_dir == None:
            self.download_dir = os.path.join(".", "download", "")
        else:
            self.download_dir = download_dir

        if start_date == None and end_date == None:
            self.enable_date = False
        else:
            self.enable_date = True

        self.filetype = filetype

        os.makedirs(self.download_dir, exist_ok=True)

    def download_search_data(self, time_sleep=True):
        for search in self.search_list:
            links = self.get_link(search, filetype=self.filetype, start_date=self.start_date, end_date=self.end_date, pages=self.pages, show_links=True)
            self.download_pdf_from_links(search, links, self.filetype, self.download_dir)
            print("")
            if time_sleep:
                time.sleep(randint(1, 2))

    def is_downloadable(self, url):
        try:
            h = requests.head(url, allow_redirects=False)
            header = h.headers
            content_type = header.get('content-type')
            if 'text' in content_type.lower():
                return False
            if 'html' in content_type.lower():
                return False
            return True
        except:
            return False

    def get_link(self, search_keyword, filetype, start_date, end_date, pages, enable_date=False, show_links=False):
        linklist = []
        titlelist = []
        print("search keyword : ", search_keyword)
        print("expected time(getting links) : ", pages * 4, "seconds~", pages * 5, "seconds")
        print("----getting links----")
        for page in range(0, pages * 10 , 10):
            while True:
                params = {}
                params['as_epq'] = search_keyword
                if enable_date:
                    params['tbs'] = "cdr:1,cd_min:" + start_date + ",cd_max:" + end_date
                params['start'] = str(page)
                params['as_filetype'] = filetype
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit /537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}

                proxy_list = [
                    {"http" : "socks5://127.0.0.1:1080", "https" : "socks5://127.0.0.1:1080"},
                ]#代理列表
                proxy = random.choice(proxy_list)

                html = requests.get("https://www.google.com/search", params=params, headers=headers, proxies=proxy)
                print(html.status_code)
                if html.status_code != 200:
                    continue
                break        
            soup = BeautifulSoup(html.text, 'lxml')
            # soup = BeautifulSoup(htmlpage.text, 'lxml')

            for result_table in soup.findAll("div", {"class": "r"}):
                a_click = result_table.find("a")
                if self.is_downloadable(a_click['href']):
                    if show_links == True:
                        print(str(a_click.renderContents())[2:-1], end='  ')
                        print(a_click['href'])
                    linklist.append(a_click['href'])
                    titlelist.append(str(a_click.renderContents())[2:-1])

            time.sleep(randint(5, 6))

        self.titlelist = titlelist
        return linklist

    def download_pdf_from_links(self, search, links, filetype, directory):
        print("----downloading----")
        print("files to download : ", len(links))
        for num, link in enumerate(links):
            try:
                r = requests.get(link, stream=True)
                os.makedirs(os.path.join(directory, search), exist_ok=True)
                with open(os.path.join(directory, search, "") + search + str(num + 1) + '.' + filetype, 'wb') as f:
                    f.write(r.content)
                print(str((num + 1) / len(links) * 100) + "% done")
            except:
                print("download error on : ", link)

  


if __name__=="__main__":
    pdfcrawler = googlePdf(['deep learning'], pages=3, start_date=None, end_date=None, filetype='pdf')#关键词 页码 起止日期 文件类型
    pdfcrawler.download_search_data()     #download pdfs from list -> ["svm"]
    #pdfcrawler.convert_pdfs(to_json=True)     #convert all pdfs to txt, json file could be used as DataFrame
    #pdfcrawler.concate_all_txt()  #concate txt files each by search keyword -> to analyze whole txt data
