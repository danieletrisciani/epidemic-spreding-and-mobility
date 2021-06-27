import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import math

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

        self.S = [self.N - self.occurrences]
        self.I = [self.occurrences]
        self.R = [0]

    def update(self, cities, beta, gamma, delta_t, t):

        if(t == 0):
            init = 0
        else:
            init = 1
            
        t_inter = np.linspace(t, t + delta_t, 2)

        y0 = self.S[len(self.S) - 1], self.I[len(self.I) - 1], self.R[len(self.R) - 1]

        # cities that host an airport has bigger beta than others
        if(self.airport_opened and self.occurrences != 0):
            beta = (self.occurrences / 200) + beta

        for city in cities:
            if(city.name != self.name):
                dist = self.calcDistance(city)
                beta += (city.occurrences / 1E4) * math.exp(- dist)

        ret = odeint(deriv, y0, t_inter, args=(self.N, beta, gamma))
        S_temp, I_temp, R_temp = ret.T

        self.S = np.concatenate([self.S, S_temp[init:]])
        self.I = np.concatenate([self.I, I_temp[init:]])
        self.R = np.concatenate([self.R, R_temp[init:]])

    def calcDistance(self, city):
        dist = np.sqrt((self.coords[0] - city.coords[0])**2 + (self.coords[1] - self.coords[1])**2)
        # print(dist, self.name, city.name)
        return dist

    def plotData(self):

        t = np.linspace(0, len(self.S), len(self.S))

        # Plot the data on three separate curves for S(t), I(t) and R(t)
        fig = plt.figure(facecolor='w')
        ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
        ax.plot(t, self.S/self.N, 'b', alpha=0.5, lw=2, label='Susceptible')
        ax.plot(t, self.I/self.N, 'r', alpha=0.5, lw=2, label='Infected')
        ax.plot(t, self.R/self.N, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
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


    def closeAirport(self):
        airport_closed = True

    def calcInitData(self, cities):
        for city in cities:
            if(self.name != city.name):
                dist = self.calcDistance(city)
                self.I[0] += city.occurrences * math.exp(-dist)