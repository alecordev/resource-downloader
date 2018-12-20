import os
import pathlib
import secrets
import urllib

from concurrent.futures import ThreadPoolExecutor

import requests
import requests_html

here = pathlib.Path(__file__).parent.absolute()
os.chdir(here)


def download(resource):
    urllib.request.urlretrieve(resource, resource.split('/')[-1])


def main(url):
    """ Download all img resources in URL """
    user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36']
    headers = {'User-Agent': secrets.choice(user_agents)}
    with requests_html.HTMLSession() as session:
        r = session.get(url, headers=headers)
        images = r.html.find('img')
        with ThreadPoolExecutor() as tp:
            tp.map(download, [requests_html.urljoin(r.url, i.attrs['src']) for i in images])


if __name__ == "__main__":
    main()
