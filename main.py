from src.F1Data import F1Data
from src.LinearRegressionModel import LinearRegressionModel
from src.RaceData import RaceData
from src.RaceSelector import RaceSelector
from src.TrackTrends import TrackTrends

if __name__ == '__main__':
    # Create & train model
    f1_data = F1Data()
    track_trends = TrackTrends(f1_data.df)
    LinearRegressionModel(track_trends.df)

    # Get race to predict
    predict_data = RaceSelector(f1_data.circuits).get_race()
    race_data = RaceData(track_trends.df, predict_data)