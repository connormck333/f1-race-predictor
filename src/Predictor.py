import numpy as np
import pandas as pd


class Predictor:

    def __init__(self, model):
        self.model = model
        self.results = pd.DataFrame()


    def prepare_data(self, race_data, label_encoder, scaler):
        race_data["circuitId_encoded"] = label_encoder.fit_transform(race_data["circuitId"])

        print(race_data[(race_data["constructorRef"] == "williams")])

        prepared_data = race_data[[
            "constructor_form",
            "driver_form_avg",
            "track_constructor_position_relative",
            "track_driver_position_relative_avg",
            "circuitId_encoded"
        ]]

        prepared_data = prepared_data.fillna(0)

        normalized_data = scaler.fit_transform(prepared_data)
        normalized_data = pd.DataFrame(normalized_data, columns=prepared_data.columns)
        normalized_data.drop_duplicates(keep="first", inplace=True)

        return normalized_data


    def predict(self, prediction_data, race_data):
        # probabilities = self.model.predict_proba(prediction_data)
        predictions = self.model.predict(prediction_data)

        self.results = race_data.copy()
        self.results["raw_predictions"] = predictions

        self.set_unique_predictions()

        print(self.results.loc[
                  (self.results["year"] == 2024),
                  ["year", "constructorRef", "raw_predictions", "prediction"]
              ])

        return self.results


    def set_unique_predictions(self):
        self.results["prediction"] = pd.Series(self.results["raw_predictions"]).rank(method="first", ascending=True).astype(int)
        self.results["prediction"] = self.results["prediction"].rank(method="dense")
