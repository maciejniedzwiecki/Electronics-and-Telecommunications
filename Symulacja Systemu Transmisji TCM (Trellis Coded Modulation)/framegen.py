# create the frame

import numpy as np
import random
import setup


def generate_frame(size: int = setup.frame) -> np.ndarray:
    # generate a frame
    size = setup.frame
    frame = np.zeros((size,), dtype=np.uint8)
    for i in range(size):
        frame[i] = random.randint(0, 3)

    return frame
