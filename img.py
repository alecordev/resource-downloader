import os
import sys
import pathlib
import secrets
import urllib
import functools
import logging
import argparse

from concurrent.futures import ThreadPoolExecutor

import requests
import requests_html

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] - %(message)s')
here = pathlib.Path(__file__).parent.absolute()
os.chdir(here)
logging.info(f'Current working directory: {here}')


def download(directory, resource):
    """ Download resource using stdlib urllib """
    logging.debug(f'Downloading {resource}')
    filename = resource.split('/')[-1]
    logging.info(f'Filename: {filename}')
    if filename in os.listdir(os.curdir):
        logging.info(f'{filename} already present')
        return
    if (len(filename.split('.')[-1]) < 4) and '.' in filename:
        urllib.request.urlretrieve(resource, filename)


def requests_download(directory, resource):
    """ Download resource using requests """
    try:
        local_filename = url.split('/')[-1]
        r = requests.get(url, stream=True)
        with open(os.path.join(directory, local_filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        logging.exception('Error')


def fetch_images(r, directory):
    """ """
    try:
        download_partial = functools.partial(download, directory)
        images = r.html.find('img')
        logging.info(f'Found {len(images)} images to process')
        with ThreadPoolExecutor() as tp:
            tp.map(download_partial, [requests_html.urljoin(r.url, i.attrs['src']) for i in images if i.attrs.get('src', False)])
    except Exception as e:
        logging.exception('Failed fetching images')


def main(url, directory):
    """ Download all img resources in URL """

    if not url:
        raise Exception('URL is required')
    if not directory:
        directory = 'images'
        os.makedirs(directory, exist_ok=True)
        os.chdir(directory)
        logging.info(f'Using default download directory: {directory}')

    user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.01',
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                   'Mozilla/5.0 (Linux; Ubuntu 14.04) AppleWebKit/537.36 Chromium/35.0.1870.2 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
                   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0']
    headers = {'User-Agent': secrets.choice(user_agents)}

    with requests_html.HTMLSession() as session:
        r = session.get(url, headers=headers)
        fetch_images(r, directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, help='URL to fetch images from')
    parser.add_argument('-d', '--directory', type=str, help='Directory under CWD to save images to')
    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    main(args.url, args.directory)
