import io
import pandas as pd
from datetime import datetime
from glider_reader import models

def read():
    file = io.FileIO(file=r"..\..\files\GliderMission.xlsx", mode="r")
    dataframe = pd.read_excel(file, skiprows=1)

    # I'm dropping the data after row 59 (panda index, not the excel file index) because that's where the
    # table at the bottom of the data is and it creates issues for processing the data
    dataframe = dataframe.truncate(after=59)

    # I'm dropping these rows (again, panda index, not excel) because the row is just a comment and it breaks the
    # processing of the data.
    dataframe = dataframe.drop([17, 31, 32])

    # Convert date columns to a date format, this allows them to be treated like dates later on.
    # for example after converted to date types "dataframe['Recovery date'] - dataframe['Deployment date']"
    # will return:
    # 0     2 days
    # 1     4 days
    # 2    14 days
    # 3     2 days
    # 4    18 days
    # 5    24 days
    # 6    22 days
    # 7    21 days
    # ...

    dataframe['Deployment date'] = convert_date(dataframe['Deployment date'])
    dataframe['Recovery date'] = convert_date(dataframe['Recovery date'])

    return dataframe


# Convert date types in the format '20210921' to a proper date type object
def convert_date(date):
    # we didn't cover this, but pandas has a to_date function that can be used, but we have to do a couple of things
    #
    # first, we have to make sure the column is in the right format date.apply() calls a function in this case
    # I'm using an inline function called a 'lambda' the value of each row is passed to lambda as 'd' and I return
    # just the first eight characters of it, which cuts off the '.0' if the type was read in as a float
    #
    # second, I tell the to_datetime function not to throw errors, but instead return NaT (or Not a Type) if it
    # can't figure out the format
    return pd.to_datetime(date.apply(lambda d: str(d)[0:8]), errors='coerce')


def create_database():
    df = read()
    missions = df[['Mission #', "Glider"]]
    for m in missions.iterrows():
        try:
            mn = m[1][0]
            mission = None
            missions = models.Mission.objects.filter(mission_number=mn)
            if len(missions) > 0:
                mission = missions[0]
            else:
                mission = models.Mission(mission_number=m[1][0])
                mission.save()

            g = models.Glider(mission=mission, label=m[1][1])
            g.save()
        except:
            pass