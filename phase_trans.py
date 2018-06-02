# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

from .bahr_data import BahrData, get_segments_by_temperature_range

def get_f_transf(bd, rng1, rng2, plot=False):
    """
    Performs lever rule and calculates transformed fraction

    Parameters
    ----------
    bd: BahrData instance
        Dilatometry data as loaded by load_asc_file function
    rng1: list length 2
        Temperature range delimiting linear expansion segment before 
        transformation has begun
    rgn2: list length 2
        Temperature range delimiting linear expansion segment after
        transformation has finished
    plot: boolean, optional
        If true, plots raw data and linear regressions for rng1 and rng2

    Returns
    -------
    T, f: tuple
        Returns tuple of numpy arrays representing the temperature T and the
        transformed fraction f. The range of temperatures of the returned
        arrays corresponds to halfway of rng1 to halfway of rng2, i.e.,
        (rng1[0]+rng1[1])/2 <= T <= (rng2[0]+rng2[1])/2

    """
    m1, m2 = np.mean(rng1), np.mean(rng2)
    rng = (bd.T >= min(m1,m2)) & (bd.T <= max(m1,m2))
    rng1 = (bd.T >= min(rng1)) & (bd.T <= max(rng1))
    rng2 = (bd.T >= min(rng2)) & (bd.T <= max(rng2))
    
    dil = bd.dl
    if len(dil) == 0:
        dil = bd.dll0
    p1 = np.polyfit(x=bd.T[rng1], y=dil[rng1], deg=1)
    p2 = np.polyfit(x=bd.T[rng2], y=dil[rng2], deg=1)

    dl1 = np.polyval(p=p1, x=bd.T)
    dl2 = np.polyval(p=p2, x=bd.T)

    if plot:
        fig, ax = plt.subplots()
        ax.plot(bd.T, dil, "k-", label="raw")
        ax.plot(bd.T, dl1, "r-", label="fit rng1")
        ax.plot(bd.T, dl2, "b-", label="fit rng2")
        ax.set_xlabel("T")
        ax.set_ylabel("dl")
        ax.legend()
        fig.show()

    f = (dil - dl1)/(dl2 - dl1)
    
    return bd.T[rng], f[rng]

def find_quenching_step(bd, dT=1.):
    """
    Finds segment corresponding to quenching step

    Parameters
    ----------
    bd: BahrData object
        Dilatometry data as loaded by load_asc_file function
    dT: float, optional
        Deviation from the maximum temperature considered by the algorithm
        to find the beginning of the quenching step; default: 1.0

    Returns
    -------
    BahrData object containing segment of data corresponding to quenching step

    """
    Tmax = np.max(bd.T)
    Trng = [-np.inf, Tmax - dT]
    return get_segments_by_temperature_range(bd, Trng)[-1]

def KM(T, beta, Ms):
    """
    Koistinen-Marburger equation
    """
    return 1 - np.exp(-beta*(Ms - T))

def KM_fit(T, f, frng=[.05, 1.], p0=None, **kwargs):
    """
    Fits f vs T curve using KM equation as model
    """
    sel = (f >= min(frng)) & (f <= max(frng))
    (beta, Ms), pcov = curve_fit(f=KM, xdata=T[sel], ydata=f[sel], p0=p0, **kwargs)
    return beta, Ms

def eval_KM_fit(beta, Ms, T, f, frng=[.05, 1.]):
    sel = (f >= min(frng)) & (f <= max(frng))
    return T[sel], KM(T[sel], beta, Ms)
