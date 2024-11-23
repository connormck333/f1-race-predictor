class TrackTrends:

    def __init__(self, df):
        self.df = df

        # Constructor track trends
        self.calculate_track_points("constructorName", "track_constructor_points")
        self.assign_track_position("track_constructor_points", "track_constructor_position")
        self.calculate_positions_against_standings("constructorStandingsPosition", "track_constructor_position", "track_constructor_position_relative")

        # Driver track trends
        self.calculate_track_points("driverRef", "track_driver_points")
        self.assign_track_position("track_driver_points", "track_driver_position")
        self.calculate_positions_against_standings("driverStandingsPosition", "track_driver_position", "track_driver_position_relative")


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