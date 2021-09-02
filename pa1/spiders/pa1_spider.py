from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import requests
import hashlib
from bs4 import BeautifulSoup



class PA1Spider(CrawlSpider):
    name = "pa1"   
    allowed_domains = ['www.kennesaw.edu']
    start_urls = ['http://www.kennesaw.edu',
                  'http://ccse.kennesaw.edu',
                  'http://engineering.kennesaw.edu'       
        ]
    
    rules = [Rule(LinkExtractor(allow='/'),
                      callback='parse_items', follow=True)]
        
    def parse_items(self, response):
        page = requests.get('http://www.kennesaw.edu')
        soup = BeautifulSoup(page.content,'html.parser')
        current_url = response.request.url
      
        
        entry = dict()
        entry["pageid"] = hashlib.md5((current_url).encode()).hexdigest()
        entry["url"] = current_url
        entry["title"] = response.css('title::text').get().strip().replace("\n","")
        entry["body"] = response.xpath('//body//p//text()').extract()
        #entry["body"] = soup.get_text("|", strip=True)
        entry["emails"] =  response.xpath('//a[starts-with(@href,"mailto:")]/text()').getall()

        yield entry