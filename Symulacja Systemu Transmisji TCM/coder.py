# encode the frame

import numpy as np


def xor(a: np.uint8) -> np.uint8:
    # xor the bits of the argument
    if a in {1, 2, 4, 7}:
        return np.uint8(1)
    else:
        return np.uint8(0)


def encode_frame(a: np.ndarray) -> np.ndarray:
    # encode the entire frame
    # transmit the first bit as is
    # push the second bit through
    # a [5, 7] convolutional encoder
    encoded = np.zeros((a.size + 2,), dtype=np.uint8)  # init the array
    sr = np.uint8(0)  # init shift register
    for i in range(a.size):  # conv. enc.
        sr = sr + ((a[i] & 1) << 2)
        c0 = (a[i] & 2) << 1
        c1 = xor(sr & 5) << 1
        c2 = xor(sr)
        encoded[i] = c0+c1+c2
        sr = sr >> 1

    # add tail, to always end up in 0 state
    if sr == 0:
        encoded[-2] = 4
        encoded[-1] = 0
    elif sr == 1:
        encoded[-2] = 7
        encoded[-1] = 0
    elif sr == 2:
        encoded[-2] = 5
        encoded[-1] = 3
    else:
        encoded[-2] = 6
        encoded[-1] = 3

    return encoded
