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
            "driverId",
            "driverName",
            "year"
        ])
        with open(get_file_path("./data/current_grid.json"), "r") as f:
            data = json.load(f)
            self.constructors = data["current_constructors"]
            self.drivers = data["current_drivers"]

        self.set_drivers_forms()


    def set_drivers_forms(self):
        for driver in self.drivers:
            recent_race_id = self.training_data.loc[self.training_data["driverRef"] == driver, "raceId"].max()
            driver_data_recent = self.training_data.loc[(self.training_data["driverRef"] == driver) & (self.training_data["raceId"] == recent_race_id)]

            driver_id = driver_data_recent["driverId"].values[0]
            driver_form = driver_data_recent["driver_form_avg"].values[0] if not driver_data_recent.empty else 0

            track_driver_pos_relative = (
                self.training_data.loc[
                    (self.training_data["driverRef"] == driver) &
                    (self.training_data["circuitId"] == self.circuit["circuitId"])
                ]
                .sort_values(by="raceId", ascending=False)
                .iloc[0]["track_driver_position_relative_avg"]
            )

            constructor = driver_data_recent["constructorName"].values[0]
            constructor_dict = self.get_constructors_forms(constructor)

            self.df.loc[len(self.df)] = [
                constructor_dict["constructor_form"],
                driver_form,
                constructor_dict["track_constructor_position_relative"],
                track_driver_pos_relative,
                self.circuit["circuitId"],
                constructor_dict["constructorId"],
                constructor_dict["constructorRef"],
                driver_id,
                driver,
                driver_data_recent["year"].values[0]
            ]


    def get_constructors_forms(self, constructor):
        recent_race_id = self.training_data.loc[self.training_data["constructorName"] == constructor, "raceId"].max()

        constructor_data_recent = self.training_data.loc[
            (self.training_data["constructorName"] == constructor) & (self.training_data["raceId"] == recent_race_id)]

        filtered_data = self.training_data.loc[
                (self.training_data["constructorName"] == constructor) &
                (self.training_data["circuitId"] == self.circuit["circuitId"])
            ]

        track_constructor_pos_relative = 0
        if not filtered_data.empty:
            track_constructor_pos_relative = (
                filtered_data.sort_values(by="raceId", ascending=False).iloc[0]["track_constructor_position_relative"]
            )

        constructor_dict = {
            "constructorId": constructor_data_recent["constructorId"].values[0],
            "constructor_form": constructor_data_recent["constructor_form"].values[0],
            "constructorRef": constructor_data_recent["constructorRef"].values[0],
            "track_constructor_position_relative": track_constructor_pos_relative
        }

        return constructor_dict