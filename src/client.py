import requests
from bs4 import BeautifulSoup
from models import Athlete, Ranking
import sys

import pandas as pd


class Client(object):
    def get_athlete(self, id):
        r = requests.get(
            "http://www.thepowerof10.info/athletes/profile.aspx",
            params={"athleteid": id},
        )

        print(r)

        if r.status_code != 200:
            raise AttributeError("Unable to find athlete with id %s." % id)

        soup = BeautifulSoup(r.content)

        name = soup.find_all(class_="athleteprofilesubheader")[0].h2.string.strip()
        club = (
            soup.find(id="cphBody_pnlAthleteDetails")
            .find_all("table")[2]
            .find_all("td")[1]
            .string
        )
        gender = (
            soup.find(id="cphBody_pnlAthleteDetails")
            .find_all("table")[2]
            .find_all("td")[3]
            .string
        )
        age_group = (
            soup.find(id="cphBody_pnlAthleteDetails")
            .find_all("table")[2]
            .find_all("td")[5]
            .string
        )
        county = (
            soup.find(id="cphBody_pnlAthleteDetails")
            .find_all("table")[2]
            .find_all("td")[7]
            .string
        )
        region = (
            soup.find(id="cphBody_pnlAthleteDetails")
            .find_all("table")[2]
            .find_all("td")[9]
            .string
        )
        nation = (
            soup.find(id="cphBody_pnlAthleteDetails")
            .find_all("table")[2]
            .find_all("td")[11]
            .string
        )

        print(name)
        print(club)
        print(gender)
        print(age_group)
        print(county)
        print(region)
        print(nation)

        athlete = Athlete(id=id)

        athlete.set_name(name)
        athlete.set_club(club)
        athlete.set_gender(gender)
        athlete.set_county(county)
        athlete.set_region(region)
        athlete.set_nation(nation)

        # sys.exit()
        # info = soup.find(id="ctl00_cphBody_pnlAthleteDetails").find_all('table')[2]

        # extra_details = {row.find_all("td")[0].string: row.find_all("td")[1].string for row in info.find_all("tr")}

        # print(extra_details)

        # a.import_data(extra_details)

        try:
            coach = (
                soup.find(id="ctl00_cphBody_pnlAthleteDetails")
                .find_all("table")[3]
                .find("a")
                .string
            )
            coach_url = (
                soup.find(id="ctl00_cphBody_pnlAthleteDetails")
                .find_all("table")[3]
                .find("a")
                .get("href")
            )

            athlete.set_coach(coach)

        except:
            pass

        return athlete

    def get_best_results(self, id, event="800m"):
        r = requests.get(
            "http://www.thepowerof10.info/athletes/profile.aspx",
            params={"athleteid": id},
        )

        print(r)

        if r.status_code != 200:
            raise AttributeError("Unable to find athlete with id %s." % id)

        soup = BeautifulSoup(r.content)

        data = []
        pb_table = soup.find(id="cphBody_divBestPerformances").find("table")
        rows = pb_table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            data.append(cols)

        df = pd.DataFrame(data[1:], columns=data[0])
        df = df.loc[:, ~df.columns.duplicated()]

        print(df)

    def get_all_results(self, id, event="800m"):
        r = requests.get(
            "http://www.thepowerof10.info/athletes/profile.aspx",
            params={"athleteid": id},
        )

        print(r)

        if r.status_code != 200:
            raise AttributeError("Unable to find athlete with id %s." % id)

        soup = BeautifulSoup(r.content)

        data = []
        pb_table = soup.find(id="cphBody_pnlPerformances").find_all("table")[1]
        rows = pb_table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            if len(cols) == 12:
                data.append(cols)

        df = pd.DataFrame(data[1:], columns=data[0])
        df = df.loc[:, ~df.columns.duplicated()]
        df = df[df.iloc[:, 0] != df.columns[0]]

        print(df)

    def get_ranking(self, event="10K", sex="M", year="2014", age_group="ALL"):

        r = requests.get(
            "http://www.thepowerof10.info/rankings/rankinglist.aspx",
            params={"event": event, "agegroup": age_group, "sex": sex, "year": 2014},
        )

        soup = BeautifulSoup(r.content)
        rankings_table = soup.find(id="ctl00_cphBody_lblCachedRankingList").find_all(
            "table"
        )[0]

        ranking_rows = [
            row
            for row in rankings_table.find_all("tr")
            if row["class"][0]
            not in ["rankinglisttitle", "rankinglistheadings", "rankinglistsubheader"]
        ]

        rankings = []
        for row in ranking_rows:
            if row.find_all("td")[0].string is None:
                continue
            r = Ranking(
                {
                    "athlete": Athlete(),
                    "event": event,
                    "year": year,
                    "age_group": age_group,
                }
            )
            r.rank = int(row.find_all("td")[0].string)
            r.time = row.find_all("td")[1].string
            r.athlete.name = row.find_all("td")[6].string.encode("utf-8")
            r.athlete.id = int(row.find_all("td")[6].a["href"].split("=")[1])
            r.venue = row.find_all("td")[11].string
            r.date = row.find_all("td")[12].string

            rankings.append(r)

        return rankings

