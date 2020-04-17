# -*- coding: utf-8 -*-
import scrapy
from ..items import StackOverflowScrapperItem


class PythonQuestionSpider(scrapy.Spider):
    name = 'python_question'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['https://stackoverflow.com/questions/tagged/python?tab=newest&page=1&pagesize=15']
    page_number = 1

    def parse(self, response):
        question_div = response.css('.question-summary')
        item = StackOverflowScrapperItem()

        for question in question_div:
            item['title'] = question.css('.question-hyperlink::text').extract()
            item['description'] = question.css('.excerpt::text').extract()
            item['asked_by'] = question.css('.user-details a::text').extract()
            item['views'] = question.css('.views::text').extract()
            item['votes'] = question.css('.vote-count-post strong::text').extract()
            item['answers'] = question.css('.unanswered strong::text , .answered::text').extract()
            item['tags'] = question.css('.post-tag::text').extract()

            yield item

        self.page_number += 1
        next_page = "https://stackoverflow.com/questions/tagged/python?tab=newest&page={self.page_number}&pagesize=15"
        if self.page_number < 300:
            yield response.follow(next_page, callback=self.parse)
