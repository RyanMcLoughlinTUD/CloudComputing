import pandas as pd # pandas handles panel data
import json # Allows automatic conversion to json data format
import pymongo
from pymongo import MongoClient #We just want the MongoClient part today
from os.path import join


# taking in data

df = pd.read_csv(join('CarDeets.csv'), encoding='latin-1')
# First, let's check the columns we have and make sure the names 
# are okay and we want all of them.
print("Columns in data frame")
print(df.columns)
# Then print the shape - in this case, the number of rows and columns.
print('DataFrame shape ',df.shape)

df.columns = list(map(lambda x: x.replace(" ", "_"), df.columns))

df[['name',  'year', 'selling_price', 'km_driven', 'fuel', 'seller_type','transmission', 'owner' ]] =\
df[['name',  'year', 'selling_price', 'km_driven', 'fuel', 'seller_type','transmission', 'owner' ]].astype("string")



# forming the data into tables
uri = 'mongodb://admin:Sp00ky!@localhost:27017/?AuthSource=admin'
client = MongoClient(uri)

mydb = client["CarDetails"]
mycol = mydb[""]
mycol.drop()

for row in df.itertuples():
    Cars = df[df.name==row.name][[              
                                                'name',  
                                                'selling_price',
                                                'km_driven',
                                                'fuel',
                                                'transmission', 
                                                'seller_type', 
                                                'owner']]
    entries = json.dumps({
                            "Year": row.year,
                            "Cars Available from year": Cars.to_dict('records')
                            })
    x = mycol.insert_one(json.loads(entries))

# #### Close the MongoDB connection

client.close()