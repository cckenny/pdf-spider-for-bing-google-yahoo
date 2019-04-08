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
from urllib.parse import unquote

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
        formatPdf = url[-4:]
        if formatPdf != '.pdf':
            return False
        return True


    def get_link(self, search_keyword, filetype, pages, show_links=False):
        linklist = []
        titlelist = []
        print("search keyword : ", search_keyword)
        print("expected time(getting links) : ", pages * 4, "seconds~", pages * 5, "seconds")
        print("----getting links----")
        for page in range(0, pages * 10 , 10):
            while True:
                params = {}
                word = search_keyword + ' filetype:' + filetype
                print(word)
                word = word.encode(encoding='utf-8', errors='strict')
                #print(word)
                params['p'] = word
                params['fr'] = 'sfp'
                params['fr2'] = 'sb-top-zh.search'
                params['b'] = str(1 + page)
                params['pz'] = '10'
                params['bct'] =  '0'
                params['xargs'] = '0'

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit /537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}

                html = requests.get("https://hk.search.yahoo.com/search;", params=params, headers=headers)
                print(html.status_code)
                if html.status_code != 200:
                    continue
                break        
            soup = BeautifulSoup(html.text, 'lxml')
            # soup = BeautifulSoup(htmlpage.text, 'lxml')

            for result_table in soup.findAll("h3"):
                dlurl = unquote(str(re.findall(r"RU=(.+?)/RK=", str(result_table)))[2:-2])
                if dlurl != None:
                    if self.is_downloadable(dlurl):
                        if show_links == True:
                            print(dlurl)
                        linklist.append(dlurl)

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
    pdfcrawler = bingPdf(['biology'], pages=30, filetype='pdf')#关键字 页码 文件类型
    pdfcrawler.download_search_data()   
