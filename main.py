from src.F1Data import F1Data
from src.LinearRegressionModel import LinearRegressionModel
from src.TrackTrends import TrackTrends

if __name__ == '__main__':
    f1Data = F1Data()
    f1Data = TrackTrends(f1Data.df)
    LinearRegressionModel(f1Data.df)