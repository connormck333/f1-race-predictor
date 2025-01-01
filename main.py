from src.F1Data import F1Data
from src.TrainingModel import TrainingModel
from src.Predictor import Predictor
from src.RaceData import RaceData
from src.RaceSelector import RaceSelector
from src.TrackTrends import TrackTrends
from src.Weightings import Weightings

if __name__ == '__main__':
    # Create & train model
    f1_data = F1Data()
    track_trends = TrackTrends(f1_data.df)
    weighted_data = Weightings(track_trends.df).apply()
    model = TrainingModel(weighted_data)

    # Get race to predict
    predict_data = RaceSelector(f1_data.circuits).get_race()
    race_data = RaceData(weighted_data, predict_data)

    # Predict race
    predictor = Predictor(model.model)
    predict_data = predictor.prepare_data(race_data.df, model.label_encoder)
    result = predictor.predict(predict_data, race_data.df)