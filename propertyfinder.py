import scrapy
from  scrapy.crawler import CrawlerProcess
import json
import scraper_helper as sh
import csv
from scrapy.selector import Selector


class property(scrapy.Spider):
    name = "property_finder"

    url = "https://www.propertyfinder.eg/en/search?c=1&l=2254&ob=mr&page="

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'property.csv',
    }

    headers = sh.get_dict(
        '''
        DOWNLOAD_DELAY: 3,                     
        CONCURRENT_REQUESTS_PER_DOMAIN: 2  ,
        accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
        accept-encoding: gzip, deflate, br
        accept-language: en-US,en;q=0.9
        cache-control: no-cache
        cookie: website_ab_tests=test64%3DvariantA; audience=new-user; _sp_ses.32cc=*; ak_bmsc=D4F7414FB241D856BABC1E29340BC535D59EB366ED5000006F188560C9E02602~plP6tW5PsoK5Hn/BgPakWXOeef3X2fH1CXoZsY0D605WfR0BBp/MXsW3aYQgVBiBIMBSvdVSS51ikaxzQu77MoU/De5OPwL4ZSyfPCu/vJ6MQfCYJaTlitARtwtwf+BnV0pAChku7Ij87nlAeUvCvmDqLpKPug5X2UiCP23dk+01OUKHZ4mRl3KGHmfTWSn/9i0JHiWkFJ5/fyZI7fB4xH90ErIZErh0/V4scBgCDxcxz+RysGnJx9eAGZOPBK7emw; pf-notification=true; AKA_A2=A; _dd_l=1; _dd=9eb38f6d-1439-4a19-ad29-a0a9fb6d21a9; bm_sv=E85EDADE0412838B43B173D4B751B56F~/sU45nfLBvcRT8VqjLDbDkCbvGHMFi6iLjbROZl8B8FJ80nTOAvZ9lDza33HlDirV+Gu1uow/XSOTeiQxDqNTun5ZGjvez6gCTaNcSkoayZWJGgs26exrH7ZWhJgmwr6EjTkpvdkq8ccogf2AOXKyxlwejilWfiZZYJg9PYSi8s=; _sp_id.32cc=02622ca8-1e6a-4ddc-be03-557009a60e8c.1618656646.3.1619342155.1618661392.370e0dec-808f-40d9-ac20-8efde3f7b662
        dnt: 1
        pragma: no-cache
        sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"
        sec-ch-ua-mobile: ?0
        sec-fetch-dest: document
        sec-fetch-mode: navigate
        sec-fetch-site: same-origin
        sec-fetch-user: ?1
        upgrade-insecure-requests: 1
        user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36
     '''
     )
    
    def start_requests(self):
        for page in range(1, 4):
            next_page = self.url + str(page)
            yield scrapy.Request(url = next_page, headers= self.headers, callback = self.parse)
    

    def parse(self, response):
       
        # with open("res.html", "w",  encoding='utf-8') as f:
        #     f.write(res.text)

        # with open('res.html', 'r',  encoding='utf-8') as f:
        #     content = f.read()
        
        # res = Selector(text=content)            
       
        for item in response.css('div[class="card-list__item"]'):
            items = {
                'name':''.join(item.css('h2.card__title-link ::text').extract()).encode('ascii', 'ignore').decode('utf-8'),
                'location': ''.join(item.css('p.card__location').css('span.card__location-text ::text').extract()),
                'area':''.join(item.css('p.card__property-amenity--area ::text').extract()),
                'type':''.join(item.css('p.card__property-amenity--property-type ::text').extract()),
                'link':''.join(item.css('a.card--clickable ::attr(href)').extract()),
                'price':''.join(item.css('span.card__price-value ::text').extract()).strip().replace('\n', '').replace("        ","").replace("     ",""),
                'number_of_bedrooms':''.join(item.css('p.card__property-amenity--bedrooms ::text').extract()),
                'pictures':''.join(item.css('img.card__img ::attr(src)').extract()),
                
            }

            yield items

            print(json.dumps(items, indent=4))

if __name__ == '__main__':
    
    process = CrawlerProcess()
    process.crawl(property)
    process.start()
                
   #property.parse(property, "")