# demodulate the signal into soft decisions
# (distances from constellation points)

import numpy as np
import setup

# dict of constellation points
constellation = {
    0: np.exp(1j * 0 * np.pi / 4),  # 000
    1: np.exp(1j * 1 * np.pi / 4),  # 001
    2: np.exp(1j * 2 * np.pi / 4),  # 011
    3: np.exp(1j * 3 * np.pi / 4),  # 010
    4: np.exp(1j * 4 * np.pi / 4),  # 110
    5: np.exp(1j * 5 * np.pi / 4),  # 111
    6: np.exp(1j * 6 * np.pi / 4),  # 101
    7: np.exp(1j * 7 * np.pi / 4)   # 100
}


# def demodulate_8psk(point: np.complex128) -> float:
#     # calculate distances from all constellation points
#     distances = np.zeros((8,))
#     a = np.array((point.real, point.imag))
#     for i in range(8):
#         b = setup.power * \
#             np.array((constellation[i].real, constellation[i].imag))
#         distances[i] = np.linalg.norm(a-b)
#     return distances

def demodulate_8psk(signal: np.ndarray) -> np.ndarray:
    # calculate distances from all constellation points
    distances = np.zeros((signal.size, 8))
    for i in range(signal.size):
        a = np.array((signal[i].real, signal[i].imag))
        for j in range(8):
            b = setup.power * \
                np.array((constellation[j].real, constellation[j].imag))
            distances[i][j] = np.linalg.norm(a-b)

    return distances
