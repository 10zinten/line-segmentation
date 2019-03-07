import argparse
import os
from urllib.request import urlopen

from tqdm import tqdm
from wand.image import Image as wi
from google_ocr import text_annotations


work = '0000'
igroup = '0000'


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


def get_url_seg(url):
    global work, igroup
    url_seg = args.url.split("&")
    work = url_seg[0].split("=")[-1]
    igroup = url_seg[1].split("=")[-1]
    first_page = url_seg[-3].split("=")[-1]
    last_page = int(url_seg[-2].split("=")[-1])
    return url_seg, work, igroup, first_page, last_page


def single_image_download(url, page_fn):
    with open(page_fn, 'wb') as f:
        f.write(urlopen(url).read())
    return page_fn


def is_singin_required(url):
    test_text = 'Copyright Work'

    _, work, igroup, first_pg, last_pg = get_url_seg(url)
    url = 'https://www.tbrc.org/browser/ImageService?work={}&igroup={}&image={}&first={}&last={}&fetchimg=yes'.format(
                work, igroup, int(first_pg)+30, first_pg, last_pg)
    print(url)
    page_fn = single_image_download(url, './data/test.png')
    texts = orc(page_fn)
    print(texts)
    return test_text in texts

def download_images(args, work_dir):
    url_seg, work, igroup, first_pg, last_pg = get_url_seg(url)

    for pg in tqdm(range(args.image, last_page+1)):
        page_fn = os.path.join(work_dir, 'page-{0:03d}.png'.format(pg))
        if not os.path.exists(page_fn) or (os.path.isfile(page_fn) and os.path.getsize(page_fn) == 0):
            url_seg[2] = "image={}".format(pg)
            url = '&'.join(url_seg)
            download(url, page_fn)

        yield page_fn


def is_pdf_exist(work, igroup):
    pass


def from_pdf(file_path, start, work_dir):
    pdf = wi(filename=file_path, resolution=300)
    pdfImage = pdf.convert("png")
    print(pdfImage)
    pg_n = start
    for img in pdfImage.sequence:
        page = wi(image=img)
        page_fn = os.path.join(work_dir, 'page-{:03}.png'.format(pg_n))
        page.save(filename=page_fn)
        pg_n += 1
        return page_fn


def create_workdir(url):
    _, work, igroup, _, _ = get_url_seg(url)
    work_dir = os.path.join("data", "{}_{}".format(work, igroup))
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    return work_dir


if __name__ == "__main__":

    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--url", type=str, help="url of image")
    ap.add_argument("--image", type=int, help="start page number", default=1)
    args = ap.parse_args()

    pages = []

    work_dir = create_workdir(args.url)
    if is_singin_required(args.url):
        print('[INFO] Singin required !!!!')
        page_fn = from_pdf('data/W1PD96682-I1PD96888-1-626-any.pdf', args.image, work_dir)
        print(page_fn)
    # else:
        # for pg_fn in download(args):
        #     texts = orc(pg_fn)
        #     pages.append(texts)

    # with open('{}/{}-{}.txt'.format('output', work, igroup), 'w') as f:
    #     f.write('\n\n'.join(pages))
