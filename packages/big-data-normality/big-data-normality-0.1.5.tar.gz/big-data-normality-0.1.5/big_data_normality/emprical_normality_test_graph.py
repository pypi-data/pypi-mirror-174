"""
This module aims at normality graph for big datasets.
"""

import pandas as pd
import numpy as np
import statistics
import matplotlib.pyplot as plt

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


class EmpiricalNormalityTestGraph:
    """
    Takes data from users and returns outputs of empirical rule normality graph processed data.
    """

    def __init__(self, df):
        """
        df is data of users.
        """

        # inputs
        self.df_users_data = df

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

            df_smp_app = df_nd_smp.append(df_smp, ignore_index=True)

            df_smp_app.plot(x="values", y=["Normal Distribution", "Real Distribution"], figsize=(16, 10), grid=True,
                            marker='o', linewidth=3.0)

            # size of on top right legend
            plt.legend(fontsize=12)

            # add title and axis names
            plt.title('{0} Normal vs Real Distributions\n'.format(str(col_name)), fontsize=30)
            plt.xlabel('\nValues', fontsize=22)
            plt.ylabel('Destiny\n', fontsize=22)
            plt.show()

            i_data += 1

    def get_processed(self):
        return
