import cv2
import numpy as np


def attach_images(img1, img2):
    h1, w1, c1 = img1.shape
    h2, w2, c2 = img2.shape
    bigger_height = max(h1, h2)
    bigger_width = max(w1, w2)
    smaller_height = min(h1, h2)
    smaller_width = min(w1, w2)

    if bigger_width == w1:
        img_ratio = w2 / w1
        w1 = w2
        h1 = int(h1 * img_ratio)
        img1 = cv2.resize(img1, (w1, h1))
    else:
        img_ratio = w1 / w2
        w2 = w1
        h2 = int(h2 * img_ratio)
        img2 = cv2.resize(img2, (w2, h2))

    attached = np.vstack((img1, img2))

    return attached
