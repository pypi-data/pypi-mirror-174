# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 11:39:18 2021

@author: Siamak Khatami
@Email: siamak.khatami@ntnu.no
@License: https://creativecommons.org/licenses/by-nc-sa/4.0/
          Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
@Source: https://github.com/copatrec
@document: https://github.com/copatrec
@Cite:
"""
import numpy as np


class _EquFuncs:
    def __init__(self):
        pass

    @staticmethod
    def sin(x, a, b, c, d):
        return a + (b * np.sin((c * x) + d))

    @staticmethod
    def cos(x, a, b, c, d):
        return a + (b * np.cos((c * x) + d))

    @staticmethod
    def tan(x, a, b, c, d):
        return a + (b * np.tan((c * x) + d))

    @staticmethod
    def sinh(x, a, b, c):
        return a * np.sinh((b * x) + c)

    @staticmethod
    def cosh(x, a, b, c):
        return a * np.cosh((b * x) + c)

    @staticmethod
    def tanh(x, a, b, c):
        return a * np.tanh((b * x) + c)

    @staticmethod
    def lnx(x, a, b, c):
        return a + (b * np.log(c * x))

    @staticmethod
    def logx(x, a, b, c):
        return a + (b * np.log10(c * x))

    @staticmethod
    def euler_exp(x, a, b, c):
        return a + (b * np.exp(c * x))

    @staticmethod
    def exp(x, a, b, c, d, e):
        return a + (b * np.power(c, (d * x) + e))

    @staticmethod
    def logistic(x, a, b, c, d, e):
        return a / (b + (c * np.exp(d + (e * x))))

    @staticmethod
    def polynomial(x, a, b, c):
        return a + (b * np.power(x, c))

    @staticmethod
    def oscillating_growth(x, a, b, c, d, e, f, g, h, i, j):
        f1 = b * np.power(np.sin(c*np.power(x, d) + e), f)
        f2 = g / (h + np.exp(i + (j * x)))
        f3 = 1 / (1 + np.exp(-1 * x))
        f4 = 1 / (1 + np.exp(x))
        return a + (f1 * f3) + (f2 * f4)

    @staticmethod
    def double_gaussian(x, a, b, c, d, e, f):
        """
        Single Gaussian has one mean but the Double has two means. However,
        having two single and double is useless because single is a special
        form of double Gaussian.

        Parameters
        ----------
        x : Independent Variable \n
        d : Larger Mean \n
        e: Smaller Mean \n
        f : Standard Deviation \n
        a: interception \n
        b: smaller mean Coefficient \n
        c: Larger Mean Coefficient \n
        ----------

        :returns:
        double_gaussian Distribution results \n
        The aim is not to draw a distribution, but to use it to fit Curve
        to see overshot and collapse behavior.
        """
        divider = f * np.sqrt(2 * np.pi)
        y1 = b / divider
        y2 = np.exp(-1 * np.power((x - d) / (2 * f), 2))
        y3 = c / divider
        y4 = np.exp(-1 * np.power((x-e) / (2 * f), 2))
        return a + y1*y2 + y3*y4


class _EquPatterns:

    def __init__(self):
        pass

    @staticmethod
    def sin(popt):
        str_equ = "{0} + ({1} * sin({2}x + {3}))".format(*popt)
        latex_equ = r"${0} + ({1} * \sin({2}x + {3}))$".format(*popt)
        return str_equ, latex_equ

    @staticmethod
    def sinh(popt):
        str_equ = "{0} * sinh({1}x + {2})".format(*popt)
        latex_equ = r"${0} * \sinh({1}x + {2})$".format(*popt)
        return str_equ, latex_equ

    @staticmethod
    def cos(popt):
        str_equ = "{0} + ({1} * cos({2}x + {3}))".format(*popt)
        latex_equ = r"${0} + ({1} * \cos({2}x + {3}))$".format(*popt)
        return str_equ, latex_equ

    @staticmethod
    def cosh(popt):
        str_equ = "{0} * cosh({1}x + {2})".format(*popt)
        latex_equ = r"${0} * \cosh({1}x + {2})$".format(*popt)
        return str_equ, latex_equ

    @staticmethod
    def tan(popt):
        str_equ = "{0} + ({1} * tan({2}x + {3}))".format(*popt)
        latex_equ = r"${0} + ({1} * \tan({2}x + {3}))$".format(*popt)
        return str_equ, latex_equ

    @staticmethod
    def tanh(popt):
        str_equ = "{0} * tanh({1}x + {2})".format(*popt)
        latex_equ = r"${0} * \tanh({1}x + {2})$".format(*popt)
        return str_equ, latex_equ

    @staticmethod
    def euler_exp(popt):
        str_equ = "{0} + ({1} * e^({2}x))".format(*popt)
        latex_equ = r"${0} + ( {1} + e^{{({2}x)}} )$".format(*popt)
        return str_equ, latex_equ

    @staticmethod
    def logistic(popt):
        str_equ = "{0} / ({1} + ( {2} * e^({3} + {4}x)))".format(*popt)
        latex_equ = r"$\frac{{ {0} }}{{ {1} + ({2} * e^{{ {3} + {4}x }}) }}$".format(*popt)
        return str_equ, latex_equ

    @staticmethod
    def lnx(popt):
        str_equ = "{0} + ({1} * ln({2}x))".format(*popt)
        latex_equ = r"${0} + ({1} * \ln({2}x))$".format(*popt)
        return str_equ, latex_equ

    @staticmethod
    def logx(popt):
        str_equ = "{0} + ({1} * log({2}x))".format(*popt)
        latex_equ = r"${0} + ({1} * \log({2}x))$".format(*popt)
        return str_equ, latex_equ

    @staticmethod
    def polynomial(popt):
        str_equ = "{0} + ({1} * x^({2}))".format(*popt)
        latex_equ = r"${0} + ({1} * x^{{ {2} }})$".format(*popt)
        return str_equ, latex_equ

    @staticmethod
    def exp(popt):

        str_equ = "{0} + ({1} * {2}^(({3} * x) + {4}))".format(*popt)
        latex_equ = r"${0} + ({1} * {2}^{{ ({3}x) + {4} }})$".format(*popt)
        return str_equ, latex_equ

    @staticmethod
    def oscillating_growth(popt):
        str_equ = "{0} + ({1} * sin(({2} * x^({3})) + {4})^({5}) *" \
                  " 1 / (1 + e^(-x))) + ({6} / ({7} + e^({8} + ({9}x))) * 1 / (1 + e^(x)))".format(*popt)

        latex_equ = r"${0} + " \
                    r"({1} * \sin( ({2}x^{{ {3} }}) + {4} )^{{ {5} }}) * " \
                    r"(\frac{{ 1 }}{{(1 + e^{{ -x }} )}}) + " \
                    r"(\frac{{ {6} }}{{ ({7} + e^{{ {8} + ({9}x) }}) }}) * " \
                    r"(\frac{{ 1 }}{{(1 + e^{{ x }} )}})$".format(*popt)
        return str_equ, latex_equ

    @staticmethod
    def double_gaussian(popt):
        str_equ = "{0} + " \
                  "({1} / ({5} * sqrt(2pi)) )*" \
                  "e^(-1 * ( (x - {3}) / (2 * {5}) )^2 ) + " \
                  "({2} / ( {5} * sqrt(2pi) ) )*" \
                  "(e^(-1 * ((x-{4}) / (2 * {5}))^2))".format(*popt)

        latex_equ = r"${0} +  " \
                    r"(\frac{{ {1} }}{{ {5}\sqrt{{ 2\pi}} }}) * " \
                    r"( e^{{ -(\frac{{ x - {3} }}{{ 2*{5}) }})^{{2}} }}) + " \
                    r"(\frac{{ {2} }}{{ {5}\sqrt{{ 2\pi}} }} ) * " \
                    r"( e^{{ -(\frac{{ x - {4} }}{{ 2*{5} }})^{{2}} }})$".format(*popt)
        return str_equ, latex_equ
