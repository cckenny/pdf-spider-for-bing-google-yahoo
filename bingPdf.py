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

class bingPdf():
    def __init__(self, search_list, download_dir=None, pages=5, filetype='pdf'):
        self.search_list = search_list
        self.pages = pages
        self.titlelist = []

        if download_dir == None:
            self.download_dir = os.path.join(".", "download", "")
        else:
            self.download_dir = download_dir

        self.filetype = filetype

        os.makedirs(self.download_dir, exist_ok=True)

    def download_search_data(self, time_sleep=True):
        for search in self.search_list:
            links = self.get_link(search, filetype=self.filetype, pages=self.pages, show_links=True)
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

    def get_link(self, search_keyword, filetype, pages, show_links=False):
        linklist = []
        titlelist = []
        print("search keyword : ", search_keyword)
        print("expected time(getting links) : ", pages * 4, "seconds~", pages * 5, "seconds")
        print("----getting links----")
        for page in range(0, pages * 14 , 14):
            while True:
                params = {}
                word = search_keyword + ' filetype:' + filetype
                print(word)
                word = word.encode(encoding='utf-8', errors='strict')
                #print(word)
                params['q'] = word
                params['first'] = str(11 + page)
                params['FROM'] = 'PERE' + str(1 + page / 14)

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit /537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}

                proxy_list = [
                    {"http" : "185.190.40.75:8080"}
                ]#代理列表
                proxy = random.choice(proxy_list)

                html = requests.get("http://cn.bing.com/search", params=params, headers=headers, proxies=proxy)
                print(proxy)
                print(html.status_code)
                if html.status_code != 200:
                    continue
                break        
            soup = BeautifulSoup(html.text, 'lxml')
            # soup = BeautifulSoup(htmlpage.text, 'lxml')

            for result_table in soup.findAll("h2"):
                a_click = result_table.find("a")
                if a_click != None and self.is_downloadable(a_click['href']):
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
    pdfcrawler = bingPdf(['lstm'], pages=3, filetype='pdf')#关键字 页码 文件类型
    pdfcrawler.download_search_data()     #download pdfs from list -> ["svm"]
    #pdfcrawler.convert_pdfs(to_json=True)     #convert all pdfs to txt, json file could be used as DataFrame
    #pdfcrawler.concate_all_txt()  #concate txt files each by search keyword -> to analyze whole txt data
