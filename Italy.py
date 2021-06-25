import pandas as pd
from City import City
import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

class Italy:

    cities = []

    time = 0
    delta_time = 1
    stop_sim = 200

    close_air_delay = -1

    beta = 0.2  # average number of contacts per person per time
    gamma = 1./10   # length of time spent by an individual in the infectious state

    def __init__(self, city_dataframe):
        
        for index, row in city_dataframe.iterrows():
            coor = [row['Latitude'], row["Longitude"]]

            self.cities.append(City(row['Name'], row['Population'], row['Occurrence'], coor))

    def calc_total_infection(self):
        pass
        
    def closeAllAirports(self):
        pass
    
    def updateModel(self):

        if(self.time > self.close_air_delay and self.close_air_delay >= 0):
            self.closeAllAirports

        for city in self.cities:
            city.update(self.cities, self.beta, self.gamma, self.delta_time, self.time)
        
        self.time += self.delta_time

        if(self.time <= self.stop_sim):
            return True
        else:
            return False

    def showPlots(self, *names):
        
        found = False

        for name in names:
            for city in self.cities:

                if (city.name == name):
                    city.plotData()
                    found = True
                    break
        
        if(not found): print("This name not belong to any city")

    def printAllData(self, normalized = False):

        clearConsole()

        names = []
        pop = []
        sus = []
        inf = []
        rem = []
        occ = []

        print("Day: ", self.time - 1)

        for city in self.cities:

            lastIndex = len(city.S) - 1

            div = 1
            if(normalized): div = city.pop 

            names.append(city.name)
            pop.append(city.N)
            if div == 1: 
                sus.append(round(city.S[lastIndex] / div))
                inf.append(round(city.I[lastIndex] / div)) 
                rem.append(round(city.R[lastIndex] / div)) 
            else: 
                sus.append(city.S[lastIndex] / div)
                inf.append(city.I[lastIndex] / div)
                rem.append(city.R[lastIndex] / div)

            occ.append(city.occurrences)
        
        temp_df = pd.DataFrame({"City": names, "Pupolation": pop, "Susceptible": sus, "Infectious": inf, "Removed": rem, "Airport connection": occ})

        with pd.option_context('expand_frame_repr', False, 'display.max_columns', None, 'display.max_rows', None):  # more options can be specified also
            print(temp_df)
        
        if(self.cities[0].airport_closed):
            status = "Closed"
        else:
            status = "Open"
        print("Airport: " + status)

data_folder = "../databases/"
allinfo_df = pd.read_csv(data_folder + "allinfo.csv")

italy = Italy(allinfo_df, )

while(italy.updateModel()):
    # italy.printAllData()
    if(italy.time == 200):
        italy.showPlots("Roma")
    pass