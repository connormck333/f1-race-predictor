import json

import kagglehub
import pandas as pd
import os

class F1Data:

    dataAfterYear = 2014
    currentConstructors = []

    def __init__(self):
        pd.set_option("display.max_rows", 300)
        self.dir = os.path.dirname(os.path.abspath(__file__))

        # Download datasets from Kaggle
        self.df = pd.DataFrame()
        path = kagglehub.dataset_download("rohanrao/formula-1-world-championship-1950-2020")

        # Initialise relevant datasets
        self.circuits = pd.read_csv(path + "/circuits.csv")
        self.lap_times = pd.read_csv(path + "/lap_times.csv")
        self.races = pd.read_csv(path + "/races.csv")
        self.results = pd.read_csv(path + "/results.csv")
        self.drivers = pd.read_csv(path + "/drivers.csv")
        self.constructors = pd.read_csv(path + "/constructors.csv")

        self.generate_main_dataframe()
        self.normalise_constructor_names()
        self.drop_non_current_constructors()
        self.calculate_constructor_reliability()


    def generate_main_dataframe(self):
        df1 = pd.merge(self.races, self.results, how="inner", on=["raceId"])
        df2 = pd.merge(df1, self.drivers, how="inner", on=["driverId"])
        df3 = pd.merge(df2, self.constructors, how="inner", on=["constructorId"])
        df4 = pd.merge(df3, self.circuits, how="inner", on=["circuitId"], suffixes=("_x1", "_y1"))

        df4.drop(["time_x", "url_x", "fp1_date", "fp2_date", "fp3_date", "quali_date", "sprint_date", "url_y", "url_x1",
                  "location", "lat", "lng", "alt", "url_y1", "date", "number_x", "milliseconds", "number_y"], axis=1, inplace=True)

        df = df4.rename(columns={
            'name_x': 'circuitName',
            'code': 'driverCode',
            'country': 'circuitCountry',
            'name_y': 'constructorName',
            'name': 'circuitName',
            'nationality_y': 'constructorNationality',
            'nationality_x': 'driverNationality'
        })

        self.df = df[df["year"] >= self.dataAfterYear]


    def normalise_constructor_names(self):
        ## Change Racing Point and Force India to Aston Martin
        self.df["constructorRef"] = self.df["constructorRef"].apply(lambda x: "aston_martin" if x == "racing_point" else x)
        self.df["constructorRef"] = self.df["constructorRef"].apply(lambda x: "aston_martin" if x == "force_india" else x)
        self.df["constructorName"] = self.df["constructorName"].apply(lambda x: "Aston Martin" if x == "Racing Point" else x)
        self.df["constructorName"] = self.df["constructorName"].apply(lambda x: "Aston Martin" if x == "Force India" else x)

        ## Change AlphaTauri and Toro Rosso to RB F1 Team
        self.df["constructorRef"] = self.df["constructorRef"].apply(lambda x: "rb" if x == "toro_rosso" else x)
        self.df["constructorRef"] = self.df["constructorRef"].apply(lambda x: "rb" if x == "alphatauri" else x)
        self.df["constructorName"] = self.df["constructorName"].apply(lambda x: "RB F1 Team" if x == "AlphaTauri" else x)
        self.df["constructorName"] = self.df["constructorName"].apply(lambda x: "RB F1 Team" if x == "Toro Rosso" else x)

        ## Change Renault and Lotus to Alpine F1 Team
        self.df["constructorRef"] = self.df["constructorRef"].apply(lambda x: "alpine" if x == "renault" else x)
        self.df["constructorRef"] = self.df["constructorRef"].apply(lambda x: "alpine" if x == "lotus_f1" else x)
        self.df["constructorName"] = self.df["constructorName"].apply(lambda x: "Alpine F1 Team" if x == "Renault" else x)
        self.df["constructorName"] = self.df["constructorName"].apply(lambda x: "Alpine F1 Team" if x == "Lotus F1" else x)

        ## Change Alfa Romeo to Kick Sauber
        self.df["constructorRef"] = self.df["constructorRef"].apply(lambda x: "sauber" if x == "alfa" else x)
        self.df["constructorName"] = self.df["constructorName"].apply(lambda x: "Sauber" if x == "Alfa Romeo" else x)


    def drop_non_current_constructors(self):
        with open(self.get_file_path("./current_grid.json"), "r") as f:
            data = json.load(f)
            self.currentConstructors = data["current_constructors"]
            self.df = self.df[self.df["constructorName"].isin(self.currentConstructors)]


    def calculate_constructor_reliability(self):
        with open(self.get_file_path("./driver_dnf_reasons.json"), "r") as f:
            data = json.load(f)
            reliability = {}

            self.df["reliability_by_year"] = 1.0

            for constructor in self.currentConstructors:
                ## Get total reliability
                total_mechanical_dnfs = self.df.loc[
                    (self.df["constructorName"] == constructor) &
                    (self.df["position"] == r"\N") &
                    (~self.df["statusId"].isin(data["driver_dnf_reasons"]))
                ]["position"].count()
                total_entries = self.df.loc[self.df["constructorName"] == constructor]["position"].count()
                reliability[constructor] = (total_entries - total_mechanical_dnfs) / total_entries

                ## Get season reliability
                for year in self.df["year"].unique():
                    year_mechanical_dnfs = self.df.loc[
                        (self.df["constructorName"] == constructor) &
                        (self.df["position"] == r"\N") &
                        (~self.df["statusId"].isin(data["driver_dnf_reasons"])) &
                        (self.df["year"] == year)
                    ]["position"].count()
                    year_entries = self.df.loc[
                        (self.df["constructorName"] == constructor) &
                        (self.df["year"] == year)
                    ]["position"].count()
                    self.df.loc[
                        (self.df["year"] == year) & (self.df["constructorName"] == constructor),
                        "reliability_by_year"] = (year_entries - year_mechanical_dnfs) / year_entries

                    if constructor == "Williams" and year == 2014:
                        print(year_entries)
                        print(year_mechanical_dnfs)


            self.df["reliability"] = self.df["constructorName"].map(reliability)

            print(self.df[["reliability_by_year", "constructorName", "year"]].head(300))


    def get_file_path(self, file_name):
        return os.path.join(self.dir, file_name)