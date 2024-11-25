import json

import pandas as pd

from src.utils.utils import get_file_path


def invalid_track_num():
    print("Invalid track number.")
    print("Please try again.")


class RaceSelector:

    def __init__(self, circuits_df):
        self.circuits_df = circuits_df
        with open(get_file_path("data/calendar.json"), "r") as f:
            self.current_tracks = json.load(f)


    def ask_user_year(self):
        valid = False
        year = None
        while not valid:
            year = input("Enter prediction year: ")
            if year in self.current_tracks.keys():
                valid = True
            else:
                print("Invalid year, please try again.")

        return year


    def ask_user_track(self, year):
        for i in range(len(self.current_tracks[year])):
            track = self.current_tracks[year][i]
            print(str(i) + ". " + track)

        print("\n")

        valid = False
        track_num = None
        while not valid:
            try:
                track_num = int(input("Enter track number: "))
            except:
                invalid_track_num()
                continue

            if track_num < 0 or track_num >= len(self.current_tracks[year]):
                invalid_track_num()
            else:
                valid = True

        return self.current_tracks[year][track_num]


    def get_circuit_id(self, track_ref):
        circuit = self.circuits_df.loc[
            (self.circuits_df["circuitRef"] == track_ref)
        ]
        return circuit["circuitId"]


    def get_race(self):
        year = self.ask_user_year()
        track_ref = self.ask_user_track(year)

        data = {
            "year": year,
            "circuitRef": track_ref,
            "circuitId": self.get_circuit_id(track_ref)
        }

        return pd.DataFrame(data)