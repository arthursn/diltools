import numpy as np
import matplotlib.pyplot as plt

class ThermoProperties(object):
    """
    Qiu, C. & Zwaag, S. Van Der. Dilatation measurements of plain carbon steels and their thermodynamic analysis. Steel Res. Int. 68, 32–38 (1997)
    """
    def __init__(self, A0, alpha0, alpha1, kappa0, kappa1, n):
        self.A0 = A0
        self.alpha0 = alpha0
        self.alpha1 = alpha1
        self.kappa0 = kappa0
        self.kappa1 = kappa1
        self.n = n

    def Vm(self, T, P):
        return self.A0*np.exp(self.alpha0*T + .5*self.alpha1*T**2.)/(1 + self.n*P*(self.kappa0 + self.kappa1*T))**(1./self.n)

    def DVV0(self, T, P, T0=0.):
        V0 = self.Vm(T0, P) 
        return (self.Vm(T, P) - V0)/V0


bcc = ThermoProperties(7.042095e-6, 2.3987e-5, 2.569e-8, 5.965e-12, 6.5152e-17, 4.7041)
fcc = ThermoProperties(6.688726e-6, 7.3097e-5, 0, 6.2951e-12, 6.5152e-17, 5.1665)
cem = ThermoProperties(23.39e-6, -1.36e-5, 8.0e-8, 0, 0, 1)

# T = np.arange(0, 2000)

# plt.plot(T, bcc.Vm(T, P), label='Ferrite')
# plt.plot(T, fcc.Vm(T, P), label='Austenite')
# plt.plot(T, cem.Vm(T, P), label='Cementite')
# plt.plot(T, bcc.DVV0(T, P), label='Ferrite')
# plt.plot(T, fcc.DVV0(T, P), label='Austenite')
# plt.plot(T, cem.DVV0(T, P), label='Cementite')
# plt.legend(loc='best')
# plt.show()


import tctools as tt
files = ['/home/arthur/Dropbox/{Shared} Lucas/Thermo-Calc/Trilhos/NP_HC.TXT',
         '/home/arthur/Dropbox/{Shared} Lucas/Thermo-Calc/Trilhos/NP_S1.TXT',
         '/home/arthur/Dropbox/{Shared} Lucas/Thermo-Calc/Trilhos/NP_NIPPON.TXT']
labels = ['HC', 'S1', 'Nippon']

for fname, lbl in zip(files, labels):
    data = tt.load_table(fname, sort=0)

    Ts = []
    Vs = []
    P = 101325.
    V0 = data[0,1]*bcc.Vm(25, P) + data[0,3]*cem.Vm(25, P)/4.
    for line in data:
        T, npbcc, npfcc, npcem = line
        V = npbcc*bcc.Vm(T, P) + npfcc*fcc.Vm(T, P) + npcem*cem.Vm(T, P)/4.
        
        Ts.append(T)
        Vs.append((V-V0)/V0)
        # Vs.append(V)

    plt.plot(np.array(Ts)-273.15, Vs, label=lbl)

# plt.xlim(680, 800)
plt.legend(loc='best')
plt.show()