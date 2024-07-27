from spider import bballSpiderSpider
from scrapy.crawler import CrawlerProcess
import os

def deletePlayerBase():
        try: os.remove("playerBase1.json")
        except: pass

process = CrawlerProcess(
    settings={
        "FEEDS": {
            "playerBase1.json": {"format": "json"},
        },
    }
)


deletePlayerBase()
process.crawl(bballSpiderSpider)
process.start()
