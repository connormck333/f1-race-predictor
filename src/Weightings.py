class Weightings:

    def __init__(self, df):
        self.df = df


    def apply(self):
        self.df["constructor_form"] = self.df["constructor_form"] * 10
        self.df["driver_form_avg"] = self.df["driver_form_avg"] * 5
        self.df["track_constructor_position_relative"] = self.df["track_constructor_position_relative"] * 10
        self.df["track_driver_position_relative_avg"] = self.df["track_driver_position_relative_avg"] * 1
        self.df["crash_rate_by_year"] = (100 - self.df["crash_rate_by_year"]) * 10
        self.df["reliability_by_year"] = self.df["reliability_by_year"] * 10

        return self.df