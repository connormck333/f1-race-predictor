import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from src.utils.utils import get_file_path


class TrainingModel:

    def __init__(self, df):
        self.model = RandomForestClassifier(n_estimators=100)
        self.label_encoder = LabelEncoder()

        self.df = df
        self.rounds = self.df[["year", "round", "circuitRef", "driverRef", "constructorRef"]]

        self.X = pd.DataFrame()
        self.prepare_X()

        self.Y = df["track_constructor_position"]
        self.Y = self.Y.fillna(0)

        self.train_model()


    def prepare_X(self):
        self.df["circuitId_encoded"] = self.label_encoder.fit_transform(self.df["circuitId"])
        self.X = self.df[[
            "constructor_form",
            "driver_form_avg",
            "track_constructor_position_relative",
            "track_driver_position_relative_avg",
            "crash_rate_by_year",
            "reliability_by_year",
            "circuitId_encoded"
        ]]
        self.X = self.X.fillna(0)


    def train_model(self):
        X_train, X_test, Y_train, Y_test, rounds_train, rounds_test = train_test_split(self.X, self.Y, self.rounds, test_size=0.2, random_state=42)

        self.model.fit(X_train, Y_train)
        joblib.dump(self.model, get_file_path("./models/race_prediction_model.pkl"))

        Y_pred = self.model.predict(X_test)
        results = rounds_test.copy()
        results["Actual"] = Y_test
        results["Predicted"] = Y_pred

        accuracy = accuracy_score(Y_test, Y_pred)
        print("Accuracy:", accuracy)
