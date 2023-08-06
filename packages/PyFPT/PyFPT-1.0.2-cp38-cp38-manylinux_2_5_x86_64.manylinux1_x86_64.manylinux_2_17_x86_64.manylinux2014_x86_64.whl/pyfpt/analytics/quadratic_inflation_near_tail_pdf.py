'''
Quadratic Inflation Near Tail PDF
----------------------------------
This module calculates the near tail of the probability density function (PDF)
for first-passage time of the number of e-folds for quadratic inflation in the
large mass case. The large mass case corresponds to diffusion domination. This
is done using the results of appendix in `<insert our paper>`_, and therefore
assumes UV cutoff at infinity.

.. _<insert our paper>: https://arxiv.org/abs/1707.00537
'''

import numpy as np
from scipy import integrate

pi = np.pi
planck_mass = 1


def quadratic_inflation_near_tail_pdf(efolds, m, phi_in, phi_end=2**0.5,
                                      numerical_integration=False):
    """Returns PDF of quadratic inflation for the near tail.

    Parameters
    ----------
    efolds : list
        The first-passage times where the PDF is to be calculated.
    m : float
        The mass of quadratic inflation potential.
    phi_in : float
        The initial field value.
    phi_end : float, optional
        The end scalar field value. Defaults to value such that the first
        slow-roll parameter is 1.
    numerical_integration : bool, optional
        If numerical integration is used.

    Returns
    -------
    pdf : list
        The probability density function at e-folds values.

    """
    v0 = (m**2)/(48*pi**2)
    v = v0*phi_in**2
    efolds_cl = 0.25*phi_in**2-0.25*phi_end**2
    ve = v0*phi_end**2
    if numerical_integration is False:

        # Calculating the terms individually for clarity
        constant = (np.sqrt(2)*pi**2)/(128*v0**2)
        exp = np.exp(-0.25*v0*efolds)

        frac_expo_i = np.divide(pi**2, 16*v0*(efolds+efolds_cl+1))
        fraction_i =\
            np.divide(np.exp(frac_expo_i-1/v)*v**1.5, (efolds+efolds_cl+1)**3)

        frac_expo_end = np.divide(pi**2, 16*v0*(efolds-efolds_cl+1))
        fraction_end = np.divide(np.exp(frac_expo_end-1/ve)*ve**1.5,
                                 (efolds-efolds_cl+1)**3)

        pdf = constant*exp*(fraction_i - fraction_end)

    elif numerical_integration is True:
        a1 = 0.25*v0*efolds + 0.0625*(v+ve)
        a2 = 0.25*v0*efolds + 0.0625*(3*ve-v)

        def g(x, a):
            return np.exp(0.25*pi*x-a*x**2)*x**(5/2)

        ga1_int, _ = integrate.quad(g, 3, np.infty, args=(a1))
        ga2_int, _ = integrate.quad(g, 3, np.infty, args=(a2))

        first_term = np.exp(-1/v)*ga1_int*v**1.5
        second_term = np.exp(-1/ve)*ga2_int*ve**1.5
        pdf = v0*np.exp(-0.25*v0*efolds)*(first_term-second_term)/(32*pi)
    return pdf
