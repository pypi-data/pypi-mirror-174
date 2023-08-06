"""
Created on Fri Nov 19 12:16:08 2021
@author: Siamak Khatami
@Email: siamak.khatami@ntnu.no
@License: https://creativecommons.org/licenses/by-nc-sa/4.0/
          Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
@Source: https://github.com/copatrec
@Document: https://github.com/copatrec
@WebApp: copatrec.org
@Cite:
"""


class CST:
    def __init__(self):
        pass

    Panel = 'Panel'
    Time_Series = 'Time_Series'
    Cross_Sectional = 'Cross_Sectional'
    Beta_Method = 'beta'
    Normal_Method = 'normal'
    IQR_Method = 'IQR'

    #  Data Types
    DataType_Series = 'Series'
    Outliers = 'outliers'

    #  Plots
    Hist_title = "Variable: {} | Method: {} \n " \
                 "Analysis Type:{} | Time: {} | Category: {}"
    Pair_interval_title = "Outlier analysis based on {method}\n" \
                          "{analysis_type} analysis | " \
                          "Borders contain {alpha:.3f} of the data."

    #  General Strings
    ALL = 'ALL'
    Cat = 'Category_{}'
    Time = 'Time_{}'
    Github_URL = "https://github.com/copatrec/copatrec"
    Note = "Note: "
    Statistic = "Statistic: "
    P_val = "p_value:"


class Warns:
    def __init__(self):
        pass
    W101 = "It is highly recommended to drop outliers by an expert of the field."
    W102 = "Analysis error: The number of observations are less than 10."
    W103 = "All X values here should be standardized if the model is generated using standardized values."
    #  Result Messages
    R101 = "Fitted. Model SE: {}"
    R102 = "Done"

    #  Progress
    P101 = "Finding outliers for a {} analysis, Method:{}"
    P102 = "Outliers processed."

    #  Equation Forms
    EF101 = 'Warning: Here xb equation Represents tanh.'

    # Result object warnings
    S100 = 'The optimal regression is selected based on the smallest SE. ' \
           'However, the unit of SE is same as variable unit.' \
           'In the case of standardization, SE becomes ' \
           'Dimensionless quantity as well ad thus has a range ' \
           'between 0 and 1.'

    S101 = 'Standard error of regression can be used to evaluate' \
           ' linear and nonlinear regressions and is valid if it is less' \
           ' than the desired significance level. SE is the primary evaluation' \
           ' criteria for best-fitted models.'

    S102 = 'The Normal test uses Skewness and kurtosis to evaluate' \
           ' whether estimation errors are distributed Normally around' \
           ' zero. "Error Normal Test" uses using p-value, which means' \
           '  "There is (not) enough evidence to claim errors are normally' \
           ' distributed" and should not be used alone to accept or reject' \
           ' the functionality of a model. '


class Errs:
    def __init__(self):
        pass
    E000 = ""
    Ignore = "ignore"
    #  Basic Errors
    E101 = "RuntimeError"
    #  Package Errors
    E201 = "Cannot fit none of equation forms."
    E202 = "Cannot find any fitted function to plot."
    E203 = "All rows are null value and dropped."
    E204 = "All rows are outlier values and dropped."
    E205 = "Cannot convert data to numerical data type."
    E206 = "No intervals and values for (X={x}, Y={y}) pairs " \
           "in category = {c} and time = {t}.\n" \
           "This mostly happens if all items are 0 or None."
    E207 = "All rows are null/zero value and dropped for " \
           "variable = {}, category = {} and time = {}."
    E208 = "{} intervals could not been calculated. \n {}"
    E209 = "Cannot calculate SE_Params and T values."
