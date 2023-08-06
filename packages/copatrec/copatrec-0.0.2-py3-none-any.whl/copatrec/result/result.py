# -*- coding: utf-8 -*-
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
import numpy as np
import pandas as pd
import sklearn.metrics as skm
import scipy.stats as sci_stat
import matplotlib.pyplot as plt
import pickle
import warnings
try:
    #  If package is installed.
    from copatrec.constants.constants import CST, Errs, Warns
except ImportError:
    #  If package is cloned.
    from src.constants.constants import CST, Errs, Warns


class ResultHelp:
    def __init__(self):
        self.Data = ': Processed data including estimated values'
        self.Reg_Type = ': Regression Type'
        self.Independent_Var = ': Name of Independent Variable'
        self.Dependent_Var = ': Name of Dependent variable'
        self.Time_col_name = ': The time column name in the dataset.'
        self.Cat_col_name = ': The category column name in the dataset.'
        self.Cross_section_time = ': Time related to the cross_sectional data'
        self.Time_series_category = ': Category of related Time_series'
        self.Func_name = 'Callable Function'
        self.Func = ': Function name'
        self.Equation_String = ': Text-based equation form'
        self.Equation_Latex = ': Latex-based equation form'
        self.Coefficients = ': Coefficients of parameters'
        self.Covariance_Coefficients = ': covariance of parameters'
        self.N = ': Number of observations'
        self.Deg_Free = ': Degree Of Freedom'
        self.DFT = ": Corrected Degrees of Freedom Total"
        self.Drop_outliers = ': Have outliers been dropped?'
        self.Outlier_method = ': Which method used to drop outliers?'
        self.Intervals = ': What are the intervals(standardized) to drop outliers?'
        self.Outliers = ": List of outliers' names."
        self.Alpha = ": Significance level"
        self.Standardization = ": Is data standardized in the process?"
        self.R2 = ': R-squared of the equation; Valid only for linear forms.'
        self.R2adj = ': Adjusted R_squared'
        self.SE_Params = ': One standard deviation errors of parameters.'
        self.T = ': T-values of parameters.'
        self.T_Table = ': T table value for the input alpha.'
        self.Par_P_values = ": coefficients p_values."
        self.Par_CI = ': Confidence intervals for the parameters.'
        self.Errors = ': All estimation Error terms.'
        self.SSE = ': Sum of Squares for Error/sum of squares for residuals.'
        self.MSE = ': Mean squared error.'
        self.R_MSE = ": Root mean squared error."
        self.SE = ': Standard error of regression/estimation(Percent)' \
                  'Typically a function is called valid if (1-alpha) percent ' \
                  'of data points are fall within -/+ 2*se'
        self.SSM = ': Corrected Sum of Squares for Model/ sum of squares for regression'
        self.SST = ': Corrected Sum of Squares Total'
        self.DMF = ': Corrected Degrees of Freedom for Model'
        self.MSM = ': Mean of Squares for Model'
        self.MST = ': Mean of Squares for Total'
        self.F = ': F_statistic value of the model.'
        self.F_Table = ': F value in the table based on the degree of freedom, significant level.'
        self.Prob_F = ': Equivalent probability of calculated F.'
        self.Error_Normal_Test = ': Normality test of Errors. Errors are normally ' \
                                 'distributed if p-value of test is more than alpha. '
        self.Is_Error_Normal = ': Are Errors normally distributed or not'
        self.Error_Stats = ': Statistically analysis of Errors'


class Result:
    """
    It could be possible to define the result class as a Data Classes, but maybe later
    Many things should be rearranged.
    We also don't want to put all arguments in the object information
    """
    def __init__(self,
                 data: pd,
                 coefficients: np.array,
                 covariance_coefficients: list,
                 func: callable,
                 equ_patterns: callable,
                 reg_type: str,
                 independent_var: str,
                 dependent_var: str,
                 standardization: bool,
                 time_col_name: str,
                 cat_col_name: str,
                 drop_outliers: bool,
                 outlier_method: str,
                 outliers: dict,
                 intervals: dict,
                 alpha: float = 0.05,
                 cross_section_time: str = "",
                 time_series_category: str = ""):

        """
        A result object which holds reports about the fitted model ane related data
        :param data: A pd.Dataframe including all X and Y and estimated Ys
        :param coefficients: an array of estimated coefficients
        :param covariance_coefficients: Covariance of estimated coefficients
        :param func: A callable function (equation form)
        :param equ_patterns: All patterns in the patterns class
        :param reg_type: Regression type: panel, time_series or cross_sectional
        :param independent_var: The independent variable names
        :param dependent_var: The dependent variable name
        :param standardization: IS data standardized or not
        :param time_col_name: The time column name
        :param cat_col_name: the category column name
        :param drop_outliers: Are outliers dropped
        :param outlier_method: Which method used to find outliers
        :param outliers: The dict of outliers
        :param intervals: The dict of intervals
        :param alpha: Significant level
        :param cross_section_time: The list of times related to the cross_sectional study
        :param time_series_category: The list of categories related to the time_series study
        """
        self.Data = data
        self.Reg_Type = reg_type
        self.Independent_Var = independent_var
        self.Dependent_Var = dependent_var
        self.Func = func
        self.Func_name = func.__name__  # the name of function in the patterns file
        y_values = self.Data[self.Dependent_Var]
        y_hat_values = self.Data[self.Independent_Var + self.Func_name]
        self.Time_col_name = time_col_name  # The time column name in the dataset.
        self.Cat_col_name = cat_col_name  # The category column name in the dataset.
        self.Cross_section_time = cross_section_time  # Only for cross-sectional analysis.
        self.Time_series_category = time_series_category  # Only for time series analysis.
        self.Drop_outliers = drop_outliers
        self.Outlier_method = outlier_method
        self.Intervals = intervals  # ([Xl, Xu], [Yl, Yu])
        self.Outliers = outliers
        eq_str = self.__equ(equ_patterns, self.Func_name, coefficients)  # A tuple of strings for the fitted form
        self.Equation_String = eq_str[0]  # Equation in the string form to print in output
        self.Equation_Latex = eq_str[1]  # Equation in the latex style to print on the plots or apps
        self.Coefficients = coefficients  # The fitted coefficients relevant to the equation form
        self.Covariance_Coefficients = covariance_coefficients  # Covariance of coefficients
        self.N = len(y_values)  # Number of observations
        self.Deg_Free = self.N - len(self.Coefficients)  # Degree of freedom
        self.Alpha = alpha  # significance level
        self.Standardization = standardization
        self.R2 = skm.r2_score(y_values, y_hat_values)
        self.DFT = self.N - 1  # Corrected Degrees of Freedom Total
        self.R2adj = 1 - ((1 - self.R2)*self.DFT) / self.Deg_Free
        try:
            # It can't calculate se_params due to very tiny or null values.
            self.SE_Params = np.sqrt(np.diag(np.abs(self.Covariance_Coefficients)))  # One standard deviation errors
            # In some cases Covariance_Coefficients can contain Nan/negative items
            self.T = self.Coefficients / self.SE_Params
            self.T_Table = sci_stat.t.ppf((1 - (self.Alpha / 2)), self.Deg_Free)
            self.Par_P_values = (1.000 - sci_stat.t.cdf(np.abs(self.T), self.Deg_Free)) * 2.000
            ebm = self.T_Table * self.SE_Params
            par_ciu = self.Coefficients + ebm
            par_cil = self.Coefficients - ebm
            self.Par_CI = np.array(list(zip(par_cil, par_ciu)))
        except ValueError:
            pass

        self.Errors = np.asarray(y_values) - np.asarray(y_hat_values)
        # Sum of Squares for Error/sum of squares for residuals
        self.SSE = np.dot(self.Errors, self.Errors.T)
        # Mean of Squares for Error
        self.MSE = self.SSE / self.Deg_Free
        self.R_MSE = np.sqrt(self.MSE)
        self.SE = np.round(np.sqrt(self.SSE/self.Deg_Free), 3)  # Its unit follows independent variable's unit.
        self.RSE = np.round(np.sum(abs(self.Errors/y_values))/self.N, 3)
        # self.SE_Fit_Goodness = self.__se_coverage()  # Ratio between 0 and 1
        # self.Outlier_Ratio = 1 - self.SE_Fit_Goodness  # Ratio between 0 and 1
        # Shapiro test is not good for the big datasets, because the nature of 
        # p_value is to imply that data is not sufficient to prove the distribution.
        # So, Anderson is better one.
        # self.Shapiro_stats , self.Shapiro_P_value = sci_stat.shapiro(self.Errors)
        # self.Anderson_stats = sci_stat.anderson(self.Errors)

        self.Error_Normal_Test = sci_stat.normaltest(self.Errors)
        self.Is_Error_Normal = self.Error_Normal_Test[1] >= self.Alpha
        self.Error_Stats = sci_stat.describe(self.Errors)
        self.General_Des = Warns.S100
        self.SSM = np.asarray(y_hat_values) - np.mean(y_values)
        self.SSM = np.dot(self.SSM, self.SSM.T)  # Corrected Sum of Squares for Model/ sum of squares for regression
        self.SST = np.asarray(y_values) - np.mean(y_values)
        self.SST = np.dot(self.SST, self.SST)  # Corrected Sum of Squares Total
        # For multiple regression: SSM + SSE = SST
        self.DFM = len(self.Coefficients) - 1  # Corrected Degrees of Freedom for Model
        self.MSM = self.SSM/self.DFM  # Mean of Squares for Model
        self.MST = self.SST / self.Deg_Free  # Mean of Squares for Total
        # MSR = sst / (self.Deg_Free)
        # self.F = self.MSE / MSR
        self.F = self.MSM / self.MSE
        self.F_Table = sci_stat.f.ppf((1 - self.Alpha),
                                      self.DFM,
                                      self.Deg_Free)
        self.Prob_F = 1.000 - sci_stat.f.cdf(np.abs(self.F),
                                             self.DFM,
                                             self.Deg_Free)

    def __se_coverage(self):
        """
        For now, this is not included in the progress.
        Indeed, this function can be used as a comparing criteria between
        two models, not an independent measurement criteria.
        How many percentages of data points fall within SE intervals?
        The percentage should be equal or larger than (1-alpha)
        :return: A percentage
        """
        y = self.Data[self.Dependent_Var]
        y_hat = self.Data[self.Independent_Var + self.Func_name]
        y_hat_se_plus = y_hat + 2 * self.SE
        y_hat_se_minus = y_hat - 2 * self.SE
        points_intervals = list(zip(y, y_hat_se_plus, y_hat_se_minus))
        points_within_intervals = [(i_minus <= i) & (i <= i_plus) for i, i_plus, i_minus in points_intervals]
        # True(1) for points that are in boundaries and False(0) for rest.
        return round(sum(points_within_intervals) / len(points_within_intervals), 3)

    def result_items(self,
                     keys: list = None):

        """
        result_items() prints the list of items in the result object with their descriptions
        :param keys: (optional) a list of items can be passed to check their description
        Otherwise, that would be a full list.
        :type: list
        """

        content_help = ResultHelp()
        report_dic = content_help.__dict__
        if keys:
            report_dic = {key: content_help.__dict__[key] for key in keys}

        for key, value in report_dic.items():
            self.__print1col((key, value))

    def report(self,
               keys: list = None):
        """
        This function prints a report of the model.
        If no argument pass to the function, it will show a full report
        Otherwise, it will print requested items. To see the list of items
        you can use result_items() function
        :param keys: a list of keys in the result-object
        :type: list
        """

        if keys:
            report_dict = {key: self.__dict__[key] for key in keys}
            for key, value in report_dict.items():
                print(key, ' : ', value)
        else:
            align = 80
            print(''.center(align, '#'))
            ###########################################
            print('Regression Result'.center(align))
            #           Regression Result            #
            print(''.center(align, '='))
            # ==========================================
            self.__print2col(("Data Type:", self.Reg_Type),
                             ("Equation:", self.Func_name))
            self.__print2col(("Dep.Var", self.Dependent_Var),
                             ("Independent.Var:", self.Independent_Var))
            self.__print2col(("Time:", self.Time_series_category),
                             ("Categories:", self.Time_series_category))
            self.__print2col(("Observations:", self.N),
                             ("Deg.Freedom:", self.Deg_Free))
            self.__print2col(("Standardized:", self.Standardization),
                             ("Significance Level:", self.Alpha))
            self.__print2col(("SE:", self.SE),
                             ("RSE:", self.RSE))
            print(''.center(align, '='))
            # ==========================================
            # Note 1
            self.__print1col(('Note:\n', self.General_Des))
            print(''.center(align, '-'))

            # ==========================================
            # Note 2
            self.__print1col(("Error Normal Test:", CST.Statistic +
                              str(round(self.Error_Normal_Test[0], 3)) + ",  " +
                              CST.P_val + " " +
                              str(round(self.Error_Normal_Test[1], 3))))
            self.__print1col(("Errors Normality:", self.Is_Error_Normal))
            self.__print1col((CST.Note, Warns.S102))

            # ------------------------------------------
            print(''.center(align, '='))
            # ==========================================
            print('Other Analysis'.center(align))
            #           Linear Analysis            #
            print(''.center(align, '-'))
            # ------------------------------------------
            alignment = int(align/10)
            print('Param'.ljust(alignment),
                  'Coeffs'.ljust(alignment),
                  'Str.Err'.ljust(2*alignment),
                  'T_stat'.ljust(alignment),
                  'p_value'.ljust(alignment),
                  'T_val.Conf'.ljust(4*alignment))
            for b in range(len(self.Coefficients)):
                self.__print6col(('B' + str(b),
                                  self.Coefficients[b],
                                  self.SE_Params[b],
                                  self.T[b],
                                  self.Par_P_values[b],
                                  self.Par_CI[b]))
            print(''.center(align, '-'))
            # ------------------------------------------
            self.__print3col(("R2:", round(self.R2, 3)),
                             ("R2.Adj:", round(self.R2adj, 3)),
                             ('', ''))
            self.__print3col(("F:", round(self.F, 3)),
                             ("F_Table:", round(self.F_Table, 3)),
                             ("Prob(F):", round(self.Prob_F, 3)))
            print(''.center(align, '='))
            # ==========================================
            print('Equation'.center(align))
            #           Equation            #
            print(''.center(align, '-'))
            self.__print1col(("Equation:", self.Equation_String))
            print(''.center(align, '#'))
            ###########################################
            # for key, value in self.__dict__.items():
            #    print(key,' : ', value)

    @staticmethod
    def help():
        """
        help() function of the result object prints an overview of functions and items in the
        result object.
        """
        help_dic = {
            'report()': 'Prints full report of the results.',
            'report(list of keys)': 'Prints report of the regression'
                                    ' for the given list of items',
            'result_items': 'Prints a list of items inside the result object '
                             'that can be called via report(list of keys) or directly'
                             'by result_object.item_name like result_object.Independent_Var',
            'save(file name)': 'This function adds a pickle to the end of the name and saves the'
                               'file. To load the file you can use pickle package.',
            'plot(args)': 'will plot the X, Y and fitted line(predicted Ys) on a scatter plot.',
            'predict(independent values)': 'will predict dependent values based on independent values.'
        }
        for key, value in help_dic.items():
            print(key, value)

    @staticmethod
    def __print1col(str1, align=80):
        """
        Prints information in one col
        :param str1:
        :param align:
        :return:
        """
        txt = str(str1[0]) + ' ' + str(str1[1])
        new_txt = [txt[i*align:(i+1)*align]
                   for i in range(int((len(txt)/align)+1))]
        for i in new_txt:
            print(i.ljust(align))

    @staticmethod
    def __print2col(s1, s2, align=80):
        """
                Prints information in two col
                :param align:
                :return:
                """
        key1, val1 = s1
        key2, val2 = s2
        c_align = 4
        d_cols = int(align / 2)
        print(key1, str(val1).rjust(d_cols - (len(key1) + c_align)),
              ''.center(c_align),
              key2, str(val2).rjust(d_cols - (len(key2) + c_align)))

    @staticmethod
    def __print3col(s1, s2, s3, align=80):
        """
                Prints information in three col
                :param align:
                :return:
                """
        key1, val1 = s1
        key2, val2 = s2
        key3, val3 = s3
        c_align = 4
        d_cols = int(align / 4)
        print(key1, str(val1).rjust(d_cols - (len(key1) + c_align)),
              ''.center(c_align),
              key2, str(val2).rjust(d_cols - (len(key2) + c_align)),
              ''.center(c_align),
              key3, str(val3).rjust(d_cols - (len(key3) + c_align)))

    @staticmethod
    def __print6col(vals, align=80):
        """
                Prints information in 6 col
                :param align:
                :return:
                """
        param, coefficients, se, t, p, ci = vals
        d_cols = int(align / 10)
        print(param.ljust(d_cols),
              str(round(coefficients, 3)).ljust(d_cols),
              str(round(se, 3)).ljust(2*d_cols),
              str(round(t, 3)).ljust(d_cols),
              str(round(p, 3)).ljust(d_cols),
              str(np.round(ci, 3)).ljust(4*d_cols))

    @staticmethod
    def __equ(obj, f, c):
        """
        Extracts the equation form
        :param obj:
        :param f:
        :param c:
        :return:
        """
        string_form, latex_form = getattr(obj, f)([round(x, 4) for x in c])
        return string_form, latex_form

    def error_hist(self):
        """
        plots the histogram of error terms
        """
        plt.hist(self.Errors, bins=20)
        plt.show()

    def predict(self,
                x: np.array) -> np.array:
        """
        This function receives new X values to predict Y based on fitted model.
        All X values here should be standardized if the model is generated using standardized values.
        :return: Y
        """
        warnings.simplefilter('always', UserWarning)
        warnings.warn(Warns.W103)
        return self.Func(x, *self.Coefficients)

    def plot(self,
             show_time_label: bool = False,
             show_category_label: bool = False,
             show_outliers: bool = False,
             plot_predicted_outliers: bool = False):
        """
        TODO: Parametrize figure size
        TODO: New Feature: plot time_series or cross_sectional beside panel plot to show bigger and smaller scale
        This function plots the result of analysis using the result object;
        :param show_time_label: Weather to show the labels of the times on the plot
        Only works if the regression type is panel or time_series
        :param show_category_label: Weather to show the labels of the categories on the plot
        Only works if the regression type is panel or cross_sectional
        :param show_outliers: Weather to plot outliers' points or not. Color would be cyan
        :param plot_predicted_outliers: Weather to plot predicted values related to the outliers or not
        :type: bool
        :return:
        """
        plt.figure(self.Independent_Var, (10, 10))
        if self.Standardization:
            plt.xticks(np.arange(0, 1, 0.05))
            plt.yticks(np.arange(0, 1, 0.05))

        dt = self.Data
        if self.Drop_outliers and show_outliers:
            fitted_data = dt[dt.index.get_level_values(CST.Outliers).isin([False])]
            outliers_data = dt[dt.index.get_level_values(CST.Outliers).isin([True])]
            plt.scatter(fitted_data[self.Independent_Var],
                        fitted_data[self.Dependent_Var])
            plt.scatter(outliers_data[self.Independent_Var],
                        outliers_data[self.Dependent_Var], c='orange')
            if plot_predicted_outliers:
                plt.plot(fitted_data[self.Independent_Var],
                         fitted_data[self.Independent_Var + self.Func_name],
                         color='red')
            else:
                plt.plot(dt[self.Independent_Var],
                         dt[self.Independent_Var + self.Func_name],
                         color='red')
        else:
            plt.scatter(dt[self.Independent_Var],
                        dt[self.Dependent_Var])
            plt.plot(dt[self.Independent_Var],
                     dt[self.Independent_Var + self.Func_name],
                     color='red')
        plt.xlabel(self.Independent_Var)
        plt.ylabel(self.Dependent_Var)
        graph_title = "Regression type: {} | SE:{}\n" \
                      "{}: {}"
        graph_title = graph_title.format(self.Reg_Type,
                                         round(self.SE, 3),
                                         self.Func_name,
                                         self.Equation_Latex)
        if self.Reg_Type == CST.Panel:
            c_names_category = ()
            c_names_time = ()
            c_names = ()
            if show_category_label:
                c_names_category = dt.index.get_level_values(
                    self.Cat_col_name).values
                c_names = c_names_category
            if show_time_label:
                c_names_time = dt.index.get_level_values(
                    self.Time_col_name).values
                c_names = c_names_time
            if show_category_label and show_time_label:
                c_names = list(zip(c_names_category.tolist(),
                                   c_names_time.tolist()))
            self.__annotate(c_names,
                            dt[self.Independent_Var].values,
                            dt[self.Dependent_Var].values)
        elif self.Reg_Type == CST.Cross_Sectional:
            graph_title = graph_title + "\n Time = " + \
                          str(self.Cross_section_time)
            if show_category_label:
                c_names = dt.index.get_level_values(self.Cat_col_name)
                self.__annotate(c_names,
                                dt[self.Independent_Var].values,
                                dt[self.Dependent_Var].values)

        elif self.Reg_Type == CST.Time_Series:
            graph_title = graph_title + "\n Category =" + \
                          str(self.Time_series_category)

            if show_time_label:
                c_names = dt.index.get_level_values(self.Time_col_name)
                self.__annotate(c_names,
                                dt[self.Independent_Var].values,
                                dt[self.Dependent_Var].values)
        plt.title(graph_title)
        plt.show()

    @staticmethod
    def __annotate(labels: list,
                   independent_var_values: np.array,
                   dependent_var_values: np.array):
        """
        This function adds annotations to the plot;
        :param labels: Labels to be added
        :param independent_var_values: Y values related to the labels
        :param dependent_var_values: X values related to the X values
        :return:
        """
        for i, txt in enumerate(labels):
            plt.annotate(txt,
                         (independent_var_values[i],
                          dependent_var_values[i]),
                         color='gray',
                         fontsize=14)

    def save(self,
             name: str):
        """
        save function receives a name of file and saves the result object in the repo
        The file would be in a pkl (pickle) format
        :param name: The name of file
        """
        name = name + '.pickle'
        with open(name, 'wb') as s:
            pickle.dump(self, s, protocol=pickle.HIGHEST_PROTOCOL)
