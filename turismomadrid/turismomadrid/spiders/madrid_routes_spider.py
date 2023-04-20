import scrapy
import re
from ..db.database import Category, Route, Itinerary, Session, Step


class MadridRoutesSpider(scrapy.Spider):
    name = "madrid_routes_spider"
    start_urls = [
        'https://turismomadrid.es/es/rutas.html',
    ]

    def parse(self, response):
        categories = response.xpath('//*[@id="component"]/div[2]/a/@href').getall()
        for category in categories:
            yield response.follow(category, self.parse_category)

    def parse_category(self, response):
        name = response.xpath('//*[@id="component"]/div/div/div[1]/div[2]/div[2]/h1/text()').get()
        image = response.xpath('//*[@id="component"]/div/div/div[1]/div[1]/@style').get().split("url('")[1].split("');")[0]
        description = response.xpath('//*[@id="component"]/div/div/div[2]/div[2]/p/text()').get()
        if not description.endswith('.'):
            description = description + '.'
        with Session() as session:
            db_category = Category(
                    name=name,
                    description=description,
                    image=image
                )
            session.add(db_category)
            session.commit()

            routes = response.xpath('//*[@id="component"]/div/div//a[contains(@href, "etapa")]/@href').getall()
            for route in routes:
                url = route
                yield response.follow(url, self.parse_route, meta={'category_id': str(db_category)})

    def parse_route(self, response):
        name = response.xpath('//*[@id="component"]/div/div[2]/div[2]/h1/text()').get()
        description = ''.join(response.xpath('//*[@id="component"]/div/div[4]/div[1]/p//text()').getall())
        image = response.xpath('//*[@id="component"]/div/div[3]/@style').get().split("url('")[1].split("');")[0]
        if len(description) > 0:
            pattern = re.compile(r'<[^>]+>')
            clean_description = pattern.sub('', description)
        else:
            clean_description = "None"

        if not clean_description.endswith('.'):
            clean_description = clean_description + '.'

        with Session() as session:
            db_route = Route(
                category_id=response.meta['category_id'],
                name=name,
                description=clean_description,
                image=image
            )
            session.add(db_route)
            session.commit()

            itineraries = response.xpath('//*[@id="component"]/div/a')
            for itinerary in itineraries:
                yield response.follow(itinerary.xpath('@href').get(), self.parse_itinerary, meta={'route_id': str(db_route)})

    def parse_itinerary(self, response):
        itinerary_title = response.xpath('//*[@id="component"]/div/div[2]/div[2]/div[1]/h1/text()').get()
        itinerary_description = ''.join(response.xpath('//*[@id="component"]/div/div[4]/div[1]/p//text()').getall())
        if itinerary_description == '':
            itinerary_description = "None"
        if not itinerary_description.endswith('.'):
            itinerary_description = itinerary_description + '.'

        itinerary_image = response.xpath('//*[@id="component"]/div/div[3]/@style').get().split("url('")[1].split("');")[0]

        with Session() as session:
            db_itinerary = Itinerary(
                route_id=response.meta['route_id'],
                name=itinerary_title,
                description=itinerary_description,
                image=itinerary_image
            )
            session.add(db_itinerary)
            session.commit()

            steps = response.xpath('//*[@id="component"]/div/div[6]/div')
            for step in steps:
                image = step.xpath('div[2]/@style').get()
                if image is not None:
                    image = image.split("url('")[1].split("');")[0]

                name = step.xpath('div/h3/div[2]/text()').get()
                if name is not None:
                    name = re.sub(r'^\d+\.*', '', name)

                description = ''.join(step.xpath('div/div//text()').getall())
                if description == '':
                    description = "None"
                if not description.endswith('.'):
                    description = description + '.'
                description = description.strip()

                db_step = Step(
                    itinerary_id=str(db_itinerary),
                    name=name,
                    description=description,
                    image=image
                )
                session.add(db_step)
                session.commit()
