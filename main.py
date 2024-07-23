from spider import bballSpiderSpider
from scrapy.crawler import CrawlerProcess
import os

def deletePlayerBase():
        try: os.remove("playerBase.json")
        except: pass

process = CrawlerProcess(
    settings={
        "FEEDS": {
            "playerBase.json": {"format": "json"},
        },
    }
)

deletePlayerBase()
process.crawl(bballSpiderSpider)
process.start()
