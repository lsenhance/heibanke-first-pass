import scrapy
import re
import pytesseract
from PIL import Image
import time
import PIL
import requests

#scrapy crawl five
class mission_four(scrapy.Spider):
    name='five'
    t=0
    ID_code=''
    count1=0
    count2=0
    def start_requests(self): 
        urls=[
            'http://www.heibanke.com/lesson/crawler_ex04/',
        ]
        yield scrapy.Request(
            url=urls[0],
            callback=self.login
        )


    def login(self,response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'username':'lslsls',
                'password':'123456'
            },
            dont_filter=True,
            callback=self.after_login
        )
                          

    def after_login(self,response):
        self.count2=self.count2+1
        with open('x.xml','wb') as fb:
            fb.write(response.body)
        img_url=response.xpath('/html/body/div/div/div[2]/form/div[3]/img/@src').extract()[0]
        img_fullurl='http://www.heibanke.com'+img_url
        print(img_fullurl)
        img_src=requests.get(img_fullurl)
        with open('1.jpg','wb') as fb:
            fb.write(img_src.content)
        self.ID_code=pytesseract.image_to_string(Image.open(r"F:\file\VS code\heibanke-scrapy-mission\tutorial\1.jpg"),lang='eng')
        print(self.ID_code)

        if len(self.ID_code)==4:
            print(self.count1)
            print(self.count2)
            self.ID_code.upper()
            print(self.ID_code)
            yield scrapy.FormRequest.from_response(
                response,
                formdata={
                    'username':'6',
                    'password':'%d'%self.t,
                    'captcha_1':'%s'%self.ID_code
                },
                callback=self.test,
                dont_filter=True
            )
        else:
            yield scrapy.Request(
                url="http://www.heibanke.com/lesson/crawler_ex04/",
                callback=self.after_login,
                dont_filter=True
            )

    def test(self,response):
        print('现在的密码为%d'%self.t)
        print(self.ID_code)
        code_wrong=re.compile('密码错误')
        ID_wrong=re.compile('验证码输入错误')
        state=response.xpath('/html/body/div/div/div[2]/h3/text()').extract()[0]
        if re.search(code_wrong,state) is not None:
            self.t=self.t+1
            yield scrapy.Request(
                url="http://www.heibanke.com/lesson/crawler_ex04/",
                callback=self.after_login,
                dont_filter=True
            )
        elif re.search(ID_wrong,state) is not None:
            yield scrapy.Request(
                url="http://www.heibanke.com/lesson/crawler_ex04/",
                callback=self.after_login,
                dont_filter=True
            )
        
        print(state)
        with open('test.xml','wb') as test:
            test.write(response.body)
#scrapy crawl five