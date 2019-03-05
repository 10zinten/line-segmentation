import argparse
import os
from urllib.request import urlopen
from tqdm import tqdm
from google_orc import text_annotations

work = '0000'
igroup = '0000'

def download(args):
    global work, igroup
    url_seg = args.url.split("&")
    work = url_seg[0].split("=")[-1]
    igroup = url_seg[1].split("=")[-1]
    last_page = int(url_seg[-2].split("=")[-1])

    vol_dir = os.path.join("data", "{}_{}".format(work, igroup))
    if not os.path.exists(vol_dir):
        os.makedirs(vol_dir)

    for pg in tqdm(range(args.image, last_page+1)):
        page_fn = os.path.join(vol_dir, 'page-{0:03d}.png'.format(pg))
        if not os.path.exists(page_fn) or (os.path.isfile(page_fn) and os.path.getsize(page_fn) == 0):
            url_seg[2] = "image={}".format(pg)
            url = '&'.join(url_seg)
            with open(page_fn, 'wb') as f:
                f.write(urlopen(url).read())

        yield page_fn

def orc(pg_fn):
    output_dir = os.path.join(*pg_fn.split('/')[:-1], 'texts')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    fn = pg_fn.split('/')[-1].split('.')[0] + '.txt'
    output_pg_fn = os.path.join(output_dir, fn)
    texts = ''
    if not os.path.exists(output_pg_fn):
        texts = text_annotations(pg_fn)
    return texts


if __name__ == "__main__":

    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--url", type=str, help="url of image")
    ap.add_argument("--image", type=int, help="start page number", default=1)
    args = ap.parse_args()

    pages = []
    for pg_fn in download(args):
        texts = orc(pg_fn)
        pages.append(texts)

    with open('{}/{}-{}.txt'.format('output', work, igroup), 'w') as f:
        f.write('\n\n'.join(pages))
