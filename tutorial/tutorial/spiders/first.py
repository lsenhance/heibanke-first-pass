import scrapy
import re

class AuthorSpider(scrapy.Spider):
    name = 'first'
    start_urls=(
        'http://www.heibanke.com/lesson/crawler_ex00/',)

    def parse(self,response):
        num=response.xpath('/html/body/div/div/div[2]/h3/text()').extract()[0]
        print(type(num))
        print(num)
        num=re.sub("\D","",num)
        print(type(num))
        print(num)
        if num is not None:
            next_page='http://www.heibanke.com/lesson/crawler_ex00/'+ num
            if next_page is not None:
                yield scrapy.Request(next_page, callback=self.parse)
        else:
            print('good work')
    