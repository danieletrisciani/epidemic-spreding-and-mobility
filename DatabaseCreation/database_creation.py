import pandas as pd
import numpy as np

from util import generateDB

fileAlreadyExist = True

data_folder = "../databases/"

#read and merge of data of population and geographic coordinantes
popo_df = pd.read_csv(data_folder + "italy_cities.csv", sep='\t', usecols=[0, 1, 7], header=None)
popo_df.columns = ["Code", "Name", "Population"]
popo_df = popo_df.set_index("Code")
big_pop_df = popo_df[popo_df['Population'] > 60000]

geo_column = ["Code", "Name", "Longitude", "Latitude"]
geo_df = pd.read_csv(data_folder + "italy_geo.csv", sep='\t', names=geo_column)
geo_df = geo_df.set_index("Code")

index_to_remove = []
for index, row in geo_df.iterrows():
    if(not (index in big_pop_df.index)):
        index_to_remove.append(index)

big_geo_df = geo_df.drop(index_to_remove)

cities_df = pd.merge(big_pop_df, big_geo_df)

if(not fileAlreadyExist):

    city_occ_df = generateDB(cities_df)
else:
    city_occ_df = pd.read_csv(data_folder + "temp.csv", index_col = 0)

final_df = cities_df.merge(city_occ_df, left_on='Name', right_on='City', how='outer')

#The city column is useless now
final_df = final_df.drop('City', axis=1)

for index, row in final_df.iterrows():
    if(np.isnan(row['Occurrence'])): 
        print('ciao')
        final_df.Occurrence[index] = 0

#save the complete database on file
final_csv = final_df.to_csv()

with open(data_folder + "allinfo.csv", 'w', encoding='utf-8') as f:
    f.write(final_csv)
    f.close()

print(cities_df.head(5))
print("\n")
print(city_occ_df.head(5))
print("\n")
print(final_df.head(5))
print("\n")
