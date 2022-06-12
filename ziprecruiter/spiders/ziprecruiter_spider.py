import scrapy


class ZiprecruiterSpiderSpider(scrapy.Spider):
    name = 'ziprecruiter'

    start_urls = ['https://www.ziprecruiter.co.uk/jobs/search?q=IT+Director&l=London&lat=&long=&d=10']

    def parse(self, response):
        jobs_link = response.xpath("//a[contains(@class,'jobList-title')]/@href").extract()
        next_page = response.xpath("//i[@class='fas fa-chevron-right']")
        for link in jobs_link:
            yield {
                'link': link
            }
        
        if next_page:
            url = next_page.xpath("../@href").extract_first()
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.parse)