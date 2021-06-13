import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder


class DataLoader(object):
    def fit(self, dataset):
        self.df = dataset.copy()

    def load_data(self):
        # fill nans
        self.df['drive'] = self.df['drive'].fillna(self.df['drive'].mode()[0])
        self.df['engV'] = self.df['engV'].fillna(self.df['engV'].median())

        # remove outliers
        self.df = self.df[self.df['mileage'].between(
            self.df['mileage'].quantile(0.05),
            self.df['mileage'].quantile(0.95))]
        self.df = self.df[self.df.engV.between(
            self.df['engV'].quantile(0),
            self.df['engV'].quantile(0.99))]

        # Label Encoder
        for c in self.df.columns:
            if self.df[c].dtype == 'object':
                lbl = LabelEncoder()
                lbl.fit(list(self.df[c].values))
                self.df[c] = lbl.transform(list(self.df[c].values))

        return self.df
