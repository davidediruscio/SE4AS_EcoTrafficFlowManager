import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from datetime import datetime, timezone
from DbManager import DbManager
from sklearn.metrics import accuracy_score, confusion_matrix


class Predictor:

    _models: dict

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Predictor, cls).__new__(cls)
        return cls.instance

    def convert_to_time_stemp(self, timestamp_str):
        timestamp = datetime.fromisoformat(timestamp_str).replace(tzinfo=timezone.utc).timestamp()
        return timestamp

    def fit(self, cross_road, tl_id):
        np.random.seed(42)
        date_array, flux_array = self.get_date_flux_array(cross_road, tl_id)
        dataset = pd.DataFrame({
            'Date': date_array,
            'Flux': flux_array
        })
        dataset['Target'] = dataset['Flux'] > 0
        model = LogisticRegression()
        model.fit(dataset['Date'], dataset['Target'])
        self._models[(cross_road, tl_id)] = model

    def get_date_flux_array(self, cross_road, tl_id):
        data_db = DbManager().get_flux_mean(cross_road, tl_id)
        flux = [data_db[i]["_value"] for i in range(len(data_db))]
        date = [data_db[i]["_time"] for i in range(len(data_db))]
        return date, flux



    def predict(self, date, cross_road, tl_id):
        return self._models[(cross_road, tl_id)].predict([date])