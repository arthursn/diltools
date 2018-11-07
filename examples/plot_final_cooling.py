# -*- coding: utf-8 -*-

import glob
import numpy as np
import matplotlib.pyplot as plt
from diltools import *

def isint(s):
    try:
        int(s)
    except:
        return False
    return True

fname = '01_Isabelle_QP_Q328oC_P350oC_t10s_09.28.17.asc'
bd = BahrData(load_asc_file(fname))  # Pandas DataFrame loaded from asc file

bd500 = get_segments_by_temperature_range(bd, [0, 500])[-1]  # BahrData for temperatures below 500 oC
plt.plot(bd500.T, bd500.dll0 - bd500.dll0[0])

bd350 = get_segments_by_temperature_range(bd, [300, 350])[-1]  # BahrData for temperatures between 300 and 350 oC
p = np.polyfit(bd350.T, bd350.dll0, 1)
x = [0, 350.]
y = np.polyval(p, x)
plt.plot(x, y - bd500.dll0[0], 'k--')

plt.xlim(0, 500.)
plt.xlabel(u'Temperature (°C)')
plt.ylabel(u'Relative change in length (%)')
plt.tight_layout()
plt.show()
plt.close()