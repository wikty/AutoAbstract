import scrapy

class QDailySpider(scrapy.Spider):
	name = 'qdaily-spider'

	start_urls = ['http://www.qdaily.com/tags/1068.html']

	def parse(self, response):
		with open('filelist.txt', 'w', encoding='utf-8') as f:
			for link in response.xpath('//div[@class="page-content"]/div/div/a[contains(@href, "article")]'):
				url = link.xpath('@href').extract_first()
				if url:
					url = response.urljoin(url)
					request = scrapy.Request(url, callback=self.parse_article)
					request.meta['filename'] = url.split('/')[-1].split('.')[-2] + '.txt'
					f.write(request.meta['filename']+'\n')
					yield request

	def parse_article(self, response):
		lines = response.xpath('//div[@class="article-detail-bd"]/*[@class="detail"]/p[following-sibling::p[contains(text(), "题图")]]/text()').extract()
		lines = [line.strip() for line in lines if line.strip()]
		with open(response.meta['filename'], 'w', encoding='utf-8') as f:
			f.write('\n'.join(lines))