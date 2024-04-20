import requests
import random
import re
import urllib


import chromedriver_autoinstaller

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


user_agents = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9',
 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17',
 'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F69 Safari/600.1.4',
 'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
 'Mozilla/5.0 (X11; CrOS x86_64 7077.134.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.156 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/7.1.7 Safari/537.85.16',
 'Mozilla/5.0 (Windows NT 6.0; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36']


class AmazonScraper:

    def __init__(self, url):
        
        service = webdriver.chrome.service.Service()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--headless=new")
        options.add_argument(f"user-agent={random.choice(user_agents)}")
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=service, options=options)

        self.search_url = url
        self.driver.get(self.search_url)        
        
    def isNullElement(self, element):
        img = element.find_elements(By.XPATH, ".//img[@src]")
        if element.text.strip() or img:
            return False
        return True
    
    def find_element(self, element, locator, expression, list=True):
        result = element.find_elements(locator, expression)
        if list:
            return result
        
        return result[0] if result else None

    def getProductTitle(self):
        return self.driver.find_element(By.ID, 'productTitle').text
    
    def getLeftImage(self):
        return [img.get_attribute('src') for img in self.driver.find_elements(By.XPATH, "//div[@id='imageBlock']//div[@class='imgTagWrapper']//img")]

    def getProductNameAndIDFromURL(self):
        product_path = urllib.parse.urlparse(self.driver.current_url).path.strip('/').split('/')

        product_name = product_path[0].replace("-", " ")
        product_id = product_path[2]
        
        return product_name, product_id

    def parseCenterDiv(self):
        #parse centerDiv

        product_detail = {}
    #     required_div = ["featurebullets_feature_div", "bylineInfo_feature_div", "title_feature_div", "productOverview_feature_div"]
        
        centerDiv = self.driver.find_elements(By.XPATH, "//div[@id='ppd']")[0].find_element(By.XPATH, ".//div[@id='centerCol']")

        #get product title
        product_detail['product_title'] = centerDiv.find_element(By.ID, 'productTitle').text

        #get product brand
        product_detail['product_brand'] = re.sub("^Visit the|^Brand:|store$", "", centerDiv.find_element(By.ID, 'bylineInfo').text, flags=re.IGNORECASE).strip()
        product_detail['product_brand_url'] = centerDiv.find_element(By.ID, 'bylineInfo').get_attribute('href')

        #get customer reviews
        customer_reviews = centerDiv.find_elements(By.XPATH, "//div[@id='averageCustomerReviews']")
        if customer_reviews:
            product_detail['customer_reviews'] = customer_reviews[0].text.split("\n")[0]

        #get prdouct overview
#         product_detail['product_overview'] = {}
        
        product_overview_feature_div = centerDiv.find_elements(By.XPATH, "//div[@id='productOverview_feature_div']")
        if product_overview_feature_div:        
            soup = BeautifulSoup(product_overview_feature_div[0].get_attribute('innerHTML'), 'html.parser')
            for i in soup.findAll('tr'):
                td = i.findChildren('td')

                #below if elif are just for glance icons
                if td[0].find('table'):
                    td = td[0].findAll('td')[-1].findAll('span')
                elif td[0].find('img'):
                    td = td[1].findAll('span')

                product_detail[td[0].text.strip()] = td[1].text.strip()
                
        #parse about section
        #replace non ascii characters and continous spaces
        product_detail['product_about'] = ""
        product_about = centerDiv.find_elements(By.XPATH, ".//div[@id='featurebullets_feature_div']//ul")
        
        if product_about:
            product_detail['product_about'] = re.sub("\s+", " ", re.sub(r'[^\x00-\x7F]+', "", product_about[0].text))


        return product_detail

    def parseBottomDivs(self):

        productDescription = self.driver.find_elements(By.XPATH, "//div[@id='productDescription']")
        if productDescription:
            productDescription = productDescription[0].text.strip()
        product_config = {}
        misc = {}
        long_description = ""
        brand_story = ""
        detailBullets = self.driver.find_elements(By.XPATH, "//div[@id='detailBullets_feature_div' and not(@data-feature-name)]")
        if detailBullets:

            for li in detailBullets[0].find_elements(By.TAG_NAME, "li"):
                spans = li.find_elements(By.XPATH, ".//span/span")
                if spans:
                    product_config[spans[0].text.replace(":","").strip()] = spans[1].text.strip()
        else:
            productDetails = self.driver.find_elements(By.XPATH, "//div[@id='productDetailsNonPets_feature_div']")


        product_information = ''
        productDetails_feature_div = self.driver.find_elements(By.XPATH, "//div[@id='productDetails_feature_div']")
        if productDetails_feature_div:
            product_information = productDetails_feature_div[0].text

        aplus_feature_div = self.driver.find_elements(By.XPATH, "//div[@id='aplus_feature_div' and div and normalize-space()]")

        images = []
        if aplus_feature_div:

            long_description = aplus_feature_div[0].find_element(By.XPATH, ".//div[@id='aplus']/div").text
            images = [i.get_attribute("src") for i in aplus_feature_div[0].find_elements(By.TAG_NAME, "img")]

        aplus_BS_feature_div = self.driver.find_elements(By.XPATH, "//div[@id='aplusBrandStory_feature_div' and div and normalize-space()]")

        if aplus_BS_feature_div:
            brand_story = aplus_BS_feature_div[0].find_element(By.XPATH, ".//div[@id='aplus']/div").text

            images.extend([i.get_attribute("src") for i in aplus_BS_feature_div[0].find_elements(By.TAG_NAME, "img")])


        #find all the divs where id's contains btfContent and has div which has some text or img element
        btf_contents = self.driver.find_elements(By.XPATH, "//div[contains(@id, 'btfContent') and div and normalize-space()]") 

        btf_description = ""
        for btf_content in btf_contents:
                btf_description += " " + btf_content.text.strip()
                images.extend([i.get_attribute("src") for i in btf_content.find_elements(By.TAG_NAME, "img")])


        misc = btf_description
        product_details = {
            'product_short_description': re.sub(r'[^\x00-\x7F]+', '', productDescription) if productDescription else '', 
            'product_long_description': re.sub(r'[^\x00-\x7F]+', '',long_description),
            'brand_story': re.sub(r'[^\x00-\x7F]+', '', brand_story),
            'misc': misc,
            'product_information': product_information
        }        

        product_details.update(product_config)
        return product_details, images

    def quit(self):
        self.driver.quit()