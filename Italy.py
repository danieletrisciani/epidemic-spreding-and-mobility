import pandas as pd
from City import City
import matplotlib.pyplot as plt
import numpy as np
import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

class Italy:

    def __init__(self, city_dataframe):
        
        self.cities = []

        for index, row in city_dataframe.iterrows():
            coor = [row['Latitude'], row["Longitude"]]

            self.cities.append(City(row['Name'], row['Population'], row['Occurrence'], coor))

        for city in self.cities:
            city.calcInitData(self.cities)

        
        self.time = 0
        self.delta_time = 1
        self.stop_sim = 200

        self.close_air_delay = 90

        self.beta = 0.2  # average number of contacts per person per time
        self.gamma = 1./10   # length of time spent by an individual in the infectious state

    def calc_total_infection(self):
        
        S = np.zeros(len(self.cities[0].S))
        I = np.zeros(len(self.cities[0].S))
        R = np.zeros(len(self.cities[0].S))

        tot_pop = 0

        for city in self.cities:
            for i in range(len(S)):
                S[i] += city.S[i]
                I[i] += city.I[i]
                R[i] += city.R[i]
            tot_pop += city.N

        t = np.linspace(0, len(S), len(S))

        # Plot the data on three separate curves for S(t), I(t) and R(t)
        fig = plt.figure(facecolor='w')
        ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
        ax.plot(t, S/tot_pop, 'b', alpha=0.5, lw=2, label='Susceptible')
        ax.plot(t, I/tot_pop, 'r', alpha=0.5, lw=2, label='Infected')
        ax.plot(t, R/tot_pop, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
        ax.set_xlabel('Time /days')
        ax.set_ylabel('Normalized Population')
        ax.set_ylim(0, 1.2)
        ax.yaxis.set_tick_params(length=0)
        ax.xaxis.set_tick_params(length=0)
        ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)
        plt.show()

        
    def closeAllAirports(self):
        for city in self.cities:
            city.airport_opened = False
    
    def updateModel(self):

        if(self.time > self.close_air_delay and self.close_air_delay >= 0):
            self.closeAllAirports()

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
        
        if(self.cities[0].airport_opened):
            status = "Open"
        else:
            status = "Closed"
        print("Airport: " + status)

data_folder = "../databases/"
allinfo_df = pd.read_csv(data_folder + "allinfo.csv")

italy = Italy(allinfo_df, )

while(italy.updateModel()):
    # italy.printAllData()
    if(italy.time == italy.stop_sim):
        # italy.showPlots("Fiumicino")
        italy.printAllData()
        italy.calc_total_infection()
    pass