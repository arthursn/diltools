# -*- coding: utf-8 -*-

import numpy as np


def smooth_derivative(x, y, window=1):
    n = len(x)
    if n != len(y):
        raise Exception('Lengths of x and y differ')
    if window < 1:
        raise Exception('Invalid value for window')

    yy = np.full(n, np.nan)
    for i in range(window, n-window+1):
        p = np.polyfit(x[i-window:(i+window)], y[i-window:(i+window)], 1)
        yy[i] = p[0]

    return x, yy
