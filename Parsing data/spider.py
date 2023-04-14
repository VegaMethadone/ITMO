import scrapy

class BlogSpider(scrapy.Spider):
  name = 'habrspider'
  # start_urls = [habr_link]
  start_urls = (f"https://habr.com/ru/all/page{page}" for page in range(1, 51))

  def parse(self, response):
    for article in response.css('.tm-title__link'):
      yield {'article_link': article.xpath('@href').get()}
     

 ##   scrapy runspider main.py -o links.json 