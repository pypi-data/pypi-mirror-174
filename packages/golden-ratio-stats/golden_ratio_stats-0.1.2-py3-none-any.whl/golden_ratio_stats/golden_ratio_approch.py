"""
This module aims to determine skewness, mean and deviation with a new approach on continuous data as name 'Golden Ratio in Statistics'.
"""

import pandas as pd
import statistics
import math



class GoldenRatio:
    """
    Takes data from users and returns outputs of empirical rule normality test processed data.
    """

    def __init__(self, df):
        """
        df is data of users.
        """

        # inputs
        self.df_users_data = df
        self.columns = ["col_name", "G", "O", "DLeft", "DRight"]

        # dataframes
        self.df_gris_outputs = pd.DataFrame(columns=self.columns)

        # lists
        self.list_outputs = []

        # calculation of GRiS
        self.__calc_gris_outputs()

    def __calc_gris_outputs(self):
        """
        Calculation of GRis

        Parameters
        df_users_data

        Returns
        -------
        """

        G_R = (1 + math.sqrt(5)) / 2

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
            df.sort_values(by=['data'], ascending=True, inplace=True)
            df.reset_index(inplace=True, drop=True)
            df_sorted = df.copy()

            # median value of dataset
            med = statistics.median(df['data'])

            ############################################################################
            ############################################################################
            # G skewness coef calculation
            # if xi < median
            df_fd = df_sorted[df_sorted['data'] < med]
            df_fd.reset_index(inplace=True, drop=True)
            fd_result = sum(df_fd['data'] - med)

            # if xi >= median
            df_sd = df_sorted[df_sorted['data'] >= statistics.median(df_sorted['data'])]
            df_sd.reset_index(inplace=True, drop=True)
            sd_result = sum(df_sd['data'] - med)

            G = round(fd_result / sd_result, 4)

            ############################################################################
            ############################################################################
            # G mean calculation
            df_sorted['diff_med'] = df_sorted['data'] - med
            n = df['data'].count()

            list_mc_weight = []
            i_index_mc = 0

            while i_index_mc <= n-1:
                if df_sorted['data'].iloc[i_index_mc] < med:
                    mc = (1 / G_R) + 2 * (i_index_mc / (n - 1))
                    list_mc_weight.append(mc)

                else:
                    mc = 1 + G_R - 2 * (i_index_mc / (n - 1))
                    list_mc_weight.append(mc)

                i_index_mc += 1

            df_mc = pd.DataFrame(list_mc_weight, columns=['MC'])
            df_mc_weight = pd.concat([df_sorted, df_mc], axis=1)
            dev = sum(df_mc_weight['MC'] * df_mc_weight['diff_med']) / sum(df_mc_weight['MC'])

            O_mean = round((med + dev), 4)

            ############################################################################
            ############################################################################
            # G Deviation Left-Right calculation
            k = df[df['data'] < O_mean].count()

            list_dc_weight = []
            i_index_dc = 0

            while i_index_dc <= n-1:
                if df_sorted['data'].iloc[i_index_dc] < O_mean:
                    dc = (G_R - (i_index_dc / (k - 1))).to_numpy(float)
                    list_dc_weight.append(dc)

                else:
                    dc = (G_R - (1 - (i_index_dc-k) / (n - k - 1))).to_numpy(float)
                    list_dc_weight.append(dc)
                i_index_dc += 1

            df_dc = pd.DataFrame(list_dc_weight, columns=['DC'])
            df_dc_weight = pd.concat([df_sorted, df_dc], axis=1)

            list_DLeft_pay = []
            list_DLeft_payda = []
            list_DRight_pay = []
            list_DRight_payda = []
            i_index_dev = 0

            while i_index_dev <= n-1:
                if df_dc_weight['data'].iloc[i_index_dev] < O_mean:
                    DL_pay = df_dc_weight['DC'].iloc[i_index_dev]*(df_dc_weight['data'].iloc[i_index_dev]-O_mean)
                    DL_payda = df_dc_weight['DC'].iloc[i_index_dev]

                    list_DLeft_pay.append(DL_pay)
                    list_DLeft_payda.append(DL_payda)

                else:
                    DR_pay = df_dc_weight['DC'].iloc[i_index_dev] * (df_dc_weight['data'].iloc[i_index_dev] - O_mean)
                    DR_payda = df_dc_weight['DC'].iloc[i_index_dev]

                    list_DRight_pay.append(DR_pay)
                    list_DRight_payda.append(DR_payda)
                i_index_dev += 1

            DLeft = sum(list_DLeft_pay) / sum(list_DLeft_payda)
            DRight = sum(list_DRight_pay) / sum(list_DRight_payda)

            ############################################################################
            ############################################################################
            # append to outputs
            values = [col_name, G, O_mean, DLeft, DRight]
            zipped = zip(self.columns, values)
            dict_outputs = dict(zipped)
            self.list_outputs.append(dict_outputs)

            i_data += 1

        self.df_gris_outputs = self.df_gris_outputs.append(self.list_outputs, ignore_index=True)
        print(self.df_gris_outputs)

    def get_processed(self):

        return self.df_gris_outputs
