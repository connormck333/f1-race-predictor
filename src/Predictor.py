import pandas as pd


class Predictor:

    def __init__(self, model):
        self.model = model
        self.results = pd.DataFrame()


    def prepare_data(self, race_data, label_encoder):
        race_data["circuitId_encoded"] = label_encoder.fit_transform(race_data["circuitId"])

        prepared_data = race_data[[
            "constructor_form",
            "driver_form_avg",
            "track_constructor_position_relative",
            "track_driver_position_relative_avg",
            "crash_rate_by_year",
            "reliability_by_year",
            "circuitId_encoded"
        ]]

        prepared_data = prepared_data.fillna(0)

        normalized_data = pd.DataFrame(prepared_data, columns=prepared_data.columns)
        normalized_data.drop_duplicates(keep="first", inplace=True)

        return normalized_data


    def predict(self, prediction_data, race_data):
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
