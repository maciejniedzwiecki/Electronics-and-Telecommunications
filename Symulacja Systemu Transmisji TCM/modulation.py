# 8-psk modulation

import numpy as np
import gray
import setup

# dict of constellation points
constellation = {
    0: np.exp(1j * 0 * np.pi / 4),
    1: np.exp(1j * 1 * np.pi / 4),
    2: np.exp(1j * 2 * np.pi / 4),
    3: np.exp(1j * 3 * np.pi / 4),
    4: np.exp(1j * 4 * np.pi / 4),
    5: np.exp(1j * 5 * np.pi / 4),
    6: np.exp(1j * 6 * np.pi / 4),
    7: np.exp(1j * 7 * np.pi / 4)
}


# def modulate_8psk(symbol: np.uint8) -> np.complex128:
#     # encode a symbol into 8-PSK constellation point
#     return setup.power * constellation[symbol]

def modulate_8psk(symbols: np.ndarray) -> np.ndarray:
    # encode symbols into 8-PSK constellation points
    signal = np.zeros((symbols.size,), dtype=np.complex128)
    for i in range(symbols.size):
        signal[i] = setup.power * constellation[symbols[i]]
    return signal

# def modulate_8psk_gray(symbol: np.uint8) -> np.complex128:
#     # encode a symbol into 8-PSK constellation point
#     # using graycode
#     return setup.power * constellation[gray.gray_to_bin(symbol)]


def modulate_8psk_gray(symbols: np.ndarray) -> np.ndarray:
    # encode symbols into 8-PSK constellation points
    # using graycode
    signal = np.zeros((symbols.size,), dtype=np.complex128)
    for i in range(symbols.size):
        signal[i] = setup.power * constellation[gray.gray_to_bin(symbols[i])]
    return signal
