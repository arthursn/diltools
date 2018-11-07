# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from diltools import *


fname = "01_Pierre_CCT_0,15oCs-1_01.31.18.asc"
bd = BahrData(load_asc_file(fname))

fig, ax = plt.subplots()
for n in [2, 5, 10, 20]:
    ax.plot(*smooth_derivative(bd.T, bd.dll0, n), label='n = {}'.format(n))
ax.set_xlabel(u'Temperature (°C)')
ax.set_ylabel(r'$\frac{{d (\Delta l / l0)}}{{d T}}$' + u' (%/°C)')
ax.legend()
fig.tight_layout()

#########

fig, ax1 = plt.subplots()
ax1.plot(bd.T, bd.dll0, 'k-', label=r'$\Delta l / l0$')

ax2 = ax1.twinx()
ax2.plot(*smooth_derivative(bd.T, bd.dll0, 10), 'r-', label=r'$\frac{{d (\Delta l / l0)}}{{d T}}$')

ax1.set_xlabel('Temperature (°C)')
ax1.set_ylabel(r'$\Delta l / l0$' + u' (%)')
ax2.set_ylabel(r'$\frac{{d (\Delta l / l0)}}{{d T}}$' + u' (%/°C)')

fig.tight_layout()

plt.show()
