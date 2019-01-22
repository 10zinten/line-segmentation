import argparse
import io
import glob
import os

from google.cloud import vision
from google.cloud.vision import types


vision_client = vision.ImageAnnotatorClient()

def text_annotations(fn):
    with io.open(fn, 'rb') as image_file:
        content = image_file.read()
        image = types.Image(content=content)

    response = vision_client.document_text_detection(image=image)
    texts = response.text_annotations

    try:
        return texts[0].description
    except:
        return ""


if __name__ == "__main__":

    from tqdm import tqdm

    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--dir", type=str, help="url of image")
    ap.add_argument("--image", type=int, help="start page number", default=1)
    args = ap.parse_args()

    fns = sorted([o for o in glob.glob(args.dir + '/*') if o.endswith('.png')])

    for fn in tqdm(fns[args.image-1:]):
        output_dir = os.path.join(args.dir, 'texts')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_fn = fn.split('/')[-1].split('.')[0] + '.txt'
        output_pg_fn = os.path.join(output_dir, output_fn)
        if not os.path.exists(output_pg_fn):
            texts = text_annotations(fn)
            with open(output_pg_fn, 'w') as f:
                f.write(texts)
