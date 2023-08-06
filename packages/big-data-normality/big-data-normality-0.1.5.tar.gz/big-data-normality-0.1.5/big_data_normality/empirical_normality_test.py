"""
This module aims at normality test for big datasets.
"""

import pandas as pd
import numpy as np
import statistics
from scipy.stats import shapiro, kstest


# intersect of lines function
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


class EmpiricalNormalityTest:
    """
    Takes data from users and returns outputs of empirical rule normality test processed data.
    """

    def __init__(self, df):
        """
        df is data of users.
        """

        # inputs
        self.df_users_data = df
        self.columns = ["col_name", "len_data", "bt_area", "nd_area", "ratio_area", "p_value", "norm_dist",
                        "coef_skew_G"]

        # dataframes
        self.df_emp_norm_outputs = pd.DataFrame(columns=self.columns)

        # lists
        self.list_outputs = []

        # calculation of empirical normality test
        self.__calc_emp_norm_outputs()

    def __calc_emp_norm_outputs(self):
        """
        Calculation of empirical normality test

        Parameters
        df_users_data

        Returns
        -------
        """

        max_column = self.df_users_data.shape[1]

        i_data = 0

        while i_data <= max_column - 1:
            df = pd.DataFrame(self.df_users_data.iloc[:, i_data])
            df = df.dropna()
            df.columns = [x.lower() for x in df.columns]
            df.columns = df.columns.str.replace(" ", "_")
            col_name = ','.join(list(df.columns))

            df = df.set_axis(['data'], axis=1)
            df['data'] = df['data'].astype(float)

            data_points = {'points': ['µ-3σ', 'µ-2σ', 'µ-σ', 'µ-0.67σ', 'µ', 'µ+0.67σ', 'µ+σ', 'µ+2σ', 'µ+3σ'],
                           'point_values': [0, 0.0228, 0.1587, 0.2486, 0.5, 0.2486, 0.1587, 0.0228, 0]}
            df_nd = pd.DataFrame(data_points)

            percs = [0, 2.28, 15.87, 24.86, 50, 75.14, 84.13, 97.72, 100]
            df_smp = [np.percentile(df.values, i) for i in percs]
            df_smp = pd.DataFrame(df_smp, columns=['values'])
            labels = ['µ-3σ', 'µ-2σ', 'µ-σ', 'µ-0.67σ', 'µ', 'µ+0.67σ', 'µ+σ', 'µ+2σ', 'µ+3σ']
            df_smp['points'] = labels
            df_smp = pd.merge(df_smp, df_nd, on='points')
            df_smp = df_smp.rename(columns={'point_values': 'Real Distribution'})

            data_ = {'points': ['µ-3σ', 'µ-2σ', 'µ-σ', 'µ-0.67σ', 'µ', 'µ+0.67σ', 'µ+σ', 'µ+2σ', 'µ+3σ'],
                     'values': [statistics.mean(df['data']) - 3 * statistics.stdev(df['data']),
                                statistics.mean(df['data']) - 2 * statistics.stdev(df['data']),
                                statistics.mean(df['data']) - statistics.stdev(df['data']),
                                statistics.mean(df['data']) - 0.67 * statistics.stdev(df['data']),
                                statistics.mean(df['data']),
                                statistics.mean(df['data']) + 0.67 * statistics.stdev(df['data']),
                                statistics.mean(df['data']) + statistics.stdev(df['data']),
                                statistics.mean(df['data']) + 2 * statistics.stdev(df['data']),
                                statistics.mean(df['data']) + 3 * statistics.stdev(df['data'])]}
            df_nd_smp = pd.DataFrame(data_)
            df_nd = pd.DataFrame(data_points)
            df_nd_smp = pd.merge(df_nd_smp, df_nd, on='points')
            df_nd_smp = df_nd_smp.rename(columns={'point_values': 'Normal Distribution'})


            df_smp_mer = pd.merge(df_nd_smp, df_smp, on='points')
            df_smp_mer = df_smp_mer.rename(columns={'values_x': 'values_nd',
                                                    'values_y': 'values_real'})
            df_smp_mer = df_smp_mer.rename(columns={'Normal Distribution': 'normal_dist'})
            df_smp_mer = df_smp_mer.drop(["Real Distribution"], axis=1)

            # finding to intersect of lines
            column_names = [0, 1]
            df_output_t = pd.DataFrame(columns=column_names)

            i_line = 1

            while i_line <= 8:
                df_output = pd.DataFrame(line_intersection(([df_smp_mer['values_nd'].iloc[i_line],
                                                             df_smp_mer['normal_dist'].iloc[i_line]],
                                                            [df_smp_mer['values_nd'].iloc[i_line - 1],
                                                             df_smp_mer['normal_dist'].iloc[i_line - 1]]),
                                                           ([df_smp_mer['values_real'].iloc[i_line],
                                                             df_smp_mer['normal_dist'].iloc[i_line]],
                                                            [df_smp_mer['values_real'].iloc[i_line - 1],
                                                             df_smp_mer['normal_dist'].iloc[i_line - 1]])))
                i_line += 1
                df_output_t = df_output_t.append(df_output.transpose())

            df_output_t = df_output_t.rename(columns={0: 'x',
                                                      1: 'y'})
            df_output_t.reset_index(inplace=True, drop=True)

            df_con = pd.concat([df_smp_mer, df_output_t], axis=1)

            # between two lines area calculation
            list_b_area = []

            i_b_area = 0

            while i_b_area <= 7:
                if ((df_con["values_nd"].iloc[i_b_area] > df_con["values_real"].iloc[i_b_area] and
                     df_con["values_nd"].iloc[i_b_area + 1] > df_con["values_real"].iloc[i_b_area + 1]) or
                        (df_con["values_nd"].iloc[i_b_area] < df_con["values_real"].iloc[i_b_area] and
                         df_con["values_nd"].iloc[i_b_area + 1] < df_con["values_real"].iloc[i_b_area + 1])):
                    area = (abs(df_con["values_nd"].iloc[i_b_area] - df_con["values_real"].iloc[i_b_area]) + abs(
                        df_con["values_nd"].iloc[i_b_area + 1] - df_con["values_real"].iloc[i_b_area + 1])) * abs(
                        df_con["normal_dist"].iloc[i_b_area + 1] - df_con["normal_dist"].iloc[i_b_area]) / 2
                    list_b_area.append(area)
                else:
                    area = abs(df_con["values_nd"].iloc[i_b_area] - df_con["values_real"].iloc[i_b_area]) * abs(
                        df_con["y"].iloc[i_b_area] - df_con["normal_dist"].iloc[i_b_area]) / 2 + abs(
                        df_con["values_nd"].iloc[i_b_area + 1] - df_con["values_real"].iloc[i_b_area + 1]) * abs(
                        df_con["normal_dist"].iloc[i_b_area + 1] - df_con["y"].iloc[i_b_area]) / 2
                    list_b_area.append(area)
                i_b_area += 1

            # normal distiribution area calculation
            list_nd_area = []

            i_nd_area = 0

            while i_nd_area <= 3:
                if df_con["values_nd"].iloc[i_nd_area + 1] != df_con["values_nd"].iloc[4]:
                    area = (abs(df_con["values_nd"].iloc[i_nd_area] - df_con["values_nd"].iloc[-(i_nd_area + 1)]) + abs(
                        df_con["values_nd"].iloc[i_nd_area + 1] - df_con["values_real"].iloc[-(i_nd_area + 2)])) * abs(
                        df_con["normal_dist"].iloc[i_nd_area + 1] - df_con["normal_dist"].iloc[i_nd_area]) / 2
                    list_nd_area.append(area)

                elif df_con["values_nd"].iloc[i_nd_area + 1] == df_con["values_nd"].iloc[4]:
                    area = abs(df_con["values_nd"].iloc[i_nd_area] - df_con["values_nd"].iloc[-(i_nd_area + 1)]) * abs(
                        df_con["normal_dist"].iloc[i_nd_area + 1] - df_con["normal_dist"].iloc[i_nd_area]) / 2
                    list_nd_area.append(area)
                i_nd_area += 1

            # normality tests
            if 30 <= df.shape[0] <= 50:
                stat, p = shapiro(df['data'])
                alpha = 0.05

                if p > alpha:
                    distribution_normal = True
                else:
                    distribution_normal = False

            elif df.shape[0] > 50:
                stat, p = kstest(df['data'], cdf='norm',
                                 args=(statistics.mean(df['data']), statistics.stdev(df['data'])))
                alpha = 0.05

                if p > alpha:
                    distribution_normal = True
                else:
                    distribution_normal = False

            # coefficient of skewness G calculation
            df['median'] = statistics.median(df['data'])

            # if xi < median
            df_fd = df[df['data'] < statistics.median(df['data'])]
            df_fd.reset_index(inplace=True, drop=True)
            fd_result = sum(df_fd['data'] - df_fd['median'])

            # if xi >= median
            df_sd = df[df['data'] >= statistics.median(df['data'])]
            df_sd.reset_index(inplace=True, drop=True)
            sd_result = sum(df_sd['data'] - df_sd['median'])

            # append to outputs
            values = [col_name, df.shape[0], sum(list_b_area), sum(list_nd_area),
                      round((sum(list_b_area) / sum(list_nd_area)) * 100, 2),
                      p, distribution_normal, round(fd_result / sd_result, 3)]
            zipped = zip(self.columns, values)
            dict_outputs = dict(zipped)
            self.list_outputs.append(dict_outputs)

            i_data += 1

        self.df_emp_norm_outputs = self.df_emp_norm_outputs.append(self.list_outputs, ignore_index=True)
        self.df_emp_norm_outputs['emp_norm_dist'] = self.df_emp_norm_outputs['ratio_area'].apply(lambda x: True if x < 21.25 else False)
        print(self.df_emp_norm_outputs)

    def get_processed(self):

        return self.df_emp_norm_outputs
