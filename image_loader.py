import os

import cv2


def load_an_image(image_file):
    result = cv2.imread(image_file)

    return result


def get_image_nums(folder_dir):
    dir_listing = os.listdir(folder_dir)
    return len(dir_listing)
