import json

import pandas as pd

from src.utils.utils import get_file_path


class RaceData:

    def __init__(self, training_data, circuit):
        self.training_data = training_data
        self.circuit = circuit
        self.df = pd.DataFrame(columns=[
            "constructor_form",
            "driver_form_avg",
            "track_constructor_position_relative",
            "track_driver_position_relative_avg",
            "circuitId",
            "constructorId",
            "constructorRef",
            "year"
        ])
        with open(get_file_path("./data/current_grid.json"), "r") as f:
            data = json.load(f)
            self.constructors = data["current_constructors"]
            self.drivers = data["current_drivers"]

        self.create_df()


    def create_df(self):
        for constructor in self.constructors:
            recent_race_id = self.training_data.loc[self.training_data["constructorName"] == constructor, "raceId"].max()

            constructor_data_recent = self.training_data.loc[
                (self.training_data["constructorName"] == constructor) & (self.training_data["raceId"] == recent_race_id)]

            drivers_data_recent = self.training_data.loc[(self.training_data["constructorName"] == constructor) & (self.training_data["raceId"] == recent_race_id)]
            driver_form_avg = drivers_data_recent["driver_form_avg"].mean()

            track_driver_pos_relative_total = 0
            for _, row in drivers_data_recent.iterrows():
                avg = (
                    self.training_data.loc[
                        (self.training_data["driverRef"] == row["driverRef"]) &
                        (self.training_data["circuitId"] == self.circuit["circuitId"])
                    ]
                    .sort_values(by="raceId", ascending=False)
                    .iloc[0]["track_driver_position_relative_avg"]
                )
                print(avg)
                track_driver_pos_relative_total += avg

            track_driver_pos_relative_avg = track_driver_pos_relative_total / len(drivers_data_recent.index)
            print(track_driver_pos_relative_avg)

            constructor_dict = self.get_constructors_forms(constructor, constructor_data_recent)

            self.df.loc[len(self.df)] = [
                constructor_dict["constructor_form"],
                driver_form_avg,
                constructor_dict["track_constructor_position_relative"],
                track_driver_pos_relative_avg,
                self.circuit["circuitId"],
                constructor_dict["constructorId"],
                constructor_dict["constructorRef"],
                constructor_data_recent["year"].values[0]
            ]


    def get_constructors_forms(self, constructor_name, constructor_data_recent):
        filtered_data = self.training_data.loc[
                (self.training_data["constructorName"] == constructor_name) &
                (self.training_data["circuitId"] == self.circuit["circuitId"])
            ]

        track_constructor_pos = 0
        if not filtered_data.empty:
            track_constructor_pos = (
                filtered_data.sort_values(by="raceId", ascending=False).iloc[0]["track_constructor_position_relative"]
            )

        constructor_dict = {
            "constructorId": constructor_data_recent["constructorId"].values[0],
            "constructor_form": constructor_data_recent["constructor_form"].values[0],
            "constructorRef": constructor_data_recent["constructorRef"].values[0],
            "track_constructor_position_relative": track_constructor_pos
        }

        return constructor_dict