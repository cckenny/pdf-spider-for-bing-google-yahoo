## filetype决定文件格式，理论上能直接搜到的文件格式都能爬
项目需要，小试牛刀  
1. bing好像检测更严格？需要弄代理。   *bing is even more strict?*  
2. google页数跟实际相比很少，可能因为在被封的边缘疯狂试探  *can get very less files(100?) from google*  
3. bing爬下来的重复率有点高，爬了8k+只有2k3的有效文件  
4. lxml解析好像不太准，**放弃lxml，直接正则匹配**  
5. 增加yahoo  
6. google很容易ban诶，暂时先不用google了，以后增加防ban机制  
