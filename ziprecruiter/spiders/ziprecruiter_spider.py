import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class ZiprecruiterSpiderSpider(scrapy.Spider):
    name = 'ziprecruiter'
    base_url = "https://www.ziprecruiter.co.uk"
    #start_urls = ['https://www.ziprecruiter.co.uk/jobs/search?q=IT+Director&l=London&lat=&long=&d=10']
    def start_requests(self):
        yield SeleniumRequest(url='https://www.ziprecruiter.co.uk/jobs/search?q=IT+Director&l=London&lat=&long=&d=10',callback=self.parse, wait_time=30, wait_until=EC.visibility_of_element_located((By.XPATH, "//a[contains(@class,'jobList-title')]")))

    def parse(self, response):
        jobs_link = response.xpath("//a[contains(@class,'jobList-title')]/@href").extract()
        next_page = response.xpath("//i[@class='fas fa-chevron-right']")
        for link in jobs_link:
            yield {
                'link': link
            }
        
        if next_page:
            url = next_page.xpath("../@href").extract_first()
            url = self.base_url + url
            yield SeleniumRequest(url=url, callback=self.parse)