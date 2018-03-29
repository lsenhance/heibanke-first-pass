#命令：scrapy crawl second
import scrapy
import re


class second_mission(scrapy.Spider):
    name="second"
    start_urls=('http://www.heibanke.com/lesson/crawler_ex01/',)
    t=0

    def parse(self,response):
        print(self.t)
        #state=response.xpath('/html/body/div/div/div[2]/h3').extract()[0]
        #print(state)
        return scrapy.FormRequest.from_response(
            response,
            url='http://www.heibanke.com/lesson/crawler_ex01/',
            formdata={
                'username':'lsenhance',
                'password':'%d'%self.t
            },
            clickdata={
                'nr':0
            },
            callback=self.test,
            dont_filter=True,
        )
    
    def test(self,response):
        #if "密码错误" in response.body:
            #print('密码错误')

        login_sta=response.xpath('/html/body/div/div/div[2]/h3').extract()[0]
        if re.search(r"密码错误",login_sta) is not None:
            login_sta=False
            print("密码错误")
            self.t=self.t+1
            yield scrapy.Request('http://www.heibanke.com/lesson/crawler_ex01/', callback=self.parse,dont_filter=True,)
        else:
            login_sta=True
            print("密码为%d"%self.t)
        #print(login_sta)