from calendar import c
from urllib.parse import urljoin
import scrapy


class BuildsSpider(scrapy.Spider):
	name = "builds"
	allowed_domains = ["lotv.spawningtool.com"]
	start_urls = ["https://lotv.spawningtool.com/build"]

	def parse_build_data(self, response):
		# created_by
		created_by = response.css('li:contains("Created by:") a::text').get()
		if created_by is None:
			created_by = response.css('li:contains("Created by:")::text').re_first(r'Created by:\s*(.*)')

		population_data = []

		# Loop through the population data and yield the results
		for line in response.xpath('//tr[not(contains(@style, "display: none"))]'):
			population_data.append({
				"population": str(line.xpath('td[1]/text()').get()).strip(),
				"timer": str(line.xpath('td[2]/text()').get()).strip(),
				"description": str(line.css('span.Building::text').get()).strip(),
			})

		yield {
			"title": response.css(".page-header > h1::text").get(),
			"description": response.css(".col-md-8 > p::text").get(),
			"link_video": response.css(".col-md-8 > a::attr(href)").get(),
			"link_build": response.url,
			'created_by' : (created_by.strip()),
			"published": (response.css('li:contains("Published on:")::text')).re_first(r'Published\s*on:\s*(.*)'),
			"patch": (response.css('li:contains("Patch:")::text')).re_first(r'Patch:\s*(.*)'),
			"difficulty": (response.css('li:contains("Difficulty:")::text')).re_first(r'Difficulty:\s*(.*)'),
			"match-up": response.meta['match-up'],
			"success": response.css("span.text-success::text").get(),
			"data": population_data,
		}
		
	def parse(self, response):
		for article in response.css('tr'):
			build_url = urljoin(self.start_urls[0], article.css("b > a::attr(href)").extract_first())
			extracted_data = article.css('td:nth-child(3)::text').get()
			yield scrapy.Request(url=build_url, callback=self.parse_build_data, meta={'match-up': extracted_data})

		next_page_url = response.css("a.pull-right::attr(href)").get()

		if next_page_url:
			yield response.follow(url=next_page_url, callback=self.parse)
