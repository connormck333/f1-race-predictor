class TrackTrends:

    def __init__(self, df):
        self.df = df

        # Constructor track trends
        self.calculate_track_points("constructorName", "track_constructor_points")
        self.assign_track_position("track_constructor_points", "track_constructor_position")
        self.calculate_positions_against_standings("constructorStandingsPosition", "track_constructor_position", "track_constructor_position_relative")
        self.scale_results("track_constructor_position_relative")

        # Driver track trends
        self.calculate_track_points("driverRef", "track_driver_points")
        self.assign_track_position("track_driver_points", "track_driver_position")
        self.calculate_positions_against_standings("driverStandingsPosition", "track_driver_position", "track_driver_position_relative")
        self.calculate_mean_driver_relative_by_team()
        self.scale_results("track_driver_position_relative_avg")


    def calculate_track_points(self, existing_column_name, new_column_name):
        track_points = self.df.groupby([existing_column_name, "year", "round"])["position_points"].sum()
        track_points = track_points.reset_index()
        track_points.rename(columns={"position_points": new_column_name}, inplace=True)
        self.df = self.df.merge(
            track_points,
            on=[existing_column_name, "year", "round"],
            how="left"
        )


    def assign_track_position(self, existing_column_name, new_column_name):
        self.df[new_column_name] = self.df.groupby(["year", "round"])[existing_column_name].rank(
            ascending=False,
            method="dense"
        ).astype(int)


    def calculate_positions_against_standings(self, standings_column_name, track_position_column_name, new_column_name):
        self.df[new_column_name] = self.df.apply(
            lambda row: row[standings_column_name] - row[track_position_column_name],
            axis=1
        )


    def calculate_mean_driver_relative_by_team(self):
        driver_relative_avg = self.df.groupby(["constructorRef", "year", "round"])["track_driver_position_relative"] \
            .mean() \
            .reset_index()

        driver_relative_avg.rename(columns={"track_driver_position_relative": "track_driver_position_relative_avg"}, inplace=True)

        self.df = self.df.merge(driver_relative_avg, on=["constructorRef", "year", "round"], how="left")


    def scale_results(self, column_name):
        min_value = self.df[column_name].min()
        max_value = self.df[column_name].max()

        self.df[column_name] = 10 * (self.df[column_name] - min_value) / (max_value - min_value)