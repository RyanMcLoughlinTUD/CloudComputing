import pandas as pd # pandas handles panel data
import json # Allows automatic conversion to json data format
from pymongo import MongoClient #We just want the MongoClient part today


# # Structure book orders into documents
# 
# This uses Python to convert a source file csv into a 1:few structure for MongoDB.
# This program reads the full csv file into a dataframe called df.
# 
# The csv has been uploaded into your module in Brightspace.

uri = 'mongodb://admin:Sp00ky!@localhost:27017/?AuthSource=admin'
client = MongoClient(uri)

# Investigate the dataset that you are using.  In this case, we have seen the dataset when we explored Data Normalization, so we know there should be a few orders, each with an order heading and orderlines.  First, load the dataset.

df = pd.read_csv('orderrows.csv', encoding='latin-1')
# First, let's check the columns we have and make sure the names 
# are okay and we want all of them.
print("Columns in data frame")
print(df.columns)
# Then print the shape - in this case, the number of rows and columns.
print('DataFrame shape ',df.shape)

print('Unique values')
print(df.nunique())
# Print the top five rows
print('Top 5 rows')
print(df.head())

# Tidy - the ISBN should be a string.  To make it a string, first convert it to
# integer, then to string.
# The ISBN should really be a string:
df['ISBN'] = df['ISBN'].astype('int').astype('string')

# Again, print the data types
print('DataFrame data types')
print(df.dtypes)

# ### Extract header information - in this case, the orderno

orders = df[['orderno']] \
.drop_duplicates() \
.sort_values(['orderno'], 
ascending = [True])
# Print the shape
print('The shape of the DataFrame orders is ',orders.shape)

# This means that there are some orders that have more than one row in the df dataframe (as 3 is less than 12).
print('First 5 orders:')
print(orders.head())

# #### Set up the database and collection you will use.

mydb = client["BookShop"]
mycol = mydb["bookorder"]
mycol.drop()

# #### Add a document to the collection for every order.

for row in orders.itertuples():

    # The itertuples() function is used to iterate over DataFrame rows as
    # named tuples.

    thisorder = (df[(df['orderno']==row.orderno)])
    
    #Some of the information is unique to the order - let's get that first
    orderinfo = thisorder[[
        'custname','email','edate','deladdr',
        'Nett','postage','ordertotal']].drop_duplicates()
    
    # Next, let's extract the embedded array of books:

    bookinfo = thisorder[[
        'Title', 'Author', 'Publisher', 'ISBN', 'cover', 
        'quantity', 'unitprice', 'subtotal', 'image']]
    # Now, let's create a json structure,  embedding the bookinfo 
    # in dictionary format, after tne header information and before the 
    # footer information.
    entries = json.dumps({"orderno": row.orderno,
                              "email":orderinfo['email'].values[0],
                               "edate": orderinfo['edate'].values[0],
                               "custname": orderinfo['custname'].values[0],
                               "deladdr": orderinfo['deladdr'].values[0],
                               "books": bookinfo.to_dict('records'),
                               "Nett": orderinfo['Nett'].values[0],
                               "postage": orderinfo['postage'].values[0],
                               "ordertotal": orderinfo['ordertotal'].values[0]
                             })
    # Now let's write the document to the collection in the database.
                                                 
    x = mycol.insert_one(json.loads(entries))
    


# #### Close the MongoDB connection

client.close()
