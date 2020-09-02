# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc']
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths= ["//h3[@class = 'lister-item-header']/a"]), callback='parse_item', follow=True ),
        Rule(LinkExtractor(restrict_xpaths=["(//a[@class = 'lister-page-next next-page'])[2]"]))
    )

    def parse_item(self, response):
        try : 
            yield {
                'Title' : response.xpath("//div[@class='title_wrapper']/h1/text()").get(),
                'Year': response.xpath("//div[@class='title_wrapper']/h1/span/a/text()").get(),
                'Director' : response.xpath("//div[@class = 'credit_summary_item']/a/text()").get(),
                'Stars' : response.xpath("//div[@class = 'credit_summary_item'][3]/span/preceding-sibling::a/text()").getall(),
                'Duration': response.xpath('normalize-space(//div[@class="subtext"]/time/text())').get(),
                'Trailer_Duration' : (response.xpath("//div[@style = 'float: left;']/text()").get()).replace(' ', ''), 
                'Genre' : response.xpath('//div[@class="subtext"]/a/text()').get(),
                'Rating' : response.xpath('//div[@class="ratingValue"]/strong/span/text()').get() + ' / 10',
                'Movie_url':response.url
            }
        except: 
            yield {
            'Title' : response.xpath("//div[@class='title_wrapper']/h1/text()").get(),
            'Year': response.xpath("//div[@class='title_wrapper']/h1/span/a/text()").get(),
            'Director' : response.xpath("//div[@class = 'credit_summary_item']/a/text()").get(),
            'Stars' : response.xpath("//div[@class = 'credit_summary_item'][3]/span/preceding-sibling::a/text()").getall(),
            'Duration': response.xpath('normalize-space(//div[@class="subtext"]/time/text())').get(),
            'Trailer_Duration' : None, 
            'Genre' : response.xpath('//div[@class="subtext"]/a/text()').get(),
            'Rating' : response.xpath('//div[@class="ratingValue"]/strong/span/text()').get() + ' / 10',
            'Movie_url':response.url
            }


# Since 4 of the movies didn't have Trailer Time they were Excluded and in Best_Movies2.json we have 46 movies !