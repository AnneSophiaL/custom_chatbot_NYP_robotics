from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import scrapy
from scrapy.crawler import CrawlerProcess


opts = Options()
opts.add_argument("--headless")

driver = webdriver.Firefox(options=opts)

driver.get("https://fr.vestiairecollective.com/sacs-femme/#gender=Femme%231")

driver.implicitly_wait(4)
driver.find_element(By.XPATH, '//*[@id="popin_tc_privacy_button_2"]').click()

bags_links = []
for n in range (1,106):
    driver.get("https://fr.vestiairecollective.com/sacs-femme/p-"+str(n)+"/#gender=Femme%231")
    
    elements = driver.find_elements(By.CSS_SELECTOR, "a.product-card_productCard__image__yiwdm")
    for elt in elements:
        try:
            link = elt.get_attribute('href')
            bags_links.append(link)
        except StaleElementReferenceException:
            # Si la référence de l'élément est périmée, relocalisez l'élément et récupérez à nouveau l'attribut href.
            elt = driver.find_element(By.CSS_SELECTOR, "a.product-card_productCard__image__yiwdm")
            link = elt.get_attribute('href')
            bags_links.append(link)
bags_links = [l for l in bags_links if l is not None]


class VestiaireCollective(scrapy.Spider):
    name = 'vestiairecollective'
    start_urls = bags_links
    #download_delay=0.5

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        d = dict()
        
        keys = response.css(".product-description-list_descriptionList__property__21dco").css("::text").extract()
        keys = [x for x in keys if x != ':']
        informations = response.css(".product-description-list_descriptionList__value__J3Z9l").css("::text").extract()
       
        informations = [y for y in informations if y != ' ' and y != 'cm' ]
        d["image"] = response.css("div.vc-images_imageContainer__Sau2S").css("::attr(src)").extract()[1]
        d["prix"] = response.css('.product-price_productPrice__Uq0dh').css("::text").extract_first()
        category = response.css(".breadcrumbs_mainBreadcrumb__item__hqQjx").css("::text").extract()
        if "Sacs à main" in category:
            d["categorie"] = category[4]
        else :
            d["categorie"] = category[3]
        for i in range(len(keys)) :
            
            if "Designer" in keys[i] :
                d["marque"] = keys[i]+informations[i]
           
            if "Modèle" in keys[i] :
                d["modele"] = keys[i]+informations[i]
            
            if "État" in keys[i] :
                d["etat"] = keys[i]+informations[i]
            
            if "Matière" in keys[i] :
                d["matiere"] = keys[i]+informations[i]                
            
            if "Couleur" in keys[i] :
                d["couleur"] = keys[i]+informations[i]  
            
            if "Localisation" in keys[i] :
                d["localisation"] = keys[i]+informations[i]  
            
            if "Hauteur" in keys[i] :
                
                d["hauteur"] = keys[i]+informations[i]+" cm"  
            
            if "Largeur" in keys[i] :
                 
                d["largeur"] = keys[i]+informations[i]+" cm" 
            
            if "Profondeur" in keys[i] :
                
                d["profondeur"] = keys[i]+informations[i]+" cm"                                                                  

            

        yield d


process = CrawlerProcess(settings={
    "FEEDS": {
        "data_vc.json": {"format": "json"},
    },
})

process.crawl(VestiaireCollective)
process.start()
