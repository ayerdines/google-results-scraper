from time import sleep
import grequests
from gevent import monkey
monkey.patch_all()

username = 'USERNAME'
password = 'PASSWORD'

class LPScrapper:
    def start_scraping(self, image_url, query):
        try:
            proxy = ('http://%s:%s@us.smartproxy.com:10000' % (username, password))
            query = "+".join(query.split())
            urls = ["https://images.google.com/searchbyimage?image_url={}&q={}".format(image_url, query)]*10
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, '
                                     'like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
            proxies = {
                'http': proxy,
                'https': proxy
            }
            requests_unsent = (grequests.get(url=u, headers=headers, proxies=proxies, timeout=10) for u in urls)
            # like map, but returns generator
            requests_iterable = grequests.imap(requests_unsent, size=4, stream=True, exception_handler=lambda x, y: "")

            # this is done synchronously -- can also potentially do on a queue
            for response in requests_iterable:
                if response.status_code != 200:
                    print("------captcha detected------")
                    response.close()
                    continue
                print("------first successful response------")
                return response.content
            return '<h3> NOT FOUND </h3>'

        except Exception as ex:
            import traceback
            traceback.print_exc()
            print(ex)
            return '<h3> NOT FOUND </h3>'


if __name__ == '__main__':
    image_url = 'https://images-na.ssl-images-amazon.com/images/I/51gVm-dTdvL.AC_SY200.jpg'
    query = "iphone amazon.com"
    scraper = LPScrapper()
    response = scraper.start_scraping(image_url=image_url, query=query)
    print(response)
