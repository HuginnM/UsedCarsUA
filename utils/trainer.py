from xgboost import XGBRegressor


class Estimator:
    @staticmethod
    def fit(train_x, train_y):
        return XGBRegressor().fit(train_x, train_y)

    @staticmethod
    def predict(trained, test_x):
        return trained.predict(test_x)
