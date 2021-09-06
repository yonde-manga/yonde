import random
import requests
import http.client
from yonde.exceptions.exceptions import TooManyRedirectsException, ConnectionErrorException, ForbiddenUrlException, \
    FailedImageException
http.client._MAXHEADERS = 1000


class Session(object):
    def __init__(self, headers=None, cloudflare=False):
        self._user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
                             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) '
                             'Version/9.0.2 Safari/601.3.9',
                             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/47.0.2526.111 Safari/537.36',
                             'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
                             'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/51.0.2704.64 Safari/537.36']
        self.__headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                        " Chrome/91.0.4472.164 Safari/537.36"}
        if cloudflare:
            import cloudscraper
            self.session = cloudscraper.CloudScraper()
        else:
            self.session = requests.Session()
        self.session.headers.update(headers if headers else self.__headers)

    def get(self, url, random_ua=False):
        try:
            if random_ua:
                self.update_headers({'user-agent': random.choice(self._user_agents)})
            req = self.session.get(url)
            if req.status_code == 403:
                raise ForbiddenUrlException(f'ForbiddenUrl - {url} ({req.status_code})')
            elif len(req.content) == 0:
                raise FailedImageException(f'FailedImage - {url} ({req.status_code})')
            return req
        except requests.exceptions.TooManyRedirects:
            raise TooManyRedirectsException(f'TooManyRedirects - {url} ({req.status_code})')
        except requests.exceptions.ConnectionError:
            raise ConnectionErrorException(f'ConnectionError - {url} ({req.status_code})')

    def update_headers(self, new_headers):
        self.session.headers.update(new_headers)
