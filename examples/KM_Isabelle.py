# -*- coding: utf-8 -*-

import sys
sys.path.insert(1, "/home/arthur/Dropbox/python")

import numpy as np 
import matplotlib.pyplot as plt
from diltools import *

fig, ax = plt.subplots()

fname = "2_Isabelle_CQ60_Homogeneizado_30min_06.06.17.asc"
dat = load_asc_file(fname)
bd = BahrData(dat)
q = find_quenching_step(bd)
T, f = get_f_transf(q, [500,700], [0,200])
ax.plot(T[::10], f[::10], 'ks', mfc="none", label=format_long_string(fname,30))

beta, Ms = KM_fit(T, f, frng=[.2, 1.], p0=[.033,357.])
T, f_fit = eval_KM_fit(beta, Ms, T, f, frng=[.2, 1.])
ax.plot(T, f_fit, "b-", label=format_KM_equation(beta, Ms))

fname = "03_Isabelle_CQ60_Homogeneizado_30min_II_09.01.17.asc"
dat = load_asc_file(fname)
bd = BahrData(dat)
q = find_quenching_step(bd)
T, f = get_f_transf(q, [500,700], [0,200], True)
ax.plot(T[::10], f[::10], 'ko', mfc="none", label=format_long_string(fname,30))

beta, Ms = KM_fit(T, f, frng=[.2, 1.], p0=[.033,357.])
T, f_fit = eval_KM_fit(beta, Ms, T, f, frng=[.2, 1.])
ax.plot(T, f_fit, "r-", label=format_KM_equation(beta, Ms))

ax.set_xlabel(u"Temperatura (°C)")
ax.set_ylabel(u"Fração transformada de martensita")

ax.legend()
plt.show()
