import os
import sys
import datetime
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup

def log(msg):
    """
    Simple logging wrapper
    """
    print('[{}] {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f'), msg))

def validate_url(url):
    """
    Takes a href or src string and makes it a valid absolute URI
    to access its contents.

    :param url: href or src URL
    :type url: str

    :return: absolute URL
    :rtype: str
    """
    # valid_schemas = set(['http://', 'https://'])
    
    # if not any(map(url.startswith, valid_schemas)):
    #     url = 'http://' + url

    # parsed_url = urllib.parse.urlparse(url)

    # if 'http://' not in sys.argv[1] and 'https://' not in sys.argv[1]:
    #     sys.argv[1] = 'http://' + sys.argv[1]

    # if sys.argv[1] not in url:
    #     url = urllib.parse.urljoin(sys.argv[1], parsed_url.geturl())

    # import pdb; pdb.set_trace()

    # log('Validated URL: {}'.format(url))
    return urllib.parse.urljoin(sys.argv[1], url)

def download(url):
    try:
        os.makedirs('downloads')
    except Exception as e:
        # log(e)
        pass

    try:
        local_filename = url.split('/')[-1]
        r = requests.get(url, stream=True)
        with open(os.path.join('downloads', local_filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        log(e)

def resource_downloader(hrefs):
    resource_criteria = ['css', 'js']
    to_download = list(map(validate_url, [href for href in hrefs for criteria in resource_criteria if href.endswith(criteria)]))
    try:
        if 'test' in sys.argv:
            log(' test '.center(20, '-'))
            log('To download: {}'.format(to_download))
        else:
            with ThreadPoolExecutor(8) as t_pool:
                t_pool.map(download, to_download)
    except Exception as e:
        log(e)

def soupify(url):
    try:
        url = validate_url(url)
        return BeautifulSoup(requests.get(url, headers={'User-Agent': 'User-Agent'}).content, 'lxml')
    except Exception as e:
        log(e)

def main():
    """
    $ python resource_downloader.py url <test>
    """
    log(sys.argv)
    if len(sys.argv) > 1:
        soup = soupify(sys.argv[1])
        resource_downloader([href['href'] for href in soup.find_all(href=True)])
        resource_downloader([href['src'] for href in soup.find_all(src=True)])

if __name__ == '__main__':
    main()