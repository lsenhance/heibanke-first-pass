#命令：scrapy crawl third
import scrapy
import re

class third_mission(scrapy.Spider):
    name='third'
    t=0
    def start_requests(self):
        urls=[
            'http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex02/',
        ]
        yield scrapy.Request(url=urls[0],callback=self.parse,
        meta={'cookiejar':1},)

    login_info={
        'username':'lslsls',
        'password':'123456'
    }

    def parse(self,response):
        return scrapy.FormRequest.from_response(
            response,
            formdata=self.login_info,
            callback=self.after_login,
            clickdata={
                'nr':2
            },
            meta={'cookiejar':response.meta['cookiejar']},
            dont_filter=True
        )

    def after_login(self,response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'username':'6',
                'password':'%d' %self.t
            },
            dont_filter=True,
            callback=self.test,
            meta={'cookiejar':response.meta['cookiejar']},
        )

    def test(self,response):
        flag=response.xpath('/html/body/div/div/div[2]/h3/text()').extract()[0]
        print(flag)
        if re.search(r'密码错误',flag) is not None:
            print("密码不为%d"%self.t)
            self.t=self.t+1
            yield scrapy.Request('http://www.heibanke.com/lesson/crawler_ex02/',callback=self.after_login,dont_filter=True,
            meta={'cookiejar':response.meta['cookiejar']},)
        else:
            print("密码为:%d"%self.t)
