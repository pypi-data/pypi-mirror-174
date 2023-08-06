'''
Skewness of the Number of e-folds
---------------------------------
This module calculates the skewness of the number of e-folds in low diffusion
limit using equation 3.37 (from `Vennin--Starobinsky 2015`_) for the third
central moment and equation 3.33 for the variance.

.. _Vennin--Starobinsky 2015: https://arxiv.org/abs/1506.04732
'''


import numpy as np
from scipy import integrate

from .reduced_potential import reduced_potential
from .reduced_potential_diff import reduced_potential_diff
from .reduced_potential_ddiff import reduced_potential_ddiff
from .variance_efolds import variance_efolds

planck_mass = 1


# Equation 3.37 in Vennin 2015, then divded by sigma^3 to make skewness
def skewness_efolds(potential, potential_dif, potential_ddif, phi_i, phi_end):
    """Returns the skewness of the number of e-folds.

    Parameters
    ----------
    potential : function
        The potential.
    potential_dif : function
        The potential's first derivative.
    potential_ddif : function
        The potential's second derivative.
    phi_i : float
        The initial scalar field value.
    phi_end : float
        The end scalar field value.

    Returns
    -------
    skewness_efolds : float
        the skewness of the number of e-folds.

    """
    v_func = reduced_potential(potential)
    v_dif_func = reduced_potential_diff(potential_dif)
    v_ddif_func = reduced_potential_ddiff(potential_ddif)

    def integrand_calculator(phi):
        # Pre calculating values
        v = v_func(phi)
        v_dif = v_dif_func(phi)
        v_ddif = v_ddif_func(phi)
        non_classical = 14*v-np.divide(11*(v**2)*v_ddif, v_dif**2)
        constant_factor = 12/(planck_mass**6)

        integrand = constant_factor*np.divide(v**7, v_dif**5)*(1+non_classical)
        return integrand
    skewness_value, er = integrate.quad(integrand_calculator, phi_end, phi_i)
    # Now normalise by the variance
    skewness_efolds =\
        skewness_value/variance_efolds(potential, potential_dif,
                                       potential_ddif, phi_i, phi_end)**1.5

    return skewness_efolds
