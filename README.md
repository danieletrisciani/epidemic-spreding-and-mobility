# Epidemics spreading: modelling & integration with mobility

## About the project
This work aims to simulate the spreading of a virus in Italy (considering cities with inhabitants > 60k). Each city is a node on a network and they are all linked to each other with weighted links, the weight is proportional to how much the virus spread to a city to another. At day 0 the only cities infected are the ones with airports. The simulation lasts for a given number of days. Each day the number of infected, recovered and susceptible inhabitants are updated for each city. The model is deterministic and based on the SIR model, described by the following differential equations:

$$
\begin{aligned}
\frac{d S}{d t} &=-\frac{\beta I S}{N} \\
\frac{d I}{d t} &=\frac{\beta I S}{N}-\gamma I \\
\frac{d R}{d t} &=\gamma I
\end{aligned}
$$

where $S$ is the number of susceptible individuals, $I$ the number of infected individuals and $R$ the recovered. Instead $\beta$ is the rate of infection, and $\gamma$ the recovery rate. $R_0=\beta / \gamma$ is called reproduction number. 
Where $N=I(t)+S(t)+R(t)$ is the total number of inhabitants of a city.

## Used databases

* https://github.com/MatteoHenryChinaski/Comuni-Italiani-2018-Sql-Json-excel/blob/master/italy_cities.json. This database stores some information about italian cities, I used it to get all the cities with a population greater than 60 thousand.
* https://github.com/MatteoHenryChinaski/Comuni-Italiani-2018-Sql-Json-excel/blob/master/italy_geo.json. This database links latitude and longitude to the corresponding city. These informations are used to calculate the distance between the cities to estimate how much a city can influence another city.
* https://openflights.org/data.html. There are two database of interests in there: airports.dat, this database stores some information about all the airport in the world, we are interested in the IATA code that uniquely identifies the airport. routes.dat, that stores all the routes between the airports all over the world using the IATA code. It is used to estimate how the airports in Italy are connected with airports abroad.

Previous databases will be used to create a new database to be used in the simulation:

|     | Name        | Population | Longitude   | Latitude    | Routes |
|-----|-------------|------------|-------------|-------------|--------|
| 0   | Torino      | 872091     | 7.68068748  | 45.0732745  | 44     |
| 1   | Novara      | 101933     | 8.62191588  | 45.44588506 | 0      |
| 2   | Asti        | 74320      | 8.20414255  | 44.89912921 | 0      |
| 3   | Alessandria | 89446      | 8.61540116  | 44.91297351 | 0      |
| 4   | Savona      | 60760      | 8.48110865  | 44.30750461 | 0      |
| ... | ...         | ...        | ...         | ...         | ...    |

## Build with
The following libraries have been used:
* [NetworkX](https://networkx.org/) Cities are considered as nodes of a network, each city has a weighted link to all the other cities. This library helps to manage the complex network.
* [Scipy](https://scipy.org/) Differential equations are solve using the `odeint` equation of the `SciPy` library.


## Usage
Launch:
$ python Italy.py

It will create the database and it will start the simulation.

## Results

Considering a simulation that last 200 days, airports close after 30 days, $\beta = 0.2$ and $\gamma = 1/10$, the SIR model evolution is represented in the plot as follows:

![sir model italy](https://github.com/danieletrisciani/epidemic-spreding-and-mobility/assets/20107065/6e223b49-a3db-497d-bb0a-5491fb84beae)

In the following table are showed the SIR model parameters for the 10 of the most populated cities with more inhabitants at day = 1, indeed the Removed are still 0 for every city.

|     | City    | Population | Susceptible | Infectious | Removed | Airport routes |
|-----|---------|------------|-------------|------------|---------|----------------|
| 0   | Roma    | 2638842    | 2638525     | 317        | 0       | 50             |
| 1   | Milano  | 1262101    | 1261765     | 336        | 0       | 60             |
| 2   | Napoli  | 959052     | 958931      | 121        | 0       | 0              |
| 3   | Torino  | 872091     | 871891      | 200        | 0       | 44             |
| 4   | Palermo | 654987     | 654884      | 103        | 0       | 63             |
| 5   | Genova  | 582320     | 582179      | 141        | 0       | 20             |
| 6   | Bologna | 380635     | 380440      | 195        | 0       | 88             |
| 7   | Firenze | 366039     | 365882      | 157        | 0       | 53             |
| 8   | Bari    | 313213     | 313132      | 81         | 0       | 50             |
| 9   | Catania | 290678     | 290542      | 136        | 0       | 115            |
| ... | ...     | ...        | ...         | ...        | ...     | ...            |

The following SIR model parameters are showed for day 60. It refers to the second peak from the previuos plot.

|     | City    | Population | Susceptible | Infectious | Removed | Airport routes |
|-----|---------|------------|-------------|------------|---------|----------------|
| 0   | Roma    | 2638842    | 680002      | 1056260    | 902580  | 50             |
| 1   | Milano  | 1262101    | 364         | 159578     | 1102159 | 60             |
| 2   | Napoli  | 959052     | 69682       | 445143     | 444227  | 0              |
| 3   | Torino  | 872091     | 497         | 131968     | 739626  | 44             |
| 4   | Palermo | 654987     | 529126      | 65991      | 59870   | 63             |
| 5   | Genova  | 582320     | 419         | 94982      | 486919  | 20             |
| 6   | Bologna | 380635     | 79          | 49564      | 330992  | 88             |
| 7   | Firenze | 366039     | 529         | 59872      | 305638  | 53             |
| 8   | Bari    | 313213     | 65230       | 136943     | 111039  | 50             |
| 9   | Catania | 290678     | 170756      | 53761      | 66161   | 115            |
| ... | ...     | ...        | ...         | ...        | ...     | ...            |

The following table show SIR model variables for day 200, there are no more infected people or few of them, and there are too many immune people for them to grow.

|     | City    | Population | Susceptible | Infectious | Removed | Airport routes |
|-----|---------|------------|-------------|------------|---------|----------------|
| 0   | Roma    | 2638842    | 114741      | 5          | 2524096 | 50             |
| 1   | Milano  | 1262101    | 245         | 0          | 1261856 | 60             |
| 2   | Napoli  | 959052     | 7893        | 1          | 951158  | 0              |
| 3   | Torino  | 872091     | 311         | 0          | 871780  | 44             |
| 4   | Palermo | 654987     | 73564       | 23         | 581400  | 63             |
| 5   | Genova  | 582320     | 250         | 0          | 582070  | 20             |
| 6   | Bologna | 380635     | 51          | 0          | 380584  | 88             |
| 7   | Firenze | 366039     | 308         | 0          | 365731  | 53             |
| 8   | Bari    | 313213     | 6899        | 0          | 306313  | 50             |
| 9   | Catania | 290678     | 26770       | 4          | 263904  | 115            |
| ... | ...     | ...        | ...         | ...        | ...     | ...            |
