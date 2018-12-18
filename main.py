import argparse
import os
from PIL import Image
import glob


def page_num(fn, offset):
    fn = fn.split("/")[-1]
    name, ext = fn.split('.')
    prefix, idx = name.split('-')
    idx = int(idx) - offset
    fn = 'output/preprocess/' + prefix + '-' + str(idx) + '.' + ext
    return fn


def preprocess(fn, offset):
    '''Reize the image, set correct page number and set dpi to 300
       Return: correct page number of Pecha'''

    img = Image.open(fn)
    img = img.resize((img.size[0], 500), Image.ANTIALIAS)
    img.save(page_num(fn, offset), dpi=(300, 300))


def pageseg(fn):
    pass

def process(path, offset):
    fns = glob.glob(path + "/*")
    for fn in fns:
        preprocess(fn, offset)
        pageseg(fn)


if __name__ == "__main__":

    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--dir", type=str, help="path to volume")
    ap.add_argument("--offset", type=int, help="page offset")
    args = ap.parse_args()

    process(args.dir, args.offset)
