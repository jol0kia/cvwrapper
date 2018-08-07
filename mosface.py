#!/usr/bin/env python3

import cv2, sys, re
import argparse

PATH_CASCADE     = "/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"
DET_MINSIZ       = 100
RATE_MOS         = 30
FLG_DETREC       = True
DETREC_COLOR     = (0, 255, 0)
DETREC_THICKNESS = 8

def options(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--sfile", default=None, help="source image file name")
    ap.add_argument("-d", "--dfile", default=None, help="destination image file name")
    ap.add_argument("-b", "--brot", default="0", help="rotate before processing [degree]")
    ap.add_argument("-a", "--arot", default="0", help="rotate after processing [degree]")

    pa = ap.parse_args(argv[1:])
    return pa

def main(argv):
    print("[info]  processing ... ({0})".format(__file__))

    opt = options(argv)

    if opt.sfile is None:
        print("[error] sfile invalid")
        return 1
    else:
        path_src = opt.sfile

    if opt.dfile is None:
        path_dst = re.sub(r'\.jpg$|\.jpeg$|\.png$|\.PNG$', '-mos.jpg', path_src)
    else:
        path_dst = opt.dfile

    if path_src == path_dst:
        print("[error] invalid argument! (path_src = path_dst = {0}".format(path_src))
        quit()

    print("[info]      input  image: {0}".format(path_src))

    img = cv2.imread(path_src)

    if opt.brot == '0':
        flg_brot  = False
        img_brot  = img
    elif opt.brot == '90':
        flg_brot  = True
        path_brot = re.sub(r'\.jpg$|\.jpeg$|\.png$|\.PNG$', '-brot.jpg', path_src)
        img_brot  = img.transpose(1,0,2)[:,::-1]
    elif opt.brot == '180':
        flg_brot  = True
        path_brot = re.sub(r'\.jpg$|\.jpeg$|\.png$|\.PNG$', '-brot.jpg', path_src)
        img_brot  = cv2.flip(img, -1)
    elif opt.brot == '270':
        flg_brot  = True
        path_brot = re.sub(r'\.jpg$|\.jpeg$|\.png$|\.PNG$', '-brot.jpg', path_src)
        img_brot  = img.transpose(1,0,2)[::-1]
    else:
        print("[error] invalid argument! (brot = {0})".format(opt.brot))
        quit()

    if flg_brot:
        cv2.imwrite(path_brot, img_brot)
        print("[info]      output image: {0}".format(path_brot))

    img_gs  = cv2.cvtColor(img_brot, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(PATH_CASCADE)
    l_fc    = cascade.detectMultiScale(img_gs,
                scaleFactor=1.1,
                minNeighbors=1,
                minSize=(DET_MINSIZ, DET_MINSIZ))

    if len(l_fc) == 0:
        print("[warn]  no face!")
        quit()

    for (x,y,w,h) in l_fc:
        print("[info]          face detected ({0}, {1}, {2}, {3})".format(x,y,w,h))
        img_fc = img_brot[y:y+h, x:x+w]
        img_fc = cv2.resize(img_fc, (w//RATE_MOS, h//RATE_MOS))
        img_fc = cv2.resize(img_fc, (w, h), interpolation=cv2.INTER_AREA)
        img_brot[y:y+h, x:x+h] = img_fc

        if FLG_DETREC:
            cv2.rectangle(img_brot, (x,y), (x+w, y+h), DETREC_COLOR, thickness=DETREC_THICKNESS)

    if opt.arot == '0':
        flg_arot  = False
    elif opt.arot == '90':
        flg_arot  = True
        path_arot = re.sub(r'\.jpg$|\.jpeg$|\.png$|\.PNG$', '-arot.jpg', path_src)
        img_arot  = img_brot.transpose(1,0,2)[:,::-1]
    elif opt.arot == '180':
        flg_arot  = True
        path_arot = re.sub(r'\.jpg$|\.jpeg$|\.png$|\.PNG$', '-arot.jpg', path_src)
        img_arot  = cv2.flip(img_brot, -1)
    elif opt.arot == '270':
        flg_arot  = True
        path_arot = re.sub(r'\.jpg$|\.jpeg$|\.png$|\.PNG$', '-arot.jpg', path_src)
        img_arot  = img_brot.transpose(1,0,2)[::-1]
    else:
        print("[error] invalid argument! (arot = {0})".format(opt.arot))
        quit()

    cv2.imwrite(path_dst, img_brot)
    print("[info]      output image: {0}".format(path_dst))

    if flg_arot:
        cv2.imwrite(path_arot, img_arot)
        print("[info]      output image: {0}".format(path_arot))

    print("[info]  ... complete! ({0})".format(__file__))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
