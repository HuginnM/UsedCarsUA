from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
import numpy as np
from sklearn.metrics import make_scorer


# Scorer for regression
def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


mape = make_scorer(mean_absolute_percentage_error, greater_is_better=False)


class Estimator:
    @staticmethod
    def fit(train_x, train_y):
        best_params = {
            'colsample_bytree': 1,
            'eval_metric': 'mape',
            'learning_rate': 0.01,
            'max_depth': 9,
            'min_child_weight': 1,
            'n_estimators': 1000,
            'nthread': 2,
            'objective': 'reg:squarederror',
            'subsample': 0.75}

        xgb_model = XGBRegressor(**best_params)
        return xgb_model.fit(train_x, train_y)

    @staticmethod
    def predict(trained, test_x):
        return trained.predict(test_x)
