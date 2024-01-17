import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from datetime import datetime, timedelta
from DbManager import DbManager
import time


class Predictor:
    _models: dict

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Predictor, cls).__new__(cls)
            cls.instance._models = {}
        return cls.instance

    def convert_to_datetime(self, timestamp_str):
        date_time = datetime.fromisoformat(timestamp_str)
        return date_time

    def preprocessing(self, cross_road, tl_id):
        date_array, flux_array = self.get_date_flux_array(cross_road, tl_id)
        dataset = pd.DataFrame({
            'DateTime': date_array,
            'Flux': flux_array
        })
        dataset['WeekDay'] = dataset['DateTime'].dt.dayofweek
        dataset['Target'] = dataset['Flux'] > 0
        dataset['Hour'] = dataset['DateTime'].dt.hour
        dataset['Minutes'] = dataset['DateTime'].dt.minute
        X = dataset[['Hour', 'Minutes', 'WeekDay']]
        Y = dataset['Flux']
        return X, Y

    def fit(self, cross_road, tl_id):
        X, Y = self.preprocessing(cross_road, tl_id)
        np.random.seed(42)
        model = DecisionTreeRegressor()
        model.fit(X, Y)
        self._models[(cross_road, tl_id)] = model

    def get_date_flux_array(self, cross_road, tl_id):
        data_db = DbManager().get_flux_mean(cross_road, tl_id)
        flux = [data_db[i]["_value"] for i in range(len(data_db))]
        date = [self.convert_to_datetime(data_db[i]["_time"]) for i in range(len(data_db))]
        return date, flux

    def prepare_data_to_predict(self, datetime_array):
        dataset = pd.DataFrame({
            'DateTime': datetime_array,
        })
        dataset['Hour'] = dataset['DateTime'].dt.hour
        dataset['Minutes'] = dataset['DateTime'].dt.minute
        dataset['WeekDay'] = dataset['DateTime'].dt.dayofweek
        return dataset[['Hour', 'Minutes', 'WeekDay']]



    def predict(self, next_times, cross_road, tl_id):
        prediction_time = [datetime.fromtimestamp(next_time) for next_time in next_times]
        prediction_time_df = self.prepare_data_to_predict(prediction_time)
        prediction = self._models[(cross_road, tl_id)].predict(prediction_time_df)
        prediction_time_df['Flux'] = prediction
        prediction_time_df['Predicted Status'] = prediction_time_df['Flux'] > 0
        if prediction_time_df['Predicted Status'].any():
            index = prediction_time_df['Predicted Status'].idxmax()
            return next_times[index]
        else:
            return 0
