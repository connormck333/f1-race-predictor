import json

import pandas as pd

from src.utils.utils import get_file_path


class RaceData:

    def __init__(self, training_data, circuit):
        self.training_data = training_data
        self.training_data.sort_values(["raceId"], ascending=[False])
        self.circuit = circuit
        self.df = pd.DataFrame(columns=[
            "constructor_form",
            "driver_form",
            "track_constructor_position_relative",
            "track_driver_position_relative",
            "circuitId",
            "constructorId",
            "driverId"
        ])
        with open(get_file_path("./data/current_grid.json"), "r") as f:
            data = json.load(f)
            self.constructors = data["current_constructors"]
            self.drivers = data["current_drivers"]

        self.set_constructors_forms()


    def set_constructors_forms(self):
        for constructor in self.constructors:
            constructor_id = self.training_data.loc[
                (self.training_data["constructorName"] == constructor),
                "constructorId"
            ].values[0]
            constructor_form = self.training_data.loc[
                (self.training_data["constructorName"] == constructor),
                "constructor_form"
            ].values[0]
            track_constructor_pos_relative = self.training_data.loc[
                (self.training_data["constructorName"] == constructor) &
                (self.training_data["circuitId"] == self.circuit["circuitId"]),
                "track_constructor_position_relative"
            ].mean()
            # track_constructor_pos_relative = track_constructor_pos_relative.values[0] if not track_constructor_pos_relative.empty else None

            new_row = pd.DataFrame([{
                "circuitId": self.circuit["circuitId"],
                "constructorId": constructor_id,
                "constructor_form": constructor_form,
                "track_constructor_position_relative": track_constructor_pos_relative
            }])
            self.df = pd.concat([self.df, new_row], ignore_index=True)

        print(self.df.head(100))