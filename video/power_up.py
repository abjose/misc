import cv2
import numpy as np
import random

def filter(idx, blur_iters, shake):
    img = cv2.imread(f"images/img{idx:04d}.bmp")
    w, h = img.shape[:2]

    center_x = 889 #w / 2
    center_y = 424 #h / 2
    blur = 0.01
    iterations = int(blur_iters)

    growMapx = np.tile(np.arange(h) + ((np.arange(h) - center_x)*blur), (w, 1)).astype(np.float32)
    shrinkMapx = np.tile(np.arange(h) - ((np.arange(h) - center_x)*blur), (w, 1)).astype(np.float32)
    growMapy = np.tile(np.arange(w) + ((np.arange(w) - center_y)*blur), (h, 1)).transpose().astype(np.float32)
    shrinkMapy = np.tile(np.arange(w) - ((np.arange(w) - center_y)*blur), (h, 1)).transpose().astype(np.float32)

    for i in range(iterations):
        tmp1 = cv2.remap(img, growMapx, growMapy, cv2.INTER_LINEAR)
        tmp2 = cv2.remap(img, shrinkMapx, shrinkMapy, cv2.INTER_LINEAR)
        img = cv2.addWeighted(tmp1, 0.5, tmp2, 0.5, 0)

    # translate
    shake = int(shake)
    dx = random.randrange(-1 * shake, shake)
    dy = random.randrange(-1 * shake, shake)
    T = np.float32([[1, 0, dx], [0, 1, dy]]) 
    img = cv2.warpAffine(img, T, (w, h))


    cv2.imwrite(f"output/img{idx:04d}.bmp", img)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)

if __name__=="__main__":
    start = 1 #150
    end = 149#239
    size = end-start+1
    
    start_blur = 1
    end_blur = 250
    
    start_shake = 1
    end_shake = 100

    blur = np.geomspace(start_blur, end_blur, size)
    shake = np.geomspace(start_shake, end_shake, size)
    for i in range(size):
        filter(start + i, blur[i], shake[i])
