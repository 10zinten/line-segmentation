import argparse
import os
from urllib.request import urlopen
from tqdm import tqdm


def download(url):
    url_seg = url.split("&")
    work = url_seg[0].split("=")[-1]
    igroup = url_seg[1].split("=")[-1]
    last_page = int(url_seg[-2].split("=")[-1])

    vol_dir = os.path.join("data", "{}_{}".format(work, igroup))
    if not os.path.exists(vol_dir):
        os.makedirs(vol_dir)

    for pg in tqdm(range(1, last_page+1)):
        page_fn = os.path.join(vol_dir, 'page-{0:03d}.png'.format(pg))
        if not os.path.exists(page_fn) or (os.path.isfile(page_fn) and os.path.getsize(page_fn) == 0):
            url_seg[2] = "image={}".format(pg)
            url = '&'.join(url_seg)
            with open(page_fn, 'wb') as f:
                f.write(urlopen(url).read())


if __name__ == "__main__":

    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--url", type=str, help="url of image")
    args = ap.parse_args()

    download(args.url)
