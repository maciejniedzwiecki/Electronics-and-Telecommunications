# additive noise
# there are too many SNR definitions, therefore we're
# basing on https://sites.ualberta.ca/~msacchi/SNR_Def.pdf

import numpy as np
import setup

# def noise(variance: float = setup.variance) -> np.complex128:
#     # add noise to a point on the complex plane
#     noise = np.random.normal(0, np.sqrt(variance/2)) + 1j* np.random.normal(0, np.sqrt(variance/2))
#     return noise


def noise(signal: np.ndarray, snr: float = setup.snr) -> np.complex128:
    # add noise to points on the complex plane
    snr = setup.snr
    noisy_signal = np.zeros((signal.size,), dtype=np.complex128)
    snr_lin = np.power(10, (snr/10))
    Ps = (1/signal.size) * np.sum(np.square(signal))
    variance = np.absolute(Ps/snr_lin)
    for i in range(signal.size):
        noise = np.random.normal(0, np.sqrt(variance/2)) + \
            1j * np.random.normal(0, np.sqrt(variance/2))
        noisy_signal[i] = signal[i] + noise

    return noisy_signal
