from scrapy.spider import Spider
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.item import Item, Field
import urllib


class Question(Item):
    title = Field()
    date = Field()
    main_image = Field()
    date = Field()
    url = Field()


class ArgSpider(CrawlSpider):


    name = "StackSpider"

    def __init__(self, tag=None, query=None, *args, **kwargs):
        super(ArgSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ["trulioo.com"]
        self.start_urls = ["https://www.trulioo.com/blog"]
        self.rules = [Rule(SgmlLinkExtractor(unique=True,
                                             restrict_css=None),
                           callback='parse',
                           follow=True)]

    def parse(self, response):
        """

        @url url to crawl"
        @scrapes main info about each blog

        """
        sel = Selector(response)
        results = []
        item = Question()
        item["title"] = sel.css('[class="entry-title qodef-post-title"]').xpath('normalize-space(text())').extract()
        item["date"] = sel.css('[class="qodef-post-info qodef-section-top"] [class="qodef-date-value"]').xpath(
            'normalize-space(text())').extract()
        item["main_image"] = sel.css('div.qodef-post-content > div.qodef-post-image > img').xpath('@src').extract()
        item["url"] = response.url
        print item
        yield item

