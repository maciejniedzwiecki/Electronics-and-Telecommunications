# graycode conversion

import numpy as np


def bin_to_gray(binary: np.uint8) -> np.uint8:
    # convert binary code to graycode
    return binary ^ (binary >> 1)


def gray_to_bin(gray: np.uint8) -> np.uint8:
    # convert graycode to binary
    mask = gray >> 1
    while mask != 0:
        gray = gray ^ mask
        mask = mask >> 1
    return gray
