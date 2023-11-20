 # Structure city airports in MongoDB
# 
# This uses Python to convert a source file csv into a 1:few structure for MongoDB.
# This program reads the full csv file into a dataframe called df.
# 
# The csv can be found at https://github.com/datasets/airport-codes

import pandas as pd # pandas handles panel data
import json # Allows automatic conversion to json data format

import pymongo # Connectivity package for MongoDB
from pymongo import MongoClient #We just want the MongoClient part today

# Set up the connection to the MongoDB client

uri = 'mongodb://admin:Sp00ky!@localhost:27017/?AuthSource=admin'
client = MongoClient(uri)

# Investigate the dataset that you are using.  In this case, we're using the airports dataset.  This has a list of airports, with their country and city.  We want to represent them in MongoDB as a document for every country.  First, load the data and look at the columns and number of rows.

df = pd.read_csv('airports.csv', sep = ',', delimiter = None,encoding='UTF8')
# First, let's check the columns we have and make sure the names are okay and we want all of them.
print('DataFrame columns')
print(df.columns)
#Then print the shape - in this case, the number of rows and columns.
print('DataFrame shape')
print(df.shape)

print('Number of different countries ')
print(len(df.Country.unique()))

print ('Number of different Time zones ',len(df.Timezone.unique()))

print('Top 20 rows')
# Print the top 20 rows

print(df.head(20))

# ### Extract header information - in this case, Country and City

city = df[['Country', 'City']].drop_duplicates().sort_values(['Country','City'], 
ascending = [True,True])
# Print the shape
print('Shape of header information ',city.shape)

# This means that there are some Country-City combinations with more than one airport. (as 7127 is less than 8107)

print('DataFrame types ',df.dtypes)
print('Top 20 city rows')
print(city.head(20))

# #### Set up the database and collection you will use.

mydb = client["Aviation"]
mycol = mydb["City"]
mycol.drop()

# #### Add a document to the collection for every city (i.e. unique Country - City combination)

for row in city.itertuples():
# The itertuples() function is used to iterate over DataFrame rows as namedtuples.
    thiscity = (df[(df['Country']==row.Country) & (df['City']==row.City)])
    tc = thiscity[['id','Name','IATA_FAA', 'ICAO',
        'latitude','longitude','altitude_ft','Timezone','DST']]
    entries = json.dumps({
            "Country": row.Country,
            "City": row.City,
            "airports":tc.to_dict('records')
            })
                                                 
    x = mycol.insert_one(json.loads(entries))
    


# #### Close the MongoDB connection

client.close()
