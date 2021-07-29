from sklearn.preprocessing import LabelEncoder
import pandas as pd
from settings.constants import WEB_VERSION


class DataLoader(object):
    def fit(self, dataset):
        self.df = dataset.copy()

    def load_data(self):

        if not WEB_VERSION:
            # fill nans
            self.df['drive'] = self.df['drive'].fillna(self.df['drive'].mode()[0])
            self.df['engV'] = self.df['engV'].fillna(self.df['engV'].median())

            # remove outliers
            self.df = self.df[self.df['mileage'].between(self.df['mileage'].quantile(0.05), self.df['mileage'].quantile(0.95))]
            self.df = self.df[self.df.engV.between(self.df['engV'].quantile(0), self.df['engV'].quantile(0.99))]

        # add mean price at car brand
        mean_car_prices = pd.read_csv('data/mean_car_prices.csv', index_col=0, squeeze=True).astype(int)
        mean_model_prices = pd.read_csv('data/mean_model_prices.csv', index_col=0, squeeze=True)

        def mean_car_apply(x):
            for value in mean_car_prices.items():
                if x == value[0]:
                    return value[1]

        def mean_model_apply(x):
            for value in mean_model_prices.items():
                if x == value[0]:
                    return value[1]

        self.df['mean_car_price'] = self.df.car.apply(mean_car_apply)
        self.df['mean_model_price'] = self.df.model.apply(mean_model_apply)

        # Return right type of the data
        self.df[['year', 'mean_model_price', 'mileage']] = self.df[
            ['year', 'mean_model_price', 'mileage']].astype(int)
        self.df['engV'] = self.df['engV'].astype(float)

        # Need to take a features from train dataset and apply label encoding to data from request (for web version)
        train_df = pd.read_csv('data/train.csv')
        print(train_df.head())
        train_df['drive'] = train_df['drive'].fillna(train_df['drive'].mode()[0])

        # Label Encoder
        for c in self.df.columns:
            if self.df[c].dtype == 'object':
                print(c)
                lbl = LabelEncoder()
                # Change to self.df[c] to use with original dataset, skip for use with web version
                lbl.fit(list(train_df[c].values))
                self.df[c] = lbl.transform(list(self.df[c].values))
                print(1)

        # Change to right order (need for web version)
        self.df = self.df[['car', 'body', 'mileage', 'engV', 'engType',
                                     'registration', 'year', 'model',
                                     'drive', 'mean_model_price', 'mean_car_price']]
        return self.df
