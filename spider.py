from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy

class bballSpiderSpider(CrawlSpider):
    name = "bbalSpider"
    allowed_domains = ['proballers.com']
    custom_settings = { "FEED_EXPORT_ENCODING": 'utf-8' ,
                       "USER_AGENT": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    start_urls = ['https://www.proballers.com/basketball/league/50/greece-heba-a1/players']
    
    rules =  (Rule(LinkExtractor(allow=(r"/player/",)), callback="parse"),)

    def parse(self, response):
        player_names = response.css("li.breadcrumb-item.active>span::text").getall()
        previous_teams = response.css("section.banner__table--competitions a.list-team-entry::attr(title)").getall()
        pts = response.css("div.identity__stats li:first-child span.identity__stats__stat::text").getall()
        reb = response.css("div.identity__stats li:nth-child(2) span.identity__stats__stat::text").getall()
        ast = response.css("div.identity__stats li:nth-child(3) span.identity__stats__stat::text").getall()
        stl = response.css("div.identity__stats li:nth-child(4) span.identity__stats__stat::text").getall()
        blk = response.css("div.identity__stats li:last-child span.identity__stats__stat::text").getall()
        position = response.css("div.identity__description li:last-child::text").getall()
        photo = response.css("div.identity__picture img::attr(src)").getall()
        for player_name in player_names:
            yield {"Player Name": player_name, 
                   "Position" : position,
                   "Previous teams" : previous_teams,
                   "Points" : pts,
                   "Rebounds" : reb,
                   "Assists" : ast,
                   "Steals" : stl,
                   "Blocks" : blk,
                   "Photo URL" : photo
                   }
                   
            
process = CrawlerProcess(
    settings={
        "FEEDS": {
            "players0.json": {"format": "json"},
        },
    }
)

process.crawl(bballSpiderSpider)
process.start()

