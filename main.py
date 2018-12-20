import argparse
import os
from PIL import Image
import glob
import subprocess


def page_name(fn, offset):
    f_dir = fn.split("/")
    fn = f_dir[-1]
    vol_dir = os.path.join('output', f_dir[-2])
    if not os.path.exists(vol_dir):
            os.makedirs(vol_dir)
    name, ext = fn.split('.')
    prefix, idx = name.split('-')
    idx = int(idx) - offset
    fn = prefix + '-' + str(idx) + '.' + ext
    fn_path = os.path.join(vol_dir, fn)
    return fn_path


def preprocess(fn, offset):
    '''Reize the image, set correct page number and set dpi to 300
       Return: correct page number of Pecha'''

    img = Image.open(fn)
    fn = page_name(fn, offset)

    img = img.resize((img.size[0], 500), Image.ANTIALIAS)
    img.save(fn, dpi=(300, 300))
    return fn


def pageseg(fn):
    cmd = 'ocropus-gpageseg -n --maxlines 7' + fn
    # subprocess.check_output(cmd)
    subprocess.call(cmd, shell=True)

def process(path, offset):
    fns = glob.glob(path + "/*")
    for fn in fns:
        fn = preprocess(fn, offset)
        print(fn)
        pageseg(fn)


if __name__ == "__main__":

    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--dir", type=str, help="path to volume")
    ap.add_argument("--offset", type=int, help="page offset")
    args = ap.parse_args()

    process(args.dir, args.offset)
