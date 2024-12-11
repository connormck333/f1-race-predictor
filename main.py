from src.F1Data import F1Data
from src.LinearRegressionModel import LinearRegressionModel
from src.Predictor import Predictor
from src.RaceData import RaceData
from src.RaceSelector import RaceSelector
from src.TrackTrends import TrackTrends

if __name__ == '__main__':
    # Create & train model
    f1_data = F1Data()
    track_trends = TrackTrends(f1_data.df)
    model = LinearRegressionModel(track_trends.df)

    # Get race to predict
    predict_data = RaceSelector(f1_data.circuits).get_race()
    race_data = RaceData(track_trends.df, predict_data)

    # Predict race
    predictor = Predictor(model.model)
    predict_data = predictor.prepare_data(race_data.df, model.label_encoder, model.scaler)
    result = predictor.predict(predict_data, race_data.df)