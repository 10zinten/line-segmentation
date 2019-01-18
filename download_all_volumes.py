import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
from tqdm import tqdm


def page_length():
    with open('data/links.html') as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    pg_len = []
    for a in soup.find_all('a'):
        o = a['href'].split('%')

        code = o[1].split('C')[-1]
        pg = o[2].split('C')[-1]
        ln = o[-1].split('C')[-1]
        pg_len.append((code, pg, ln))

    return pg_len


def download_all_volumes():
    for code, vol, ln in page_length():
        page_dir = 'data/volumes/' + 'vol-{}'.format(vol)
        if not os.path.exists(page_dir):
             os.makedirs(page_dir)
        print('[INFO]  Volume-{} downloading....'.format(vol))
        for pg in tqdm(range(1, int(ln)+1)):
            url = 'https://www.tbrc.org/browser/ImageService?work=W22084&igroup={}&image={}&first=1&last={}&fetchimg=yes'.format(code, pg, ln)
            with open(page_dir + '/page-{0:03d}'.format(pg), 'wb') as f:
                f.write(urlopen(url).read())

            if pg == 5:
                break


if __name__ == "__main__":
    download_all_volumes()
