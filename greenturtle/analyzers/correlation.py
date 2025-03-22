# Copyright (c) 2025 GreenTurtle
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Asset Return Correlation measures the relationship between the returns
of two or more assets.
"""

from typing import Union

import pandas as pd

from greenturtle.analyzers.summary import ReturnSummary


class Correlation:

    """correlation for different assets"""

    def __init__(self):
        self.return_summaries = {}

    def add_return_summary(self,
                           name,
                           return_summary: Union[ReturnSummary, None] = None):
        """add the return summary for one asset"""
        if return_summary is not None:
            self.return_summaries[name] = return_summary

    def compute_correlation(self, method="spearman"):
        """compute the correlation by pandas dataframe."""

        # construct daily return dataframe to compute the correlation.
        return_df_list = []

        for name, return_summary in self.return_summaries.items():

            days_return = return_summary.days_return
            if days_return is None:
                continue

            datetime_column = []
            return_column = []
            for day in days_return:
                datetime_column.append(day)
                return_column.append(days_return[day])

            data = {"date": datetime_column, name: return_column}
            return_df = pd.DataFrame(data)
            return_df.set_index("date", inplace=True)
            return_df_list.append(return_df)

        df = pd.concat(return_df_list, axis=1, join='inner')
        cc = df.corr(method=method)

        return cc
