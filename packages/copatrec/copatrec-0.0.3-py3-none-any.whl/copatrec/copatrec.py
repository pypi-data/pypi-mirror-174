# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 12:03:18 2021
@author: Siamak Khatami
@Email: siamak.khatami@ntnu.no
@License: https://creativecommons.org/licenses/by-nc-sa/4.0/
@Source: https://github.com/copatrec
@Document: https://github.com/copatrec
@WebApp: copatrec.org
@Cite:
"""
import inspect
import logging as lg
import os
import warnings
import string
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random as rnd
import scipy.stats as sts
from scipy.optimize import curve_fit
from sklearn.preprocessing import MinMaxScaler

try:
    #  If package is cloned.
    from src.math.patterns import _EquFuncs, _EquPatterns
    from src.summary.summary import Summary
    from src.constants.constants import CST, Warns, Errs
except ImportError:
    #  If package is installed
    from copatrec.math.patterns import _EquFuncs, _EquPatterns
    from copatrec.summary.summary import Summary
    from copatrec.constants.constants import CST, Warns, Errs

class Copatrec:
    def __init__(self,
                 data: pd.DataFrame,
                 dependent_var: str,
                 time_col: str = "",
                 category_col: str = "",
                 report: bool = True,
                 report_to_file: bool = False
                 ):
        """
        COPATREC initializer function
        :param data:
        :type: pd.DataFrame
        :param dependent_var: The column name in the dataframe which represents dependent variable.
        :type: str
        :param time_col:  The column name in the dataframe which represents time information.
        :type: str
        :param category_col: The column name in the dataframe which represents categories names.
        :type: str
        :param report: whether to report the process or not.
        :type: bool
        :param report_to_file: Whether to print report into a file (True) or in the Terminal(False)
        The default value is False.
        :type: bool
        """
        #   Initialization
        self.__EquFuncs = _EquFuncs  # saving _EquFuncs class into a class object.
        self.__EquPatterns = _EquPatterns  # saving _EquFuncs class into a class object.

        # List of functions which are used in the analysis process.
        self.Models = [_EquFuncs.sin,
                       _EquFuncs.sinh,
                       _EquFuncs.cos,
                       _EquFuncs.cosh,
                       _EquFuncs.tan,
                       _EquFuncs.tanh,
                       _EquFuncs.lnx,
                       _EquFuncs.logx,
                       _EquFuncs.euler_exp,
                       _EquFuncs.exp,
                       _EquFuncs.logistic,
                       _EquFuncs.polynomial,
                       _EquFuncs.oscillating_growth,
                       _EquFuncs.double_gaussian
                       ]

        self.Data = data
        self.Time_col = time_col
        self.Category_col = category_col

        if not self.Category_col:  # A column name is added if there is no col
            # the default category name
            self.Category_col = CST.Cat.format(''.join(rnd.sample(string.ascii_lowercase, 5)))
            self.Data[self.Category_col] = 1  # the default value
        if not self.Time_col:  # A time name is added if there is no time col
            self.Time_col = CST.Time.format(''.join(rnd.sample(string.ascii_lowercase, 5)))  # Default time col name
            self.Data[self.Time_col] = 1  # Default value for the col
            #  for col in data[self.Category_col]:
            #       self.Data[self.Time_col].at[self.Data[self.Category_col] == col] = list(
            #       range(self.Data[self.Time_col].at[self.Data[self.Category_col] == col].shape[0]))
        self.Dependent_var = dependent_var
        self.Independent_var = [var for var in self.Data.columns if var not in [
            self.Time_col,
            self.Category_col,
            self.Dependent_var
        ]]  # All columns excepts dependent variable, time and category columns are counted as independent variable.
        self.__fix_data_types()  # Reformat data in the dataset.
        if report:
            args = {
                'level': lg.INFO,
                'format': '%(levelname)s - %(message)s',
                'filemode': 'w'
            }
            if report_to_file:
                caller_file_name = os.path.basename(inspect.stack()[1].filename).split('.')[0]
                args['filename'] = caller_file_name+'.log'
            lg.basicConfig(**args)
        else:
            lg.disable()

    def __fix_data_types(self):
        """
        This function changes the data type presented in the self.Data
        """
        all_vars = [col for col in self.Data.columns
                    if col not in [self.Time_col,
                                   self.Category_col]]  # Dependent and independent
        vars_type_dict = {self.Time_col: str,
                          self.Category_col: str}  # Changing time and category columns' data type
        for col in all_vars:
            vars_type_dict[col] = float

        self.Data = self.Data.astype(vars_type_dict)  # applying the defined dictionary of datatypes to the dataframe

    @staticmethod
    def __calc_mean_std(data: pd) -> \
            (pd.Series, pd.Series):
        """
        Calculates the mean and standard deviation of the Dataframe, GroupedDataFrame or Series
        :param data: A data either in Dataframe or Series type
        :Type: pd.DataFrame
        :return:
        Means | Standard deviations
        """
        var_groups_stats = data.describe()
        var_groups_means = var_groups_stats['mean']
        var_groups_std = var_groups_stats['std']
        return var_groups_means, var_groups_std

    @staticmethod
    def __alpha_beta(mean: float,
                     std: float) -> \
            (float, float):
        """
        Calculates the alpha and beta for the beta distribution based on the observed
        mean and standard deviation;
        :param mean: Mean of observed data set
        :type: float
        :param std: Standard deviation of the observed data set.
        :type: float
        :return: alpha| beta
        """
        lg.captureWarnings(True)

        n = (mean * (1 - mean)) / np.power(std, 2)
        alpha = mean * n
        beta = (1 - mean) * n
        # with warnings.catch_warnings():
        #       warnings.simplefilter("ignore")
        return alpha, beta

    @staticmethod
    def __beta_upper_lower(sl: float,
                           alpha: float,
                           beta: float) -> \
            (float, float):
        """
        Returns the intervals (lower, upper) for the Beta distribution
        based on the received parameters;
        :param sl: Significant level
        :type: float
        :param alpha: Alpha parameter of the beta distribution
        :param beta: beta parameter of the beta distribution
        :return: (lower band, upper band)
        """
        lower = sts.beta.ppf(sl / 2, alpha, beta)
        upper = sts.beta.ppf(1 - sl / 2, alpha, beta)
        return lower, upper

    @staticmethod
    def __normal_upper_lower(sl: float,
                             stats: pd) -> \
            (float, float):
        """
        Returns the intervals (lower, upper) for the Normal distribution
        based on the received parameters. Since the standard deviation of
        the real population is unknown, a two side T-distribution is used to find the
        intervals;
        :param sl: Significant level
        :type: float
        :param stats: statistical information related to the data
        :type: pd.Series
        :return: (lower band, upper band)
        """
        t_intervals = sts.t.interval(alpha=1 - sl,
                                     df=stats['count'],
                                     loc=stats['mean'],
                                     scale=stats['std'])

        lower = t_intervals[0]
        upper = t_intervals[1]
        return lower, upper

    @staticmethod
    def __iqr_upper_lower(sl: float,
                          values: np.array) -> \
            (float, float):
        """
        Returns the intervals (lower, upper) using the IQR(Inter-quartile range)
        based on the received parameters. Since the standard deviation of
        the real population is unknown, a two side T-distribution is used to find the
        intervals;
        In this function, instead of having scipy function, a more dynamic approach is used.
        The IQR function in Matplot, seaborn and scipy use 1.5 * IQR point. The number 1.5 in that
        formula is the result of normal ppf based on the confidence level (1 - sl) where sl is
        approximate 5%.
        To make it better, instead of using 1.5, ppf is used. Thus, it is not recommended comparing this
        IQR with box_plots
        :param sl: Significant level
        :type: float
        :param values: data in a numpy array format
        :type: np.Array
        :return: (lower band, upper band)
        """
        q1 = np.nanquantile(values, 0.25)
        q3 = np.nanquantile(values, 0.75)
        iqr = q3 - q1
        norm_value = sts.norm.ppf(1-sl)
        lower = q1 - (norm_value * iqr)
        upper = q3 + (norm_value * iqr)
        return lower, upper

    @staticmethod
    def __minmax_scaler(values: pd.Series) -> pd.Series:
        """
        This function receives a series and standardize them based on Min and Max points
        :param values: input Pd.Series
        :return: Standardized Series
        """
        try:
            # max and min functions can't calculate properly when there are nan in the data
            max_v = max(values.dropna())
            min_v = min(values.dropna())
            values = (values - min_v) / (max_v - min_v)
        except Exception as e:
            lg.error(e)
        return values

    @staticmethod
    def __normal_scaler(values: pd.Series) -> pd.Series:
        """
        This function receives a series and standardize them based on mean and std
        :param values: input Pd.Series
        :return: Standardized Series
        """
        try:
            values_stats = values.describe()  # Statistical attributed of the data
            mean = values_stats['mean']
            std = values_stats['std']
            values = (values - mean) / std
        except Exception as e:
            lg.error(e)
        return values

    def __beta_intervals(self,
                         values: pd.DataFrame or pd.Series,
                         sl: float) -> \
            (float, float, pd.Series):
        """
        This function calculates the intervals of a sample using beta distribution
        and returns intervals (lower band, upper band) as well as standardized data using MaxMin scaler.\n
        :param values: Receives the sample values
        :type: pd.Dataframe
        :param sl: Significant level
        :type: float
        :return:
            lower band: The lower band of calculated intervals |
            upper band: The upper band of the calculated intervals |
            scaled values: The scaled values based on the MaxMin scaler
        """
        # if type(values).__name__ == CST.DataType_Series:
        #     values = values.values  # Some functions can't operate on series \
        #     # So it is needed to be used as numpy array
        # values = values.reshape(-1, 1)  # MinMaxScaler accepts 1d data shape.
        values = self.__minmax_scaler(values)
        # Adding an epsilon to prevent having zero
        # values = values.reshape(-1,)  # Flatting data
        values_means, values_std = self.__calc_mean_std(pd.Series(values))
        values_alpha, values_beta = self.__alpha_beta(values_means,
                                                      values_std)
        var_low, var_up = self.__beta_upper_lower(sl,
                                                  values_alpha,
                                                  values_beta)
        return var_low, var_up, values

    def __normal_intervals(self,
                           values: pd,
                           sl: float) -> \
            (float, float, pd.Series):
        """
        This function calculates the intervals of a sample using Normal distribution\n
        :param values: Receives the sample values
        :param sl: Significant level
        :return:
            lower band: The lower band of calculated intervals |
            upper band: The upper band of the calculated intervals |
            scaled values: The scaled values based on the MaxMin scaler
        """

        # if type(values).__name__ == CST.DataType_Series:
        #     values = values.values  # Some functions can't operate on series \
        #     # So it is needed to be used as numpy array
        # values = values.reshape(-1, 1)  # StandardScaler accepts 1d data shape.
        # values = StandardScaler().fit_transform(values) + 1e-5
        # Adding an epsilon to prevent having zero
        # values = values.reshape(-1,)  # Flatting data
        values = self.__normal_scaler(values)
        values_stats = pd.Series(values).describe()  # Statistical attributed of the data
        var_low, var_up = self.__normal_upper_lower(sl, values_stats)
        return var_low, var_up, values

    def __iqr_intervals(self,
                        values: pd,
                        sl: float) -> \
            (float, float, pd.Series):
        """
        This function calculates the intervals of a sample using Normal distribution\n
        :param values: Receives the sample values
        :param sl: Significant level
        :return:
            lower band: The lower band of calculated intervals |
            upper band: The upper band of the calculated intervals |
            scaled values: The scaled values based on the Normal standardization |
        """

        # if type(values).__name__ == CST.DataType_Series:
        #     values = values.values  # Some functions can't operate on series \
        #     # So it is needed to be used as numpy array
        # values = values.reshape(-1, 1)  # StandardScaler accepts 1d data shape.
        # values = StandardScaler().fit_transform(values) + 1e-5
        # Adding an epsilon to prevent having zero
        # values = values.reshape(-1,)  # Flatting data
        values = self.__normal_scaler(values)
        var_low, var_up = self.__iqr_upper_lower(sl, values)
        return var_low, var_up, values

    def __plot_intervals(self,
                         analysis_type: str,
                         x_var_name: str,
                         x_values: np.array,
                         x_intervals: (float, float),
                         y_values: np.array,
                         y_intervals: (float, float),
                         sl: float,
                         method: str,
                         plot_names: bool):
        """
        Plots intervals in pair mode (x= independent variable, y = dependent variable)\n
        :param analysis_type: Panel, Time_series or Cross_sectional
        :param x_var_name: Independent variable name
        :param x_values: Independent variable values
        :param x_intervals: Independent variable intervals
        :param y_values: Dependent variable values
        :param y_intervals: Dependent variable intervals
        :param sl: significant level
        """
        y_lower_band, y_upper_band = y_intervals
        x_lower_band, x_upper_band = x_intervals
        plt.figure(figsize=(10, 10))
        if plot_names:
            for i, c in pd.concat([x_values, y_values], axis=1).iterrows():
                plt.annotate(i,
                             (c[0], c[1]),
                             color='gray',
                             fontsize=14)
            # for i, c in enumerate(category_names):
            #     # Preparing annotation of the plot to show
            #     # related data points information.
            #     plt.annotate(c,
            #                  (x_values[i], y_values[i]),
            #                  color='gray')
        plt.scatter(x_values, y_values)
        plt.ylabel(self.Dependent_var)
        plt.xlabel(x_var_name)
        [plt.axhline(y, c='r') for y in [y_lower_band, y_upper_band]]
        # Adding up intervals on the plot
        [plt.axvline(x, c='r') for x in [x_lower_band, x_upper_band]]
        title = CST.Pair_interval_title
        if method == CST.Beta_Method:
            title = title.format(method='Beta distribution',
                                 analysis_type=analysis_type,
                                 alpha=1 - sl)
        elif method == CST.Normal_Method:
            title = title.format(method='Normal distribution',
                                 analysis_type=analysis_type,
                                 alpha=1 - sl)
        elif method == CST.IQR_Method:
            title = title.format(method="Inter Quartile Range method",
                                 analysis_type=analysis_type,
                                 alpha=1 - sl)
        plt.title(title)
        plt.show()

    @staticmethod
    def __plot_hist(data: np.array,
                    intervals: (float, float),
                    outliers: list,
                    title: str = "",
                    plot_outliers_name: bool = True):
        """
        This function receives data and intervals and plots a histogram using optional parameters
        :param data: The data related to any dependent and independent variable
        :param intervals: The calculated intervals for this data
        :param outliers: [[], []]; A nested list of outliers corresponding to the lower and upper
        bands
        :param title: A string to print as title of histogram plot
        :param plot_outliers_name: whether to print the outliers' name in the plot title or not.
        """
        if not np.isnan(data).all():
            plt.figure(figsize=(10, 10))
            plt.hist(data)
            [plt.axvline(x, c='r') for x in intervals]
            if plot_outliers_name:
                title = title + "\n "+CST.Outliers+":\n" + str(outliers)
            plt.title(title)
            plt.show()

    @staticmethod
    def __outlier_names(low_band,
                        upper_band,
                        values,
                        category_names):
        """
        This function returns the outlier values names
        :param low_band: Lower band
        :param upper_band: Upper band
        :param values: Values to find names
        :param category_names: The list of all names which outliers are going to be selected
        :return:
        A list of outlier values' names
        """

        outlier_names = (category_names[values < low_band].tolist(),
                         category_names[values > upper_band].tolist())
        return outlier_names

    @staticmethod
    def __outlier_names_flattener(outliers):
        """
        This function receives two list of outliers for lower and upper bands
        and joints these lists together.
        """
        outs = []
        for values in outliers:
            try:
                outs.extend(values[0])
                outs.extend(values[1])
            except IndexError:
                continue
        return list(dict.fromkeys(outs))

    def __single_outliers(self,
                          method: str,
                          values: pd.Series,
                          sl: float,
                          names: list) -> \
            (float, float, pd.Series, list, str):

        """
        This function calculates lower band, upper band, standard values and outliers;
        :param method: Method which is used to standardized and calculate intervals
        :type: str
        :param values: values to calculate intervals and standardize
        :type: pd.DataFrame or pd.Series
        :param sl: significant level
        :type: float
        :param names: list of relevant names corresponding to each value in the parameters
        :type: list
        :returns:
            lower band: The lower band of intervals|
            upper band: The upper band of intervals|
            standard values: The corresponding standard values of received values|
            outliers: [[], []]; The name of categories which are outliers extracted from "names"|
            error_term: if any error occurs, it will send it back to the main function.
        """

        error_term = ""
        lower_band, upper_band, var_standard, outliers = (0, 0, values, [[], []])
        if method == CST.Beta_Method:
            try:
                lower_band, upper_band, var_standard = self.__beta_intervals(values,
                                                                             sl)
                outliers = self.__outlier_names(lower_band,
                                                upper_band,
                                                var_standard,
                                                names)
            except Exception as e:
                error_term = Errs.E208.format(CST.Beta_Method, e)

        elif method == CST.Normal_Method:
            try:
                lower_band, upper_band, var_standard = self.__normal_intervals(
                    values, sl)
                outliers = self.__outlier_names(lower_band,
                                                upper_band,
                                                var_standard,
                                                names)
            except Exception as e:
                error_term = Errs.E208.format(CST.Normal_Method, e)
        elif method == CST.IQR_Method:
            try:
                lower_band, upper_band, var_standard = self.__iqr_intervals(
                    values, sl)
                outliers = self.__outlier_names(lower_band,
                                                upper_band,
                                                var_standard,
                                                names)
            except Exception as e:
                error_term = Errs.E208.format(CST.IQR_Method, e)
        return lower_band, upper_band, var_standard, outliers, error_term

    def time_series_outliers(self,
                             sl: float = 0.005,
                             method: str = CST.Beta_Method,
                             plot_pairs: bool = True,
                             plot_hists: bool = True,
                             plot_outliers_name: bool = True) -> \
            (dict, dict):
        """
        time_series_outliers() calculates the outliers, by assuming the analysis type is time_series.
        So, it will first group the data based on the different categories in the input dataframe and select
        data for all time for specific category presented in the dataset. Then it will calculate intervals
        and outliers list corresponding to each variable (all dependent and independent).
        The returned data are two dictionaries and their keys are intervals[variable name][category]
        and outliers[variable name][category].
        In addition, there are some parameters to support plots with different characteristics.
        Afterwards,
        :param sl: Significant level
        :type: float
        :param method: method of calculating intervals, 'beta', 'normal' or 'IQR'
        :type: str
        :param plot_pairs: whether plot intervals in a scatter pair mode (independent variable, dependent variable)
        :type: bool
        :param plot_hists: whether plot intervals on the histogram per each variable
        :type: bool
        :param plot_outliers_name: whether to print outliers' names on the histogram title or not.
                                    Only works, if plot_pairs = True or plot_hist = True.
        :type: bool
        :return:
        intervals[variable name][category] |  outliers[variable name][category]
        """
        lg.info(Warns.P101.format(CST.Time_Series, method).center(40, '*'))
        lg.warning(Warns.W101)
        dict_intervals = {}  # dict[var] = dict[cat]
        dict_standard_values = {}  # dict[var] = dict[cat]
        dict_outliers = {}  # dict[var] = dict[cat]
        grouped_data_by_cat_col = self.Data.groupby([self.Category_col])
        # Creating grouped dataframes based on the categories presented in the Dataframe.

        for var in [self.Dependent_var] + self.Independent_var:
            lg.info('variable {} started.'.format(var).ljust(20, '-'))
            this_var_dict_intervals = {}  # dict[cat] = tuple(lower band , upper band)
            this_var_dict_standard_values = {}  # dict[cat] = values
            this_var_dict_outliers = {}  # dict[cat] = tuple(based on lower band, based on upper band)
            for cat, cat_dt in grouped_data_by_cat_col:  # Iterating over grouped data set
                this_cat_this_var_data = cat_dt[var]
                this_cat_category_names = cat_dt[self.Time_col].values
                var_unique_values = list(set(this_cat_this_var_data.value_counts().index))
                if not (var_unique_values == [0] or var_unique_values == []):  # If there are some values
                    # Find the outliers for the single variable.
                    outliers_pack = self.__single_outliers(method=method,
                                                           values=this_cat_this_var_data,
                                                           sl=sl,
                                                           names=this_cat_category_names)
                    # Unpacking the outliers
                    l_band, u_band, standard_values, outliers, error_term = outliers_pack
                    # Saving information in the relevant dictionaries
                    this_var_dict_intervals[cat] = (l_band, u_band)
                    this_var_dict_standard_values[cat] = standard_values
                    this_var_dict_outliers[cat] = outliers

                    if error_term:
                        lg.error(error_term)
                    else:
                        if plot_hists:
                            title = CST.Hist_title.format(var,
                                                          method,
                                                          CST.Time_Series,
                                                          CST.ALL,
                                                          cat)
                            # Preparing title for the histogram
                            # if method == CST.Beta_Method or method == CST.Normal_Method:
                            # Matplot has a box plot which is used if the method is IQR# Not anymore
                            self.__plot_hist(this_var_dict_standard_values[cat],
                                             this_var_dict_intervals[cat],
                                             this_var_dict_outliers[cat],
                                             title,
                                             plot_outliers_name)
                else:
                    this_var_dict_intervals[cat] = (np.nan, np.nan)
                    this_var_dict_standard_values[cat] = np.array([])
                    this_var_dict_outliers[cat] = []
                    lg.error(Errs.E207.format(var, cat, CST.ALL))  # All rows are empty

            dict_intervals[var] = this_var_dict_intervals
            dict_standard_values[var] = this_var_dict_standard_values
            dict_outliers[var] = this_var_dict_outliers
            lg.info('variable {} done.'.format(var).ljust(20, '-'))
        if plot_pairs:
            for x_var in self.Independent_var:
                for cat, cat_dt in grouped_data_by_cat_col:
                    x_unique_values = list(set(pd.Series(dict_standard_values[x_var][cat])))
                    # in Numpy np.nan == np.nan returns false. Which means, it can't aggregate nan values.
                    # Considering that characteristic, set and list is used to get the unique values.
                    # An easy way to get unique values from the series
                    y_unique_values = list(set(pd.Series(dict_standard_values[self.Dependent_var][cat])))
                    if (not (x_unique_values == [0] or x_unique_values == [])) and \
                            (not (y_unique_values == [0] or y_unique_values == [])):
                        # To check if values are not a list of zeros or nan values
                        # this_time_category_names = cat_dt[self.Time_col].values
                        self.__plot_intervals(CST.Time_Series,
                                              x_var,
                                              dict_standard_values[x_var][cat],
                                              dict_intervals[x_var][cat],
                                              dict_standard_values[self.Dependent_var][cat],
                                              dict_intervals[self.Dependent_var][cat],
                                              sl,
                                              method,
                                              plot_outliers_name)
                    else:
                        lg.warning(Errs.E206.format(x=x_var, y=self.Dependent_var, c=cat, t=CST.ALL))
        lg.info(Warns.P102.center(40, '*'))
        return dict_intervals, dict_outliers

    def cross_sectional_outliers(self,
                                 sl: float = 0.005,
                                 method: str = CST.Beta_Method,
                                 plot_pairs: bool = True,
                                 plot_hists: bool = True,
                                 plot_outliers_name: bool = True) -> \
            (dict, dict):
        """
        cross_sectional_outliers() calculates the outliers, by assuming the analysis type is cross_sectional.
        So, it will first group the data based on the different times in the input dataframe and select
        data for all categories for specific time presented in the dataset. Then it will calculate intervals
        and outliers list corresponding to each variable (all dependent and independent).
        The returned data are two dictionaries and their keys are intervals[variable name][time]
        and outliers[variable name][time].
        In addition, there are some parameters to support plots with different characteristics.
        Afterwards,
        :param sl: Significant level
        :type: float
        :param method: method of calculating intervals, 'beta', 'normal' or 'IQR'
        :type: str
        :param plot_pairs: whether plot intervals in a scatter pair mode (independent variable, dependent variable)
        :type: bool
        :param plot_hists: whether plot intervals on the histogram per each variable
        :type: bool
        :param plot_outliers_name: whether to print outliers' names on the histogram title or not.
                                    Only works, if plot_pairs = True or plot_hist = True.
        :type: bool
        :return:
        intervals[variable name][category] |  outliers[variable name][category]
        """
        lg.info(Warns.P101.format(CST.Cross_Sectional, method).center(40, '*'))
        lg.warning(Warns.W101)
        dict_intervals = {}  # dict[var] = dict[time]
        dict_standard_values = {}  # dict[var] = dict[time]
        dict_outliers = {}  # dict[var] = dict[time]
        grouped_data_by_time_col = self.Data.groupby([self.Time_col])

        for var in [self.Dependent_var] + self.Independent_var:
            lg.info('variable {} started.'.format(var).ljust(20, '-'))
            this_var_dict_intervals = {}  # dict[time]
            this_var_dict_standard_values = {}  # dict[time]
            this_var_dict_outliers = {}  # dict[time]
            for time, time_dt in grouped_data_by_time_col:  # Iterating over grouped data set
                this_time_this_var_data = time_dt[var]
                this_time_category_names = time_dt[self.Category_col].values
                var_unique_values = list(set(this_time_this_var_data.value_counts().index))
                if not (var_unique_values == [0] or
                        var_unique_values == []):  # If there is any data to be analysis
                    # Calculating the outliers for this specific variable
                    single_outliers = self.__single_outliers(method=method,
                                                             values=this_time_this_var_data,
                                                             sl=sl,
                                                             names=this_time_category_names)
                    l_band, u_band, standard_values, outliers, error_term = single_outliers
                    # Saving the outliers' information in the relevant data set
                    this_var_dict_intervals[time] = (l_band, u_band)
                    this_var_dict_standard_values[time] = standard_values
                    this_var_dict_outliers[time] = outliers
                    if error_term:
                        lg.error(error_term)
                    else:
                        if plot_hists:
                            title = CST.Hist_title.format(var,
                                                          method,
                                                          CST.Cross_Sectional,
                                                          time,
                                                          CST.ALL)
                            self.__plot_hist(this_var_dict_standard_values[time],
                                             this_var_dict_intervals[time],
                                             this_var_dict_outliers[time],
                                             title,
                                             plot_outliers_name)
                else:
                    this_var_dict_intervals[time] = (np.nan, np.nan)
                    this_var_dict_standard_values[time] = np.array([])
                    this_var_dict_outliers[time] = []
                    lg.error(Errs.E207.format(var, CST.ALL, time))  # All rows are empty

            dict_intervals[var] = this_var_dict_intervals
            dict_standard_values[var] = this_var_dict_standard_values
            dict_outliers[var] = this_var_dict_outliers
            lg.info('variable {} done.'.format(var).ljust(20, '-'))
        if plot_pairs:

            for x_var in self.Independent_var:
                for time, time_dt in grouped_data_by_time_col:
                    #  this_time_category_names = time_dt[self.Category_col].values  # Can be accessed form index
                    x_unique_values = list(set(pd.Series(dict_standard_values[x_var][time])))
                    y_unique_values = list(set(pd.Series(dict_standard_values[self.Dependent_var][time])))
                    if (not (x_unique_values == [0] or x_unique_values == [])) and \
                            (not (y_unique_values == [0] or y_unique_values == [])):
                        self.__plot_intervals(CST.Cross_Sectional,
                                              x_var,
                                              dict_standard_values[x_var][time],
                                              dict_intervals[x_var][time],
                                              dict_standard_values[self.Dependent_var][time],
                                              dict_intervals[self.Dependent_var][time],
                                              sl,
                                              method,
                                              plot_outliers_name)
                    else:
                        lg.warning(Errs.E206.format(x=x_var, y=self.Dependent_var, c='"ALL"', t=time))
        lg.info(Warns.P102.center(40, '*'))
        return dict_intervals, dict_outliers

    def panel_outliers(self,
                       sl: float = 0.005,
                       method: str = CST.Beta_Method,
                       plot_pairs: bool = True,
                       plot_hists: bool = True,
                       plot_outliers_name: bool = True) -> \
            (dict, dict):
        """
        panel_outliers() calculates the outliers, by assuming the analysis type is panel.
        it will calculate intervals and outliers list corresponding to each variable's mean
        of the categories (not all the data for all dependent and independent).
        The returned data are two dictionaries and their keys are intervals[variable name]
        and outliers[variable name]. In addition, there are some parameters to support plots
        with different characteristics.
        The Nested structure of the panel analysis is different from time_series and cross_sectional.
        In panel analysis, it is only going over variable pairs so there are no time/category keys for
        the dictionaries. This is valid for outliers as well.
        Afterwards,
        :param sl: Significant level
        :type: float
        :param method: method of calculating intervals, 'beta', 'normal' or 'IQR'
        :type: str
        :param plot_pairs: whether plot intervals in a scatter pair mode (independent variable, dependent variable)
        :type: bool
        :param plot_hists: whether plot intervals on the histogram per each variable
        :type: bool
        :param plot_outliers_name: whether to print outliers' names on the histogram title or not.
                                    Only works, if plot_pairs = True or plot_hist = True.
        :type: bool
        :return:
        intervals[variable name] |  outliers[variable name]
        """

        lg.info(Warns.P101.format(CST.Panel, method).center(60, '*'))
        lg.warning(Warns.W101)
        dict_intervals = {}
        dict_standard_values = {}
        dict_outliers = {}

        # Grouping data based on the categories to access better
        grouped_data_by_category_col = self.Data.groupby([self.Category_col])
        list_category_names = grouped_data_by_category_col[
            self.Dependent_var].describe().index.values  # getting all category names
        for var in [self.Dependent_var] + self.Independent_var:
            lg.info('variable {} started.'.format(var).ljust(20, '-'))
            this_var_data, _ = self.__calc_mean_std(
                grouped_data_by_category_col[var])  # mean of categories are used to establish the intervals

            var_unique_values = list(set(this_var_data.value_counts().index))
            # This code drops nan values as well, so it is used instead of
            # list(set(this_var_data))
            if not (var_unique_values == [0] or var_unique_values == []):
                outliers_pack = self.__single_outliers(method=method,
                                                       values=this_var_data,
                                                       sl=sl,
                                                       names=list_category_names)
                l_band, u_band, standard_values, outliers, error_term = outliers_pack
                dict_intervals[var] = (l_band, u_band)
                dict_standard_values[var] = standard_values
                dict_outliers[var] = outliers

                if plot_hists:
                    title = CST.Hist_title.format(var,
                                                  method,
                                                  CST.Panel,
                                                  CST.ALL,
                                                  CST.ALL)
                    # if method == CST.Beta_Method or method == CST.Normal_Method:
                    self.__plot_hist(dict_standard_values[var],
                                     dict_intervals[var],
                                     dict_outliers[var],
                                     title,
                                     plot_outliers_name)
                    # Box plot has 1.5 fixed number to calculate IQR thus, its results are different.
            else:
                dict_intervals[var] = (np.nan, np.nan)
                dict_standard_values[var] = np.array([])
                dict_outliers[var] = []
                lg.error(Errs.E207.format(var, CST.ALL, CST.ALL))  # All rows are empty
            lg.info('variable {} done.'.format(var).ljust(20, '-'))
        if plot_pairs:
            for x_var in self.Independent_var:
                x_unique_values = list(set(pd.Series(dict_standard_values[x_var])))
                y_unique_values = list(set(pd.Series(dict_standard_values[self.Dependent_var])))
                if (not (x_unique_values == [0] or x_unique_values == [])) and \
                        (not (y_unique_values == [0] or y_unique_values == [])):
                    self.__plot_intervals(CST.Panel,
                                          x_var,
                                          dict_standard_values[x_var],
                                          dict_intervals[x_var],
                                          dict_standard_values[self.Dependent_var],
                                          dict_intervals[self.Dependent_var],
                                          sl,
                                          method,
                                          plot_outliers_name)
                else:
                    lg.warning(Errs.E206.format(x=x_var, y=self.Dependent_var, c=CST.ALL, t=CST.ALL))
        lg.info(Warns.P102.center(40, '*'))
        return dict_intervals, dict_outliers

    def time_series(self,
                    max_epochs: int = 8000,
                    alpha: float = 0.05,
                    standardization: bool = True,
                    drop_outliers: bool = False,
                    outlier_method: str = CST.Beta_Method,
                    plot: bool = False,
                    plot_only_best: bool = True,
                    show_time_label: bool = False,
                    show_outliers: bool = False,
                    plot_predicted_outliers: bool = False
                    ) -> \
            (dict, dict, dict):
        """
        Time_series() does a time-series analysis on the data set. This function groups the data based
        on the available categories in the data set and selects all values for all available times.
        Then using machine learning curve_fit() function of scipy package, it fits the different
        equation forms to find the complex patters.
        As the result, for each fitting process it returns a result object that can be accessed from the
        returned dictionaries based on the dictionary structures(see "Returns" section).
        To see the contents of the result object summary_object.help() can be used.
        To read more about the complex forms and their
        relevant equation forms and examples of this function, please refer to the GitHub page;
        :param max_epochs: Maximum number of iterations the Ml optimizer should try to re-adjust
        its findings;
        :param alpha: Significant level
        :param standardization: whether to standardize data or not
        :param plot: To plot the results or not
        :param plot_only_best: To plot best fitted function or all functions.
        There are "number of independent variables" * "number of categories" * "number of equation forms";
        amount of fitting process. Sometimes, if the data set is so variant, there can be hundreds of plot.
        In order to be effective, by putting this option to True, it only plots the best fitted equation form
        for "number of independent variables" * "number of categories" of progress;
        :param show_time_label: whether to show the times' labels on the plots or not
        :param drop_outliers: whether to do an outliers pre-processing or not
        :param show_outliers: if drop_outliers, should it show outliers points on the equation plot or not
        :param plot_predicted_outliers: if drop_outliers, should it show "Predicted" parts of fitted function
        related to the outliers or not. If False, it will only draw predicted line for the valid data
        :param outlier_method: The method name to be used for analysis of outliers;
        beta, normal or IQR
        :return:
        Optimum form dictionary[independent variable][category] = result object
        All forms' dictionary[independent variable][category][equation form name] = result object
        Error terms' dictionary [independent variable][category][equation form name] = Main Error
        """
        opt_forms_dict = dict()  # This will hold and return optimal equation forms
        # dict[independent variable][category]
        all_forms_dict = dict()  # This holds all result objects
        # dict[independent variable][category][equation form]
        error_terms = dict()  # This holds all error terms relevant to the fitting process.
        # dict[independent variable][category][equation form]
        intervals, outliers, current_outliers = None, None, None  # Initialization, To prevent linting error
        if drop_outliers:
            # collect all intervals and outliers if drop_outliers is True
            intervals, outliers = self.time_series_outliers(method=outlier_method,
                                                            plot_pairs=False,
                                                            plot_hists=False)

        for independent_var in self.Independent_var:
            lg.info(
                "X: {}, Y: {}".format(
                    self.Dependent_var,
                    independent_var).center(40, "="))
            # Selecting data for the current specific independent and dependent variable
            this_independent_dt = self.Data[[self.Time_col, self.Category_col,
                                             self.Dependent_var, independent_var]]
            cat_best_func = dict()  # Init a dict to save best function of the current variable set and categories
            cats_results = dict()  # cats_results[cat] = results[equation form]
            # Init dict to save result objects of the categories
            cats_errs = dict()  # cats_errs[cat] = errs[equation form]
            # Init dict for saving categories' error terms
            cat_groups = this_independent_dt.groupby(self.Category_col)  # Grouping the data set based on categories
            for Cat, Cats_dt in cat_groups:
                lg.info(("Category:" + Cat).center(40, "-"))
                if drop_outliers:
                    # If drop_outliers then select outliers for the current dependent variable
                    # and independent variable from the outliers' dictionary.
                    current_outliers = [outliers[key][Cat] for key in [self.Dependent_var,
                                                                       independent_var]]
                    # Flatting the nested list
                    current_outliers = self.__outlier_names_flattener(current_outliers)
                #  Preprocessing the data
                this_cat = self.__preprocessing(data=Cats_dt,
                                                regression_type=CST.Time_Series,
                                                standardization=standardization,
                                                drop_outliers=drop_outliers,
                                                outliers=current_outliers)

                this_cat = this_cat.sort_index(level=[self.Time_col])
                best_se = np.inf  # Any SE less than current should be replaced
                results = dict()  # A dict to store summary_objects in the results.
                errs = dict()  # Dictionary of the errors to return further
                if this_cat.shape[0] > 10:  # Do analysis if it is more than 10 rows
                    for func in self.Models:  # iterating over the function in the class
                        lg.info(func.__name__.center(40, "*"))  # Printing function name
                        try:
                            # Try to fit the data and receive the results
                            # popt stands for the coefficients
                            # p_cov stands for the covariance of the coefficients
                            popt, p_cov, this_cat, model_summary = self.__fit_model(
                                data=this_cat, func=func, reg_type=CST.Time_Series,
                                independent_var=independent_var, drop_outliers=drop_outliers,
                                standardization=standardization, outlier_method=outlier_method,
                                outliers=outliers, intervals=intervals, epochs=max_epochs,
                                alpha=alpha, time_series_category=Cat, cross_section_time=CST.ALL)
                            lg.info(Warns.R101.format(model_summary.SE))
                            results[func.__name__] = model_summary
                            errs[func.__name__] = None
                            if model_summary.SE < best_se:
                                # setting the best function
                                best_se = model_summary.SE
                                cat_best_func[Cat] = model_summary
                            if plot and not plot_only_best:
                                # to plot the best, we have to wait to end the loop
                                model_summary.plot(show_time_label=show_time_label,
                                                   show_outliers=show_outliers,
                                                   plot_predicted_outliers=plot_predicted_outliers)
                        except Exception as e:
                            errs[func.__name__] = "{} in function {} \n {}".format(type(e),
                                                                                   func.__name__,
                                                                                   str(e))
                            lg.error(errs[func.__name__])
                    cats_errs[Cat] = errs
                    # This can be done after the loop, but to increase the Readability
                    # In addition, in any case there would be "errs" dict, so, no need to put this in the try clause.
                    try:
                        cats_results[Cat] = results
                        if plot and cat_best_func and plot_only_best:
                            if not drop_outliers:
                                show_outliers = False
                            try:
                                cat_best_func[Cat].plot(show_time_label=show_time_label,
                                                        show_outliers=show_outliers,
                                                        plot_predicted_outliers=plot_predicted_outliers)
                            except Exception as e:
                                lg.error(str(type(e)) + Errs.E202)

                    except Exception as e:
                        lg.error(Errs.E201+"\n"+e)

                else:
                    errs = {func.__name__: Warns.W102 for func in self.Models}
                    # cats_results[Cat] = {}  # If no results, the cats_results would be empty itself
                    # So, no need to use that command. Readability purpose only
                    cats_errs[Cat] = errs  # If no results for the
                    lg.error(Warns.W102)

            opt_forms_dict[independent_var] = cat_best_func
            # cat_best_func[Cats]; because there is one cat_best_func per cat
            all_forms_dict[independent_var] = cats_results  # cats_results[cats][equations]
            error_terms[independent_var] = cats_errs  # cats_errs[cats][equations]
        return opt_forms_dict, all_forms_dict, error_terms  # data is provided in the result object

    def cross_sectional(self,
                        max_epochs: int = 8000,
                        alpha: float = 0.05,
                        standardization: bool = True,
                        drop_outliers: bool = False,
                        outlier_method: str = CST.Beta_Method,
                        plot: bool = False,
                        plot_only_best: bool = True,
                        show_category_label: bool = False,
                        show_outliers: bool = False,
                        plot_predicted_outliers: bool = False
                        ) -> \
            (dict, dict, dict):
        """
        Time_series() does a time-series analysis on the data set. This function groups the data based
        on the available categories in the data set and selects all values for all available times.
        Then using machine learning curve_fit() function of scipy package, it fits the different
        equation forms to find the complex patters.
        As the result, for each fitting process it returns a result object that can be accessed from the
        returned dictionaries based on the dictionary structures(see "Returns" section).
        To see the contents of the result object summary_object.help() can be used.
        To read more about the complex forms and their
        relevant equation forms and examples of this function, please refer to the GitHub page;
        :param max_epochs: Maximum number of iterations the Ml optimizer should try to re-adjust
        its findings;
        :param alpha: Significant level
        :param standardization: whether to standardize data or not
        :param plot: To plot the results or not
        :param plot_only_best: To plot best fitted function or all functions.
        There are "number of independent variables" * "number of categories" * "number of equation forms";
        amount of fitting process. Sometimes, if the data set is so variant, there can be hundreds of plot.
        In order to be effective, by putting this option to True, it only plots the best fitted equation form
        for "number of independent variables" * "number of categories" of progress;
        :param show_category_label: whether to show the categories' labels on the plots or not
        :param drop_outliers: whether to do an outliers pre-processing or not
        :param show_outliers: if drop_outliers, should it show outliers points on the equation plot or not
        :param plot_predicted_outliers: if drop_outliers, should it show "Predicted" parts of fitted function
        related to the outliers or not. If False, it will only draw predicted line for the valid data
        :param outlier_method: The method name to be used for analysis of outliers;
        beta, normal or IQR
        :return:
        Optimum form dictionary[independent variable][category] = result object
        All forms' dictionary[independent variable][category][equation form name] = result object
        Error terms' dictionary [independent variable][category][equation form name] = Main Error
        """
        opt_forms_dict = dict()  # This will hold and return optimal equation forms
        # dict[independent variable][time]
        all_forms_dict = dict()  # This will hold and return optimal equation forms
        # dict[independent variable][time][equation form]
        error_terms = dict()  # This holds all error terms relevant to the fitting process.
        # dict[independent variable][time][equation form]
        intervals, outliers, current_outliers = None, None, None
        if drop_outliers:
            intervals, outliers = self.cross_sectional_outliers(method=outlier_method,
                                                                plot_pairs=False,
                                                                plot_hists=False)
        for independent_var in self.Independent_var:
            lg.info("X: {}, Y: {}".format(self.Dependent_var,
                                          independent_var).center(40, "="))
            # Selecting data for the current specific independent and dependent variable
            this_independent_dt = self.Data[[self.Time_col,
                                             self.Category_col,
                                             self.Dependent_var,
                                             independent_var]]
            time_best_func = dict()  # Init a dict to save best function of the current variable set and times
            time_results = dict()  # time_results[time] = results[equation form]
            # Init dict to save result objects of the different times
            time_errs = dict()   # cats_errs[time] = errs[equation form]
            # Init dict for saving times' error terms
            time_groups = this_independent_dt.groupby(self.Time_col)  # Grouping the data set based on times
            for time, time_dt in time_groups:
                lg.info(("Time:" + time).center(40, "-"))
                if drop_outliers:
                    # If drop_outliers then select outliers for the current dependent variable
                    # and independent variable from the outliers' dictionary.
                    current_outliers = [outliers[key][time] for key in [self.Dependent_var, independent_var]]
                    # Flatting the nested list
                    current_outliers = self.__outlier_names_flattener(current_outliers)
                #  Preprocessing the data
                this_time = self.__preprocessing(data=time_dt,
                                                 regression_type=CST.Cross_Sectional,
                                                 standardization=standardization,
                                                 drop_outliers=drop_outliers,
                                                 outliers=current_outliers)

                best_se = np.inf   # Any SE less than current should be replaced
                results = dict()  # A dict to store summary_objects in the results.
                errs = dict()  # Dictionary of the errors to return further
                # related to the category
                if this_time.shape[0] > 10:  # If N data is more than 10 do analysis
                    for func in self.Models:
                        lg.info(func.__name__.center(40, "*"))
                        try:
                            # Try to fit the data and receive the results
                            # popt stands for the coefficients
                            # p_cov stands for the covariance of the coefficients
                            popt, p_cov, this_time, model_summary = self.__fit_model(
                                data=this_time, func=func, reg_type=CST.Cross_Sectional,
                                standardization=standardization, drop_outliers=drop_outliers,
                                outliers=outliers, epochs=max_epochs, independent_var=independent_var,
                                outlier_method=outlier_method,  intervals=intervals, alpha=alpha,
                                cross_section_time=time, time_series_category=CST.ALL)
                            lg.info(Warns.R101.format(model_summary.SE))  # Log the fitted message
                            results[func.__name__] = model_summary  # Save the model_summary
                            errs[func.__name__] = np.nan  # Since everything is ok, no error term.
                            if model_summary.SE < best_se:
                                # If this models.se is <best_se then this is the best_se
                                best_se = model_summary.SE
                                time_best_func[time] = model_summary
                            if plot and not plot_only_best:
                                # IF it is asked to plot all equation forms for all time and independent variable
                                model_summary.plot(show_category_label=show_category_label,
                                                   show_outliers=show_outliers,
                                                   plot_predicted_outliers=plot_predicted_outliers)
                        except Exception as e:
                            errs[func.__name__] = "{} in function {} \n {}".format(Errs.E101,
                                                                                   func.__name__,
                                                                                   str(e))
                            lg.error(errs[func.__name__])

                    time_errs[time] = errs  # In any case, there would be "errs" dict, so no need to try except
                    try:
                        # Looping over equations finished. Time to save results in the dicts
                        time_results[time] = results

                        if plot and time_best_func and plot_only_best:
                            if not drop_outliers:
                                show_outliers = False
                            try:
                                time_best_func[time].plot(show_category_label=show_category_label,
                                                          show_outliers=show_outliers,
                                                          plot_predicted_outliers=plot_predicted_outliers)
                            except Exception as e:
                                lg.error(str(type(e)) + Errs.E202)
                    except Exception as e:
                        lg.error(Errs.E201 + "\n" + e)
                else:
                    errs = {func.__name__: Warns.W102 for func in self.Models}
                    # time_results[time] = {}  # Since it is empty, and it inited as empty, then just for Readability
                    time_errs[time] = errs
                    lg.error(Warns.W102)

            all_forms_dict[independent_var] = time_results
            opt_forms_dict[independent_var] = time_best_func
            error_terms[independent_var] = time_errs
        return opt_forms_dict, all_forms_dict, error_terms

    def panel(self,
              max_epochs: int = 8000,
              alpha: float = 0.05,
              standardization: bool = True,
              drop_outliers: bool = False,
              outlier_method: str = CST.Beta_Method,
              plot: bool = False,
              show_category_label: bool = False,
              show_time_label: bool = False,
              show_outliers: bool = False,
              plot_predicted_outliers: bool = False
              ) -> \
            (dict, dict, dict):
        """
        panel() does a panel regression analysis on the data set. Using machine learning curve_fit()
        function of scipy package, it fits the different equation forms to find the complex patters for all data.
        It should be noted that, in general, because of a big characteristics of different categories
        in different data set it is recommended to analysis the data in panel mode with a team member who is
        the expert in the field. As the result, for each fitting process it returns a result object that can be
        accessed from the returned dictionaries based on the dictionary structures(see "Returns" section).
        To see the contents of the result object summary_object.help() can be used.
        To read more about the complex forms and their
        relevant equation forms and examples of this function, please refer to the GitHub page;
        >>The structure of returned data is different from time_series and cross_sectional functions
        :param max_epochs: Maximum number of iterations the Ml optimizer should try to re-adjust
        its findings;
        :param alpha: Significant level
        :param standardization: whether to standardize data or not
        :param plot: To plot the results or not
        :param show_time_label: whether to show the times' labels on the plots or not
        :param show_category_label: whether to show the categories' labels on the plots or not
        :param drop_outliers: whether to do an outliers pre-processing or not
        :param show_outliers: if drop_outliers, should it show outliers points on the equation plot or not
        :param plot_predicted_outliers: if drop_outliers, should it show "Predicted" parts of fitted function
        related to the outliers or not. If False, it will only draw predicted line for the valid data
        :param outlier_method: The method name to be used for analysis of outliers;
        beta, normal or IQR
        :return:
        Optimum form dictionary[independent variable] = result object
        All forms' dictionary[independent variable][equation form name] = result object
        Error terms' dictionary [independent variable][equation form name] = Main Error
        """
        opt_forms_dict = dict()  # opt_forms_dict[independent variable]
        all_forms_dict = dict()  # all_forms_dict[independent variable][equation forms]
        error_terms = dict()  # error_terms[independent variable][equation form]
        intervals, outliers, current_outliers = None, None, None
        if drop_outliers:
            intervals, outliers = self.panel_outliers(method=outlier_method,
                                                      plot_pairs=False,
                                                      plot_hists=False)
        for independent_var in self.Independent_var:
            results = dict()  # Initiating the results[equation form]
            errs = dict()  # errs[equation forms]

            this_independent_dt = self.Data[[self.Time_col,
                                             self.Category_col,
                                             self.Dependent_var,
                                             independent_var]]
            if drop_outliers:
                # Selecting outliers for the current pairs
                current_outliers = [outliers[key] for key in [self.Dependent_var, independent_var]]
                # Flattening the outliers
                current_outliers = self.__outlier_names_flattener(current_outliers)
            # Preprocessing the data, standardization, dropping outliers and etc
            this_independent_dt = self.__preprocessing(data=this_independent_dt,
                                                       regression_type=CST.Panel,
                                                       standardization=standardization,
                                                       drop_outliers=drop_outliers,
                                                       outliers=current_outliers)

            print_txt = "X: " + self.Dependent_var + ", Y: " + independent_var
            lg.info(print_txt.center(40, "="))
            if this_independent_dt.shape[0] > 10:  # If there are enough data to do the analysis
                best_se = np.inf
                for func in self.Models:
                    lg.info(func.__name__.center(40, "*"))
                    try:
                        # Try to fit the data and receive the results
                        # popt stands for the coefficients
                        # p_cov stands for the covariance of the coefficients
                        popt, p_cov, this_independent_dt, model_summary = self.__fit_model(
                            data=this_independent_dt, func=func, reg_type=CST.Panel,
                            standardization=standardization, independent_var=independent_var,
                            drop_outliers=drop_outliers, outlier_method=outlier_method,
                            outliers=outliers, intervals=intervals, epochs=max_epochs, alpha=alpha,
                            cross_section_time=CST.ALL, time_series_category=CST.ALL)
                        lg.info(Warns.R101.format(model_summary.SE))
                        results[func.__name__] = model_summary
                        errs[func.__name__] = np.nan
                        if model_summary.SE < best_se:
                            # IF the SE of current model is better than best_se
                            # Then current model is the best until now.
                            best_se = model_summary.SE
                            opt_forms_dict[independent_var] = model_summary
                        if plot:
                            if not drop_outliers:
                                show_outliers = False
                            try:
                                model_summary.plot(show_time_label=show_time_label,
                                                   show_category_label=show_category_label,
                                                   show_outliers=show_outliers,
                                                   plot_predicted_outliers=plot_predicted_outliers)
                            except Exception as e:
                                lg.error(str(type(e)) + Errs.E202)

                    except Exception as e:
                        errs[func.__name__] = "{} in function {} \n {}".format(Errs.E101,
                                                                               func.__name__,
                                                                               str(e))
                        lg.error(errs[func.__name__])

                error_terms[independent_var] = errs
                try:
                    all_forms_dict[independent_var] = results
                except Exception as e:
                    lg.error(Errs.E201 + "\n" + e)
            else:
                errs = {func.__name__: Warns.W102 for func in self.Models}
                # all_forms_dict[independent_var] = {}  # Since it is empty, and it inited as empty,
                # then just for Readability
                error_terms[independent_var] = errs
                lg.error(Warns.W102)

        return opt_forms_dict, all_forms_dict, error_terms

    def __fit_model(self,
                    data: pd.DataFrame,
                    func: callable,
                    reg_type: str,
                    independent_var: str,
                    standardization: bool,
                    drop_outliers: bool,
                    outlier_method: str,
                    outliers: dict,
                    intervals: dict,
                    epochs: int = 8000,
                    alpha: float = 0.05,
                    cross_section_time: str = "",
                    time_series_category: str = "") -> \
            (list, list, pd.DataFrame, Summary):
        """
        This function tries to fit data on received equation form using curve_fit() function of scipy.
        The curve_fit is using ML techniques to fit the equation, not OLS.
        Som of these parameters only are called to be passed to the Result object
        :param data: a pd.DataFrame including dependent, independent and relevant time and category columns
        :param func: a Callable function which represents equation form
        :param reg_type: Regression type to fit; panel, time_series or cross_sectional
        :param independent_var: The independent variable name in the Dataframe
        :param standardization: Should a data standardization done or not. It is using MinMax scaler
        :param drop_outliers: To drop outliers or not
        :param outlier_method: If drop_outliers, which method should be used; bet, normal, IQR
        :param outliers: Dictionary of the outliers
        :param intervals: Dictionary of the intervals
        :param epochs: Max number of epochs which should curve_fit use to iterate
        :param alpha: Significant level of analysis
        :param cross_section_time: If it is a cross_sectional analysis,
        the corresponding time in which all categories are selected for that
        :param time_series_category: If it is a time_series analysis,
        the corresponding category in which all times are selected for that
        :return:
        List of coefficients |
        A nested list of estimated covariance of the coefficients |
        The input DataFrame plus estimated values for the fitted model.
        the column of the estimated values are [independent variable name + equation form name] |
        The result object of the fitted equation form.
        """
        x = data[independent_var]
        y = data[self.Dependent_var]
        if outliers:
            # drop data before curve_fitting considering their method
            if reg_type == CST.Panel:
                # Categories are indexed as the second multi index level
                x = x.drop(outliers, level=1, errors=Errs.Ignore)
                y = y.drop(outliers, level=1, errors=Errs.Ignore)
            elif reg_type == CST.Cross_Sectional:
                x = x.drop(outliers, level=1, errors=Errs.Ignore)
                y = y.drop(outliers, level=1, errors=Errs.Ignore)
            elif reg_type == CST.Time_Series:
                # Time is index as the first multi index
                x = x.drop(outliers, level=0, errors=Errs.Ignore)
                y = y.drop(outliers, level=0, errors=Errs.Ignore)
        # lg.captureWarnings(True)

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            popt, p_cov = curve_fit(func, x, y, maxfev=epochs)
            # Don't show the warnings of curve_fitting

        # if we pass *popt to the function, since we have kept the order of coefficients properly there,
        # it will unpack and use them according to the order.
        y_hat = [func(xi, *popt) for xi in data[independent_var].values]
        data[independent_var + func.__name__] = y_hat
        # if reg_type == CST.Time_Series:
        #     data = data.sort_values(self.Time_col)
        # else:
        data = data.sort_values(by=independent_var)
        # Create the Result object
        model_summary = Summary(data=data, coefficients=popt,
                                covariance_coefficients=p_cov, func=func,
                                equ_patterns=self.__EquPatterns, reg_type=reg_type, independent_var=independent_var,
                                dependent_var=self.Dependent_var, standardization=standardization,
                                time_col_name=self.Time_col, cat_col_name=self.Category_col,
                                drop_outliers=drop_outliers, outlier_method=outlier_method,
                                outliers=outliers, intervals=intervals, alpha=alpha,
                                cross_section_time=cross_section_time, time_series_category=time_series_category)
        return popt, p_cov, data, model_summary

    def __preprocessing(self,
                        data: pd.DataFrame,
                        regression_type: str,
                        standardization: bool = True,
                        drop_outliers: bool = False,
                        outliers: list = None,
                        ) -> \
            pd.DataFrame:
        """
        This function receives data in the  dataframe shape with 4 cols
        X, Y, Time, Category (Order is not important)
        :param data:
        :type: pd.DataFrame
        :param regression_type: panel, time_series or cross_sectional
        :type: str
        :param standardization: whether to standardize the data or not
        :type: bool
        :param drop_outliers:
        :type: bool
        :param outliers: [outliers of both dependent and independent variables]
        :type: list
        :return: (Standardized data)
        :rtype: (pd.DataFrame)
        """
        d = data
        d = d.dropna()
        if d.empty:
            lg.error(Errs.E203)
            return d
        else:
            d = d.reset_index(drop=True)
            d = d.set_index([self.Time_col, self.Category_col], drop=True)
            if drop_outliers:
                if regression_type == CST.Panel:
                    d[CST.Outliers] = np.in1d(d.index.get_level_values(self.Category_col),
                                              np.array(outliers))
                elif regression_type == CST.Time_Series:
                    d[CST.Outliers] = np.in1d(d.index.get_level_values(self.Time_col), np.array(outliers))
                elif regression_type == CST.Cross_Sectional:
                    d[CST.Outliers] = np.in1d(d.index.get_level_values(self.Category_col),
                                              np.array(outliers))
                d = d.reset_index().set_index([self.Time_col, self.Category_col, CST.Outliers])
            for col in d.columns:
                try:
                    d[col] = pd.to_numeric(d[col], errors='coerce')
                except TypeError:
                    lg.error(Errs.E205)
                    return d
                if standardization:
                    d[col] = MinMaxScaler().fit_transform(
                        np.array(d[col].values).reshape(-1, 1)) + 1e-5
                    #  To prevent data from catch in 0 errors in fitting process, an epsilon is added.
            d = d.dropna()
            if d.empty:
                lg.error(Errs.E203)
            return d

# TODO 3: Save standardized data in the data set and retrieve from there. Just do standardization if it is not in the
# data set.

