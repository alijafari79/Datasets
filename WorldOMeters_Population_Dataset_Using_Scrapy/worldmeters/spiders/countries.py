# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import open_in_browser

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath("//td/a")
        
        for country in countries :
            name = country.xpath(".//text()").get() #Name of the country ;
            link = country.xpath(".//@href").get()
            
            # abs_url=  f'https://www.worldometers.info{link}'   # ---> Relative url
            # abs_url = response.urljoin(link)          #  ---- > Relative url

            yield response.follow(url = link , callback = self.parse_country , meta = {'CountryName':name})
        # yield response.follow(url = 'https://www.worldometers.info/world-population/china-population/')

    def parse_country(self , response): 

        rows = response.xpath("(//table[@class = 'table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        name = response.request.meta['CountryName']

        for row in rows : 
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()

            yield{
                'Country Name' : name,
                'year':year ,
                'population':population
            }