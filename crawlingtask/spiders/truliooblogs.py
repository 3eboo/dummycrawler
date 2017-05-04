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
    """

    Scrapes first 15 stackoverflow.com questions containing "query" within a given "tag" and
    displays links, number of votes etc in the terminal.

    Usage:

      ~: scrapy crawl StackSpider -a tag=[your tag] -a query=[your query]

    For example

       ~: scrapy crawl StackSpider -a tag=python -a query="crawling a website"


    """

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

        @url http://stackoverflow.com/search?q=%5Bpython%5Dfiltering"
        @returns items 15
        @returns requests 0 1
        @scrapes votes answers date link

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

