'''
cookies=[
    {
    'name':'csrftoken',
    'value':'znfnB4o0lP7ZwnJomFEZdvNrz2xCwk4L',
    'domain':'www.heibanke.com',
    'path':'/',
    }]
'''
#命令：scrapy crawl fourth
import scrapy
import re
import threading
import requests
import time

class mission_three(scrapy.Spider):
    name='fourth'
    t=0
    def start_requests(self):
        urls=[
            'http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex03/',
        ]
        yield scrapy.Request(url=urls[0],
                meta={'cookiejar':1},
                callback=self.login
            )
    #登陆黑板客
    def login(self,response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'username':'lslsls',
                'password':'123456'
            },
            callback=self.after_login,
            clickdata={
                'nr':2
            },
            meta={'cookiejar':response.meta['cookiejar']},
            dont_filter=True
        )
    #开始闯第四关
    def after_login(self,response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'username':'6',
                'password':'%d'%self.t
            },
            callback=self.find,
            meta={'cookiejar':response.meta['cookiejar']},
            dont_filter=True
        )
    #解析密码
    def parse_password(self,response):
        pos_pattern=r'_pos.>(.*)</td>'
        val_pattern=r'_val.>(.*)</td>'
        pos_list=re.findall(pos_pattern,response.text)
        val_list=re.findall(val_pattern,response.text)
        #打包字典，填充数值
        for pos,val in zip(pos_list,val_list):
            if pos not in self.password_dict.keys():
                self.password_dict[pos]=val
                self.count=self.count+1 #位数加1
                print(self.count)
        if(self.count==100):
            print(self.count)
            pass



                                                            
    #解析pw_list网址
    def find_password(self,response):
        self.count=0    #密码位数，100位
        self.password_list=['' for n in range(101)]
        self.pass_url=response.url
        self.password_dict={}   #保存键值对的字典
        while self.count<100:
            time.sleep(2)
            yield scrapy.Request(url=response.url,
                    meta={'cookiejar' : response.meta['cookiejar']},
                    dont_filter=True,
                    callback=self.parse_password
                )
        for pos in self.password_dict.keys():
            self.password_list[int(pos)]=self.password_dict[pos]
        password=int(''.join(self.password_list))
        print('密码为：%s'%password)
        '''threads=[None]*5
        for i in range(0,5):
            threads[i]=threading.Thread(target=self.work)
            threads[i].start()

        for i in range(0,5):
            threads[i].join()
            '''



    #验证密码是否正确，不正确则跳到find_password
    def find(self,response):
        try:
            flag = response.xpath('/html/body/div/div/div[2]/h3/text()').extract()[0]
        except:
            flag = 'None'
        if re.search(r'密码错误', flag) is not None:
            yield scrapy.Request(url=response.urljoin(response.xpath('/html/body/div/div/div[2]/p[2]/a/@href').extract()[0]),
                    meta={'cookiejar' : response.meta['cookiejar']},
                    dont_filter=True,
                    callback=self.find_password
                )
        else:
            with open('x.xml','wb') as fb:
                fb.write(response.body)

