# -*- coding: utf-8 -*-

def format_KM_equation(beta, Ms):
    return r"$1 - \exp[-{}({:.1f} - T)]$".format(latex_sci_not(beta,4), Ms)

def latex_sci_not(number, dec=4):
    """
    Formats a number into scientific notation in LaTeX format
    """
    m, n = "{:.{}e}".format(number, dec).split("e")
    return r"{} \times 10^{{{:d}}}".format(m, int(n))

def format_long_string(string, size):
    if len(string) > size:
        string = "{}...".format(string[:size])
    return string
