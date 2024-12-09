import json
import kagglehub
import pandas as pd

from src.utils.utils import get_file_path
from src.utils.utils import get_points_by_position


class F1Data:

    dataAfterYear = 2014
    currentConstructors = []

    def __init__(self):
        pd.set_option("display.max_rows", 300)
        pd.set_option("display.max_columns", 10)

        # Get current drivers & constructors
        with open(get_file_path("data/current_grid.json"), "r") as f:
            data = json.load(f)
            self.currentConstructors = data["current_constructors"]
            self.currentDrivers = data["current_drivers"]

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
        self.constructor_standings = pd.read_csv(path + "/constructor_standings.csv")
        self.driver_standings = pd.read_csv(path + "/driver_standings.csv")

        self.generate_main_dataframe()
        self.normalise_constructor_names()
        self.drop_non_current_constructors()
        self.create_reliability_and_crash_rate()
        self.calculate_current_form()


    def generate_main_dataframe(self):
        df1 = pd.merge(self.races, self.results, how="inner", on=["raceId"])
        df1 = pd.merge(df1, self.drivers, how="inner", on=["driverId"], suffixes=("", "_drivers"))
        df1 = pd.merge(df1, self.constructors, how="inner", on=["constructorId"], suffixes=("", "_constructors"))
        df1 = pd.merge(df1, self.circuits, how="inner", on=["circuitId"], suffixes=("", "_circuits"))
        df1 = pd.merge(df1, self.constructor_standings, how="inner", on=["raceId", "constructorId"], suffixes=("", "_constructorStandings"))
        df1 = pd.merge(df1, self.driver_standings, how="inner", on=["raceId", "driverId"], suffixes=("", "_driverStandings"))

        df1.drop(["date", "time_x", "url", "fp1_date", "fp1_time", "fp2_date", "fp2_time", "fp3_date", "fp3_time",
                  "quali_date", "quali_time", "sprint_date", "sprint_time", "resultId", "number", "positionText",
                  "positionOrder", "laps", "time_y", "milliseconds", "fastestLap", "fastestLapTime", "fastestLapSpeed",
                  "number_drivers", "code", "dob", "url_drivers", "url_constructors", "location", "lat", "lng", "alt",
                  "url_circuits", "constructorStandingsId", "positionText_constructorStandings", "wins", "driverStandingsId",
                  "positionText_driverStandings", "wins_driverStandings"], axis=1, inplace=True)

        print(df1.columns.unique())

        df = df1.rename(columns={
            'points_constructorStandings': 'constructorStandingsPoints',
            'points_driverStandings': 'driverStandingsPoints',
            'name_constructors': 'constructorName',
            'name_circuits': 'circuitName',
            'name': 'driverName',
            'country': 'circuitCountry',
            'nationality_constructors': 'constructorNationality',
            'nationality': 'driverNationality',
            'position_constructorStandings': 'constructorStandingsPosition',
            'position_driverStandings': 'driverStandingsPosition',
            'points_y': 'constructorStandingsPoints',
            'points_x': 'driversRacePoints'
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
        self.df = self.df[self.df["constructorName"].isin(self.currentConstructors)]


    def create_reliability_and_crash_rate(self):
        with open(get_file_path("data/dnf_reasons.json"), "r") as f:
            data = json.load(f)
            non_mechanical_dnf_reasons = data["driver_dnf_reasons"] + data["non_mechanical_dnf_reasons"]
            self.calculate_constructor_reliability(non_mechanical_dnf_reasons)

            self.calculate_drivers_crash_rate(data["driver_dnf_reasons"])


    def calculate_drivers_crash_rate(self, dnf_reasons):
        crash_rate = {}

        self.df["crash_rate_by_year"] = 1.0

        for driver in self.currentDrivers:
            total_driver_dnfs = self.df.loc[
                (self.df["driverRef"] == driver) &
                (self.df["position"] == r"\N") &
                (self.df["statusId"].isin(dnf_reasons))
            ]["position"].count()
            total_entries = self.df.loc[self.df["driverRef"] == driver]["position"].count()
            crash_rate[driver] = 1 - ((total_entries - total_driver_dnfs) / total_entries)

            ## Get season crash rate
            for year in self.df["year"].unique():
                year_driver_dnfs = self.df.loc[
                    (self.df["driverRef"] == driver) &
                    (self.df["position"] == r"\N") &
                    (self.df["statusId"].isin(dnf_reasons)) &
                    (self.df["year"] == year)
                    ]["position"].count()
                year_entries = self.df.loc[
                    (self.df["driverRef"] == driver) &
                    (self.df["year"] == year)
                    ]["position"].count()

                self.df.loc[
                    (self.df["year"] == year) & (self.df["driverRef"] == driver),
                    "driver_crash_rate_by_year"
                ] = 1 - ((year_entries - year_driver_dnfs) / year_entries)

        self.df["driver_crash_rate"] = self.df["driverRef"].map(crash_rate)


    def calculate_constructor_reliability(self, dnf_reasons):
        reliability = {}

        self.df["reliability_by_year"] = 1.0

        for constructor in self.currentConstructors:
            ## Get total reliability
            total_mechanical_dnfs = self.df.loc[
                (self.df["constructorName"] == constructor) &
                (self.df["position"] == r"\N") &
                (~self.df["statusId"].isin(dnf_reasons))
                ]["position"].count()
            total_entries = self.df.loc[self.df["constructorName"] == constructor]["position"].count()
            reliability[constructor] = (total_entries - total_mechanical_dnfs) / total_entries

            ## Get season reliability
            for year in self.df["year"].unique():
                year_mechanical_dnfs = self.df.loc[
                    (self.df["constructorName"] == constructor) &
                    (self.df["position"] == r"\N") &
                    (~self.df["statusId"].isin(dnf_reasons)) &
                    (self.df["year"] == year)
                    ]["position"].count()
                year_entries = self.df.loc[
                    (self.df["constructorName"] == constructor) &
                    (self.df["year"] == year)
                    ]["position"].count()
                self.df.loc[
                    (self.df["year"] == year) & (self.df["constructorName"] == constructor),
                    "reliability_by_year"
                ] = (year_entries - year_mechanical_dnfs) / year_entries

        self.df["reliability"] = self.df["constructorName"].map(reliability)


    def calculate_current_form(self):
        self.df.sort_values(["year", "round"])
        self.df["position_points"] = self.df["position"].apply(get_points_by_position)

        self.calculate_drivers_form()
        self.calculate_constructor_form()
        self.calculate_mean_driver_form_by_team()


    def calculate_drivers_form(self):
        self.df["driver_form"] = self.df.groupby("driverRef")["position_points"] \
            .rolling(window=6, min_periods=1) \
            .mean() \
            .reset_index(level=0, drop=True)


    def calculate_constructor_form(self):
        self.df["form_id"] = self.df.groupby(["year", "round"]).ngroup()

        def calculate_constructor_form_for_group(group):
            # For each row, apply the rolling sum over the last 6 races
            return group.apply(
                lambda row: group.loc[
                    (group["form_id"] <= row["form_id"]) & (group["form_id"] > row["form_id"] - 6),
                    "driver_form"
                ].mean(), axis=1
            )

        constructor_form = self.df.groupby("constructorName").apply(calculate_constructor_form_for_group)
        constructor_form = constructor_form.reset_index(level=0, drop=True)
        self.df["constructor_form"] = constructor_form

        self.df.drop(["form_id"], inplace=True, axis=1)


    def calculate_mean_driver_form_by_team(self):
        driver_form_avg = self.df.groupby(["constructorRef", "year", "round"])["driver_form"] \
            .mean() \
            .reset_index()

        driver_form_avg.rename(columns={"driver_form": "driver_form_avg"}, inplace=True)

        self.df = self.df.merge(driver_form_avg, on=["constructorRef", "year", "round"], how="left")
