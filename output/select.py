import argparse
import glob
from pathlib import Path

import cv2

ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("--dir", type=str, help="path to volume")
ap.add_argument("--test", default=False, action="store_true")
args = ap.parse_args()

path = Path(args.dir)
fns = sorted([o for o in path.iterdir() if not o.name.endswith('.png')])

if args.test:
    fns = fns[:2]

def select():
    good_psegs = []

    for page in fns:
        is_good = False
        is_good_quality = False

        ORG = 'original'
        org_img = cv2.imread(str(page)+'.png')
        org_img = cv2.resize(org_img, (1000, 200))
        cv2.namedWindow(ORG)
        cv2.moveWindow(ORG, 0, 0)
        cv2.imshow(ORG, org_img)

        PSEG = 'pseg'
        pseg_img = cv2.imread(str(page)+'.pseg.png')
        pseg_img = cv2.resize(pseg_img, (1000, 200))
        cv2.namedWindow(PSEG)
        cv2.moveWindow(PSEG, 0, 300)
        cv2.imshow(PSEG, pseg_img)

        # Display all the individual line
        lines = glob.glob(str(page) + '/*')
        lines = sorted(lines)
        # check for 7 lines, which is good seg
        is_good = True if len(lines) == 7 else False

        for i, line in enumerate(lines):
            LINE = 'lines ' + str(i+1)
            line_img = cv2.imread(line)
            line_img = cv2.resize(line_img, (1000, 50))
            cv2.namedWindow(LINE)
            cv2.moveWindow(LINE, 0, 600)
            cv2.imshow(LINE, line_img)
            cv2.waitKey(0)
            cv2.destroyWindow(LINE)

        # Check for good pageseg quality, assume there is 7 lines
        if is_good and not is_good_quality:
            while True:
                res = input('[INFO]  Is pageseg quality good [y/n]: ')
                if isinstance(res, str):
                    if res is 'y':
                        is_good_quality = True
                        break
                    elif res is 'n':
                        is_good_quality = False
                        break
                    else:
                        print('\n[ERROR]  please response y / n')

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        if is_good and is_good_quality:
            good_psegs.append(page)

    print('[INFO]  Found', len(good_psegs), 'good psegs')

    # Save all the good pseg filename to file
    with open('good_pseg.txt', 'w') as f:
        for page in good_psegs:
            f.write(str(page) + '\n')
        print('[INFO] saved successfully !')

if __name__ == "__main__":
    select()
