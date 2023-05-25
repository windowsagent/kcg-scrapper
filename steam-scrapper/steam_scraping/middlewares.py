import warnings

import scrapy_warcio


class WarcioDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.warcio = scrapy_warcio.ScrapyWarcIo()
        self.warcio.config["warc_dest"] = settings["WARC_STORE"]

    def process_request(self, request, spider):
        request.meta["WARC-Date"] = scrapy_warcio.warc_date()
        return None

    def process_response(self, request, response, spider):
        ok = 200 <= response.status < 300
        is_resource = request.meta.get("is_resource")
        test_mode = request.meta.get("test_mode")
        if ok and not is_resource and not test_mode:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.warcio.write(response, request)
        return response
