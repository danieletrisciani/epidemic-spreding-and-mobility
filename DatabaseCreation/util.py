import pandas as pd
import numpy as np

data_folder = "../databases/"

def generateDB(cities_df):
    #read and compute data of airports and routes

    airports_df = pd.read_csv(data_folder + "Airports.csv", usecols=[0, 3, 4, 6, 7], header=None)
    airports_df.columns = ["Code", "State", "AirCode", "Latitude", "Longitude"]
    airports_df = airports_df.set_index('Code')
    it_airports_df = airports_df[airports_df['State'] == 'Italy']
    it_airports_df = it_airports_df[airports_df['AirCode'] != '\\N']
    it_airports_df.reset_index(drop=True, inplace=True)

    routes_df = pd.read_csv(data_folder + "Routes.csv", usecols=[2, 4], header=None)
    routes_df.columns = ["Departure", "Destinations"]

    #rows of the routes database that consider italian airport are deleted
    i = 0
    index_to_remove = []
    for index_routes, row_routes in routes_df.iterrows():
        remove = True
        for index_air, row_air in it_airports_df.iterrows():
            if(row_air["AirCode"] == row_routes["Departure"]):
                remove = False
                break

        if(remove): index_to_remove.append(index_routes)
        i += 1
        if(i % 200 == 0): print(i)

    routes_df = routes_df.drop(index_to_remove)

    cities = []
    occ = []
    for index_air, row_air in it_airports_df.iterrows():
        distance = 1000
        cities.append('')
        occ.append(0)
        #calculation of the city the own the airport based on the distance of geographic coordinates
        for index_city, row_city in cities_df.iterrows():
            latitude = row_city['Latitude'] - row_air['Latitude']
            longitude= row_city['Longitude'] - row_air['Longitude']
            temp = np.sqrt(latitude**2 + longitude**2)
            
            if(distance > temp):
                distance = temp
                cities[index_air] = row_city['Name']

        #calculations of the number of departures from airports
        for index_routes, row_routes in routes_df.iterrows():
            if(row_air["AirCode"] == row_routes["Departure"]):
                occ[index_air] += 1

    #avoid that there are multiple occurrence with the same name
    cities_ex = []
    occ_ex = []

    for i in range(len(cities)):
        if(not (cities[i] in cities_ex)):
            cities_ex.append(cities[i])
            occ_ex.append(occ[i])
        else:
            index = cities_ex.index(cities[i])
            print(occ[i])
            occ_ex[index] = occ_ex[index] + occ[i]


    print(len(occ_ex))
    city_occ_df = pd.DataFrame({'City': cities_ex, 'Occurrence': occ_ex})

    #save on file
    city_occ_csv = city_occ_df.to_csv()

    with open(data_folder + "temp.csv", 'w', encoding='utf-8') as f:
        f.write(city_occ_csv)
        f.close()

    return city_occ_df