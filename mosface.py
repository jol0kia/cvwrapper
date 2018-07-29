#!/usr/bin/env python3

import cv2, sys, re

PATH_CASCADE     = "/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"
DET_MINSIZ       = 100
RATE_MOS         = 30
FLG_DETREC       = True
DETREC_COLOR     = (0, 255, 0)
DETREC_THICKNESS = 8

print("[info]  processing ... ({0})".format(__file__))

if len(sys.argv) == 2:
    path_src = sys.argv[1]
    path_dst = re.sub(r'\.jpg$|\.jpeg$|\.png$|\.PNG$', '-mos.jpg', path_src)
elif len(sys.argv) == 3:
    path_src = sys.argv[1]
    path_dst = sys.argv[2]
else:
    print("[error] invalid argument!")
    quit()

if path_src == path_dst:
    print("[error] invalid argument!")
    quit()

print("[info]      input  image: {0}".format(path_src))

img     = cv2.imread(path_src)
img_gs  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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
    img_fc = img[y:y+h, x:x+w]
    img_fc = cv2.resize(img_fc, (w//RATE_MOS, h//RATE_MOS))
    img_fc = cv2.resize(img_fc, (w, h), interpolation=cv2.INTER_AREA)
    img[y:y+h, x:x+h] = img_fc

    if FLG_DETREC:
        cv2.rectangle(img, (x,y), (x+w, y+h), DETREC_COLOR, thickness=DETREC_THICKNESS)

cv2.imwrite(path_dst, img)
print("[info]      output image: {0}".format(path_dst))
print("[info]  ... complete! ({0})".format(__file__))

