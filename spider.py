from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tokenRemover import removeToken
from extractStatsFromTable import getStatsFromTable, createStatEntry
import json
import sys

class bballSpiderSpider(CrawlSpider):
    visitedUrls = set()
    name = "bbalSpider"
    allowed_domains = ['proballers.com']
    custom_settings = { "FEED_EXPORT_ENCODING": 'utf-8' ,
                       "USER_AGENT": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    start_urls = ['https://www.proballers.com/basketball/league/50/greece-heba-a1/players/' + str(year) for year in range(2000,2024)]  
    
    rules =  (Rule(LinkExtractor(allow=(r"/player/",)), callback="parse"),)
    def parse(self, response):
        URL = response.request.url
        if URL in self.visitedUrls: 
            return
        self.visitedUrls.add(URL)
        dict = {}
        player_name = response.css("li.breadcrumb-item.active>span::text").getall()
        position = response.css("div.identity__description li:last-child::text").getall()
        Ethnicity = response.css("div.identity__description li:nth-child(2)::text").getall()
        photo = response.css("div.identity__picture img::attr(src)").getall() 
        tbody = response.css("#player-stats-regular > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(2)")
        rows = getStatsFromTable(tbody)
        playerEntry = {"Name" : player_name[0],
                       "Position" : position[0].strip(),
                       "Ethnicity" : Ethnicity[0],
                       "Photo" : photo[0],
                       "Stats" : createStatEntry(rows)}  
        
        yield playerEntry


