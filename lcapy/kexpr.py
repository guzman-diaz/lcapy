"""This file provides the kExpr class to represent k-domain (discrete Fourier
domain) expressions.

Copyright 2020 Michael Hayes, UCECE

"""

from __future__ import division
from .fourier import inverse_fourier_transform
from .functions import exp
from .sym import j, oo, pi
from .dexpr import dExpr
from .dsym import nsym, ksym, zsym
import sympy as sym


class kExpr(dExpr):

    """Fourier domain expression or symbol."""

    var = ksym
    domain_name = 'Frequency'
    domain_units = 'Hz'

    def __init__(self, val, **assumptions):

        assumptions['real'] = True
        check = assumptions.pop('check', True)
        
        super(kExpr, self).__init__(val, **assumptions)
        # Define when class defined.
        self._fourier_conjugate_class = nexpr

        expr = self.expr

        if check and expr.find(zsym) != set():
            raise ValueError(
                'k-domain expression %s cannot depend on z' % self.expr)
        if check and expr.find(nsym) != set() and not expr.has(sym.Sum):
            raise ValueError(
                'k-domain expression %s cannot depend on n' % self.expr)

    def plot(self, kvector=None, **kwargs):
        """Plot frequency response at values specified by kvector.  If kvector
        is a tuple, this sets the frequency limits.

        kwargs include:
        axes - the plot axes to use otherwise a new figure is created
        xlabel - the x-axis label
        ylabel - the y-axis label
        ylabel2 - the second y-axis label if needed, say for mag and phase
        xscale - the x-axis scaling, say for plotting as ms
        yscale - the y-axis scaling, say for plotting mV
        plot_type -  'dB_phase', 'mag-phase', 'real-imag', 'mag', 'phase',
        'real', or 'imag'
        in addition to those supported by the matplotlib plot command.
        
        The plot axes are returned.

        There are many plotting options, see lcapy.plot and
        matplotlib.pyplot.plot.

        For example:
            V.plot(kvector, log_frequency=True)
            V.real.plot(kvector, color='black')
            V.phase.plot(kvector, color='black', linestyle='--')

        By default complex data is plotted as separate plots of magnitude (dB)
        and phase.

        """

        from .plot import plot_frequency
        return plot_frequency(self, kvector, **kwargs)

    def IDFT(self, N=None, evaluate=True):

        from .nexpr import n
        from sympy import Sum, summation

        if N is None:
            from .expr import expr
            from .sym import sympify
            
            N = sympify('N')

        foo = self.expr * exp(2 * j * pi * nsym * ksym / N) / N

        if evaluate:
            result = summation(foo, (ksym, 0, N))       
        else:
            result = Sum(foo, (ksym, 0, N))

        if hasattr(self, '_fourier_conjugate_class'):
            result = self._fourier_conjugate_class(result)
        else:
            result = nExpr(result, check=False)
            
        return result
    

class Yk(kExpr):

    """f-domain admittance"""

    quantity = 'Admittance'
    units = 'siemens'

    def __init__(self, val, **assumptions):

        super(Yk, self).__init__(val, **assumptions)
        self._fourier_conjugate_class = Yn


class Zk(kExpr):

    """f-domain impedance"""

    quantity = 'Impedance'
    units = 'ohms'

    def __init__(self, val, **assumptions):

        super(Zk, self).__init__(val, **assumptions)
        self._fourier_conjugate_class = Zn


class Hk(kExpr):

    """f-domain transfer function response."""

    quantity = 'Transfer function'
    units = ''

    def __init__(self, val, **assumptions):

        super(Hk, self).__init__(val, **assumptions)
        self._fourier_conjugate_class = Hn


class Vk(kExpr):

    """f-domain voltage (units V/Hz)."""

    quantity = 'Voltage spectrum'
    units = 'V/Hz'

    def __init__(self, val, **assumptions):

        super(Vk, self).__init__(val, **assumptions)
        self._fourier_conjugate_class = Vn


class Ik(kExpr):

    """f-domain current (units A/Hz)."""

    quantity = 'Current spectrum'
    units = 'A/Hz'

    def __init__(self, val, **assumptions):

        super(Ik, self).__init__(val, **assumptions)
        self._fourier_conjugate_class = In


def kexpr(arg):
    """Create kExpr object.  If `arg` is ksym return k"""

    if arg is ksym:
        return k
    return kExpr(arg)
        
from .nexpr import Hn, In, Vn, Yn, Zn, nexpr
k = kExpr('k')