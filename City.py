import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import math
import NetworkX as nx

#the function which to solve the differential equation
def deriv(y, t, N, beta, gamma):
    S, I, R = y

    dSdt = -beta * S * I  / N 
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

class City:

    def __init__(self, name, pop, occurrences, coords, I0 = 0):
        self.name = name
        self.N = pop
        self.occurrences = occurrences
        self.coords =coords
        self.airport_opened = True
        self.z = 150

        self.S = np.array([self.N])
        self.I = np.array([0])
        self.R = np.array([0])

    def getInfected(self):

        return self.I[len(self.I) - 1]

    def update(self, cities, beta, gamma, delta_t, t):

        if(t == 0):
            init = 0
        else:
            init = 1
            
        t_inter = np.linspace(t, t + delta_t, 2)

        y0 = self.S[len(self.S) - 1], self.I[len(self.I) - 1], self.R[len(self.R) - 1]

        # cities that host an airport has bigger beta than others
        if(self.airport_opened and self.occurrences != 0):
            beta += (self.occurrences/1E4)

        for city in cities:
            if(city.name != self.name):
                dist = self.calcDistance(city)
                beta += (city.getInfected()/1E6) * np.exp(-self.z*dist)

        ret = odeint(deriv, y0, t_inter, args=(self.N, beta, gamma))
        S_temp, I_temp, R_temp = ret.T

        self.S = np.concatenate([self.S, S_temp[init:]])
        self.I = np.concatenate([self.I, I_temp[init:]])
        self.R = np.concatenate([self.R, R_temp[init:]])
        lastIndex = len(city.S) - 1

    #distance from the city, using the euler distance
    def calcDistance(self, city):
        def to_rad(grade): return grade * np.pi / 180
        
        # print(city.name)
        # print(self.coords[0])
        # print(city.coords[0])

        x0 = np.cos(to_rad(self.coords[0]))
        x1 = np.cos(to_rad(city.coords[0]))
        y0 = np.sin(to_rad(self.coords[1]))
        y1 = np.sin(to_rad(city.coords[1]))

        dist = np.sqrt(np.abs((x0 - x1))**2 + np.abs((y0 - y1))**2)
        # print(dist, self.name, city.name)
        return dist

    def plotData(self, normalized = False):

        ylabel_text = "Population"

        dem = 1
        if(normalized): 
            dem = self.N
            ylabel_text = "Normalized Population"

        t = np.linspace(0, len(self.S), len(self.S))

        # Plot the data on three separate curves for S(t), I(t) and R(t)
        fig = plt.figure(facecolor='w')
        ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
        ax.set_title(self.name)
        ax.plot(t, self.S/dem, 'b', alpha=0.5, lw=2, label='Susceptible')
        ax.plot(t, self.I/dem, 'r', alpha=0.5, lw=2, label='Infected')
        ax.plot(t, self.R/dem, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
        ax.set_xlabel('Days')
        ax.set_ylabel(ylabel_text)
        ax.yaxis.set_tick_params(length=0)
        ax.xaxis.set_tick_params(length=0)
        ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)
        plt.savefig('plots/{}_plot.png'.format(self.name))
        plt.show()


    def closeAirport(self):
        airport_closed = True

    def calcInitData(self, cities):
        for city in cities:
            dist = self.calcDistance(city)
            self.I[0] += city.occurrences * np.exp(-self.z * dist)
        self.S[0] = self.S[0] - self.I[0]