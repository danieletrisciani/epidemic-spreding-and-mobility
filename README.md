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

## Build with
The following libraries have been used:
* [NetworkX](https://networkx.org/) Cities are considered as nodes of a network, each city has a weighted link to all the other cities. This library helps to manage the complex network.
* [Scipy](https://scipy.org/) Differential equations are solve using the `odeint` equation of the `SciPy` library.


## Usage

## Results



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
