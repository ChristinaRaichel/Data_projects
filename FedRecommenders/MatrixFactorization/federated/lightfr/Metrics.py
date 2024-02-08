
import pandas as pd
import torch
import numpy as np
import math
from sklearn import metrics as sk_metrics


class Metrics(object):
    def __init__(self, configs):
        super(Metrics, self).__init__()
        self.configs = configs

    def get_hit_ratio(self, test_data: pd.DataFrame):  # for implicit feedback
        top_k = self.configs['top_k']
        hrs = {}
        if test_data.empty:
            for current_top_k in range(1, top_k + 1):
                hrs[current_top_k] = 0.0
            return hrs

        test_data['rank'] = test_data['pred'].rank(method='first', ascending=False)
        test_data_rank = int(test_data.head(1)['rank'])

        for current_top_k in range(1, top_k + 1):
            if test_data_rank <= current_top_k:
                hrs[current_top_k] = 1.0
            else:
                hrs[current_top_k] = 0.0
        return hrs

    def get_ndcg(self, test_data: pd.DataFrame):  # for implicit feedback
        top_k = self.configs['top_k']
        ndcgs = {}
        if test_data.empty:
            for current_top_k in range(1, top_k + 1):
                ndcgs[current_top_k] = 0.0
            return ndcgs

        test_data['rank'] = test_data['pred'].rank(method='first', ascending=False)
        test_data_rank = int(test_data.head(1)['rank'])
        for current_top_k in range(1, top_k + 1):
            if test_data_rank <= current_top_k:
                ndcgs[current_top_k] = math.log(2) * 1.0 / math.log(1 + test_data_rank)
            else:
                ndcgs[current_top_k] = 0.0
        return ndcgs