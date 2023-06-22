from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import scrapy
from scrapy.crawler import CrawlerProcess
import numpy as np

opts = Options()
opts.add_argument("--headless")

driver = webdriver.Firefox(options=opts) 

driver.implicitly_wait(4)

bags_links = []
for n in range (1,70):
    driver.get("https://www.mytheresa.com/fr-fr/bags.html?p="+str(n))
    elements = driver.find_elements(By.CSS_SELECTOR, 'a[class="product-image"]')
    for elt in elements :
        link = elt.get_attribute('href')
        bags_links.append(link)






class Mytheresa(scrapy.Spider):
    name = 'mytheresa'
    start_urls = bags_links
    
    def start_requests(self):
        
        for url in self.start_urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        d = dict()
        d["image"] = response.css('img[id="image-0"]').css("::attr(src)").extract_first()
        d["prix"] = response.css("span.price").css("::text").extract_first()
        category = response.css('.breadcrumbs').css("::text").extract()
        category = [x for x in category if "\n" not in x]
        if len(category) < 5 :
            d["categorie"] = np.nan
        else :
            d["categorie"] = category[3]
        d["marque"] = response.css("a.text-000000").css("::text").extract_first()
        d["modele"] = response.css("span.pb2  ").css("::text").extract_first()
        informations = response.css('li[class="pa1"]').css("::text").extract()
        for info in informations :
            if "matériau" in info :
                d["matiere"] = info
            if "couleur" in info :
                d["couleur"] = info
            if "Fabriqué" in info :
                d["fabrication"] = info
            if "Hauteur" in info :
                d["hauteur"] = info
            if "Largeur" in info :
                d["largeur"] = info
            if "Profondeur" in info :
                d["profondeur"] = info
        yield d


process = CrawlerProcess(settings={
    "FEEDS": {
        "data_mt.json": {"format": "json"},
    },
})

process.crawl(Mytheresa)
process.start()
