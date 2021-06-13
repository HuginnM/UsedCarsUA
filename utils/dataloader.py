import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder


class DataLoader(object):
    def fit(self, dataset):
        self.df = dataset.copy()

    def load_data(self):
        # Label Encoder
        for c in self.df.columns:
            if self.df[c].dtype == 'object':
                lbl = LabelEncoder()
                lbl.fit(list(self.df[c].values))
                self.df[c] = lbl.transform(list(self.df[c].values))

        return self.df
