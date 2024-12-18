import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, StandardScaler

from src.utils.utils import get_file_path


class LinearRegressionModel:

    def __init__(self, df):
        self.model = LinearRegression()
        self.scaler = MinMaxScaler(feature_range=(1, 10))
        self.label_encoder = LabelEncoder()

        self.df = df
        self.rounds = self.df[["year", "round", "circuitRef", "driverRef", "constructorRef"]]

        self.X = pd.DataFrame()
        self.prepare_X()

        self.Y = df["track_constructor_position"]
        self.Y = self.Y.fillna(0)

        self.normalize_fields()
        self.train_model()


    def prepare_X(self):
        self.df["circuitId_encoded"] = self.label_encoder.fit_transform(self.df["circuitId"])
        self.X = self.df[[
            "constructor_form",
            "driver_form_avg",
            "track_constructor_position_relative",
            "track_driver_position_relative_avg",
            "circuitId_encoded"
        ]]
        self.X = self.X.fillna(0)

        self.X["constructor_form"] = self.X["constructor_form"] * 20



    def normalize_fields(self):
        normalized_data = self.scaler.fit_transform(self.X)
        self.X = pd.DataFrame(normalized_data, columns=self.X.columns)


    def train_model(self):
        X_train, X_test, Y_train, Y_test, rounds_train, rounds_test = train_test_split(self.X, self.Y, self.rounds, test_size=0.2, random_state=42)

        self.model.fit(X_train, Y_train)
        joblib.dump(self.model, get_file_path("./models/race_prediction_model.pkl"))

        Y_pred = self.model.predict(X_test)
        results = rounds_test.copy()
        results["Actual"] = Y_test
        results["Predicted"] = Y_pred
        print(results.loc[
                (results["year"] == 2024) & (results["circuitRef"] == "jeddah"),
                ["year", "circuitRef", "constructorRef", "Actual", "Predicted"]
              ])

        mse = mean_squared_error(Y_test, Y_pred)
        r2 = r2_score(Y_test, Y_pred)
        # accuracy = accuracy_score(Y_test, Y_pred)
        # print("Accuracy:", accuracy)

        print("Mean Squared Error:", mse)
        print("R-squared:", r2)
