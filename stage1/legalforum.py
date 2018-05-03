import scrapy
import re

SESSION_ID = re.compile(r's=[a-f0-9]{32}\&')

ROOT_URL = 'http://legal-forum.ru/'


class LegalforumSpider(scrapy.Spider):
    name = "legalforum"

    def start_requests(self):
        urls = [ROOT_URL]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_main)

    def parse_main(self, response):
        threads = response.xpath("//td[@class='alt1Active']//a/@href").extract()
        for t in threads:
            link = ROOT_URL + SESSION_ID.sub('', t)
            yield response.follow(link, self.parse_thread)
            yield response.follow(link, self.parse_main)

    def parse_thread(self, response):
        threads = response.xpath("//td[@class='alt1']//a[contains(@href, 'showthread.php')]/@href").extract()
        for t in threads:
            link = ROOT_URL + SESSION_ID.sub('', t)
            yield response.follow(link, self.parse_posts)

        next_link = response.xpath("//div[@class='pagenav']//a[text()='>']/@href").extract_first()
        if next_link:
            yield response.follow(ROOT_URL + SESSION_ID.sub('', next_link), self.parse_thread)

    def parse_posts(self, response):
        lines = response.xpath("//div[contains(@id, 'post_message_')]/text()").extract()
        yield {'text': '\n'.join(line.strip() for line in lines if line.strip())}

        next_link = response.xpath("//div[@class='pagenav']//a[text()='>']/@href").extract_first()
        if next_link:
            yield response.follow(ROOT_URL + next_link, self.parse_posts)
