#命令：scrapy crawl first
#re说明：https://docs.python.org/3/library/re.html
import scrapy
import re

class AuthorSpider(scrapy.Spider):
    name = 'first'
    start_urls=(
        'http://www.heibanke.com/lesson/crawler_ex00/',)

    def parse(self,response):
        num=response.xpath('/html/body/div/div/div[2]/h3/text()').extract()[0]
        print(num)
        #使用正则表达式的sub方法提取数字,返回str
        num=re.sub(r'\D',"",num)    

        #使用正则表达式的findall方法提取数字  IndexError: list index out of range 
        #num=re.findall(r"\d+",num)
        #search方法，返回match object,match是从头开始匹配
        #num=re.search(r"\d+",num)

        if (type(num)==list):
            if len(num)==1 and num[0] is not None:
                num=num[0]
            else:
                num=None
        elif(type(num)==str):
            pass
        else:
            if num!=None:
                num=num[0]
        

        if num is not None:
            next_page='http://www.heibanke.com/lesson/crawler_ex00/'+ num
            yield scrapy.Request(next_page, callback=self.parse)
    