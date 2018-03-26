import scrapy
import re

class AuthorSpider(scrapy.Spider):
    name = 'first'
    start_urls=(
        'http://www.heibanke.com/lesson/crawler_ex00/',)

    def parse(self,response):
        num=response.xpath('/html/body/div/div/div[2]/h3/text()').extract()[0]
        print(num)
        num=re.sub("\D","",num)
        next_page='http://www.heibanke.com/lesson/crawler_ex00/'+ num
        yield scrapy.Request(next_page, callback=self.parse)
    