# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from builtins import open


class BahrData(object):
    """
    l0 in the same units as dl (um)
    """

    def __init__(self, data, l0=None):
        self.index = []
        self.t = []
        self.dl = []
        self.dll0 = []
        self.T = []
        self.Tnom = []
        self.alpha = []
        self.l0 = l0

        self.p = []

        self.data = data

    def __getitem__(self, item):
        return self.data[item]

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

        keys = self._data.keys()
        
        if 'index' in keys:
            self.index = np.array(self._data['index'])
        if 'time' in keys:
            self.t = np.array(self._data['time'])
        if 'time.s' in keys:
            self.t = np.array(self._data['time.s'])

        if 'change in length' in keys:
            self.dl = np.array(self._data['change in length'])
        
        if 'rel. change in length' in keys:
            self.dll0 = 1e-2*np.array(self._data['rel. change in length'])
        if 'dl.pct' in keys:
            self.dll0 = 1e-2*np.array(self._data['dl.pct'])
        
        if self.l0:
            if len(self.dll0) == 0:
                self.dll0 = self.dl/self.l0
            elif len(self.dl) == 0:
                self.dl = self.dll0*self.l0

        if 'temperature' in keys:
            self.T = np.array(self._data['temperature'])
        if 'TC1' in keys:
            self.T = np.array(self._data['TC1'])
        if 'sample temperature' in keys:
            self.T = np.array(self._data['sample temperature'])
        if 'nominal temperature' in keys:
            self.Tnom = np.array(self._data['nominal temperature'])
        
        if 'alpha' in keys:
            self.alpha = np.array(self._data['alpha'])

    def get_alpha(self, T0, T1, deg=2, **kwargs):
        sel = kwargs.get('sel', range(len(self.T)))
        l0 = kwargs.get('l0', self.l0)

        if len(self.dll0) > 0:
            self.p = np.polyfit(self.T[sel], self.dll0[sel]/100., deg=deg)
            alpha = (np.polyval(self.p, T1) - np.polyval(self.p, T0))/(T1 - T0)
        else:
            if l0:
                self.p = np.polyfit(self.T[sel], self.dl[sel], deg=deg)
                alpha = (np.polyval(self.p, T1) - np.polyval(self.p, T0))/(l0*(T1 - T0))
            else:
                raise Exception('l0 not provided')

        return alpha

    def split_segments(self):
        if len(self.Tnom) > 0:
            isiso = np.diff(self.Tnom) == 0
            splitseg, = np.where(isiso[:-1] != isiso[1:])
            splitseg += 1
            dflist = np.split(self.data, splitseg)
            return [BahrData(df, self.l0) for df in dflist]


def load_asc_file(fname):
    """
    Load Bahr asc file

    Parameters
    ----------
    fname : str
        File name

    Returns
    -------
    Pandas DataFrame with structured data
    """
    columns = []
    data = []

    with open(fname, errors='ignore') as f:
        line = f.readline()  # reads first line
        line = line.strip('#')
        filelocation = line.strip()

        line = f.readline()  # reads second line
        line = line.strip('#')
        line = line.strip()
        line = line.split('-')

        # reads the column names
        columns = [col.strip().lower() for col in line[1].split('/')]
        columns.insert(0, line[0].strip().lower())
        columns.insert(0, 'index')

        # number of columns expected
        ncol = len(columns)

        # reads data
        for line in f:
            try:
                arr = list(map(float, line.split()))
                if len(arr) == ncol:
                    data.append(arr)
            except:
                pass

    return pd.DataFrame(data=data, columns=columns)

def get_segments_by_temperature_range(bd, Trng):
    """
    Split BahrData into chunks of data for a given temperature interval

    Parameters
    ----------
    bd: BahrData object
        Dilatometry data
    Trng: list
        Temperature interval for selection

    Returns
    -------
    List of BahrData objects corresponding to all segments fulfilling
    the temperature range
    """
    Trng = sorted(Trng)
    sel = (bd.T >= Trng[0]) & (bd.T <= Trng[1])  # selection

    ind, = np.where(sel)
    spl, = np.where(np.diff(ind) > 1)
    spl += 1

    df_grp = np.split(bd.data[sel], spl)  # split dataframe selection

    return [BahrData(df, bd.l0) for df in df_grp]