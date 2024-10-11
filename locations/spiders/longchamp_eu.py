import scrapy

from locations.dict_parser import DictParser
from locations.geo import point_locations


class LongchampEUSpider(scrapy.Spider):
    name = "longchamp_eu"
    item_attributes = {"brand": "Longchamp", "brand_wikidata": "Q1869471"}
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def start_requests(self):
        template = "https://www.longchamp.com/on/demandware.store/Sites-Longchamp-EU-Site/de_DE/Stores-FindStores?showMap=true&radius=300&lat={}&lng={}"
        for lat, lon in point_locations("eu_centroids_120km_radius_country.csv"):
            yield scrapy.Request(url=template.format(lat, lon))

    def parse(self, response):
        for store in response.json().get("stores"):
            item = DictParser.parse(store)

            yield item
