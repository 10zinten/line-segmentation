import os
from pathlib import Path
from collections import defaultdict

from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm


text_path = Path('../derge-kangyur/derge-kangyur-tags/').resolve()
vol_path = Path('output/volumes/')


def find_img_num(code):
    pg, _ = code.split('.')
    n = 2*int(pg[:-1])
    if pg[-1] is 'a': n -= 1
    return n

def remove_markup(line):
    line = line.replace("[", "")
    line = line.replace("]", "")
    if ',' in line:
        result = []
        sub_line = line.split(',')
        for sub in sub_line:
            sub = sub.replace("(", "")
            idx = sub.find(")")
            if idx != -1:
                sub = sub[idx+1:]
            result.append(sub)
        return ''.join(result)
    return line

def to_raw_text(line):
    idx = line.find("]")
    desp, line = line[:idx], line[idx+1:]
    desp = desp[1:]
    line = line[:-1]
    return remove_markup(line), find_img_num(desp)

def is_text_line(line):
    line = line[line.find("]")+1:]
    return len(line) > 20

def create_text_dict(nvol, text_fn):
    text_dict = defaultdict(list)

    with open(str(text_fn)) as f:
        text_lines = f.readlines()

    for line in text_lines:
        if is_text_line(line):
            raw_text, n = to_raw_text(line)
            text_dict[n].append(raw_text)
    return text_dict

def create_img_dict(vol):
    images = defaultdict(list)

    psegs = sorted([o for o in vol.iterdir()
                    if o.is_dir() and (len(list(o.iterdir())) <= 7 or (o.name == 'page-003' and len(list(o.iterdir())) == 6))
                ])

    for pseg in psegs:
        n = int(pseg.name.split('-')[-1])
        images[n].extend(['/'.join(o.parts[-3:]) for o in sorted(list(pseg.iterdir()))])
    return images

def create_csv(vol, images, texts):
    all_images, all_texts = [], []
    for k in images:
        if (k == 3 and len(images[k]) == 6) or len(texts[k]) == 7:
            all_images.extend(images[k])
            all_texts.extend(texts[k])
    df = pd.DataFrame({'filename': all_images, 'text': all_texts})
    df.to_csv(str(vol_path/'{}.csv'.format(vol)), index=False)
    return df

if __name__ == "__main__":
    for vol in tqdm([o for o in vol_path.iterdir() if o.is_dir()]):
        n = int(vol.name.split('-')[-1])
        texts = create_text_dict(n, text_path/'{0:03d}-tagged.txt'.format(n))
        images = create_img_dict(vol)

        create_csv('vol-{0:03d}'.format(n), images, texts)
