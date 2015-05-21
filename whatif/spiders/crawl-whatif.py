from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from whatif.items import WhatifItem
from scrapy.http import Request

class WhatifSpider(BaseSpider):
    name = "whatif"
    allowed_domains = ["what-if.xkcd.com"]
    start_urls = ["http://what-if.xkcd.com/1/"]
    base_url = 'http://what-if.xkcd.com/'

    def make_url(self, url):
        import re
        url = re.search(r'href=[\'"]?([^\'" >]+)', url).group(0)[6:]
        if url.startswith("http"):
            return url
        else:
            return self.base_url+url[1:]

    def _download_url(self, url, filename):
        from urllib import urlretrieve as retrieve
        import os
        if not os.path.exists(filename):
            print "Saving ", url, " as ", filename
            retrieve(url, filename)

    def download_image(self, images):
        import re, os
        urls = map(lambda x:re.search(r'src=[\'"]?[^\'" >]*', x).group(0)[5:], images)
        for dirname in map(os.path.dirname, urls):
            if dirname.startswith(self.base_url):
                dirname = dirname[len(self.base_url):]
            else:
                dirname = dirname[1:]
            if not os.path.exists(dirname):
                print "Creating directory:: ", dirname
                os.makedirs(dirname)
        for url in urls:
            if not url.startswith('http'):
                url = self.base_url + url[1:]
            self._download_url(url, url[len(self.base_url):])

    def write(self, item):
        import re, os
        title = re.split(r'[<>]', item['title'][0])[2]
        filename = item['No'].zfill(3) + '-' + title
        if os.path.exists(filename):
            return
        with open(filename, 'w') as f:
            print "Saving to file: ", filename
            f.write(item['article'][0].encode('utf-8'))
            f.write('\n')

    def parse(self, response):
        hxs = HtmlXPathSelector(response).xpath('//*[@id="entry-wrapper"]')
        items = []
        item = WhatifItem()
        item['No'] = response.url.split('/')[3]
        item['title'] = hxs.xpath('article/a/h1').extract()
        item['article'] = hxs.xpath('article').extract()
        item['question'] = hxs.xpath('//*[@id="question"]').extract()
        item['attribute'] = hxs.xpath('//*[@id="attribute"]').extract()
        links = hxs.xpath('//li[@class="nav-next"]/a')
        item['link'] = self.make_url(links[0].extract()) if len(links) > 0 else None
        item['images'] = hxs.xpath('//img[@class="illustration"]').extract()
        self.download_image(item["images"])
        self.write(item)
        items.append(item)
        yield Request(item['link'], callback=self.parse)
