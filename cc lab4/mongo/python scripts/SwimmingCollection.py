import pandas as pd # pandas handles panel data
import json # Allows automatic conversion to json data format
from pymongo import MongoClient #We just want the MongoClient part today
from os.path import join
df = pd.read_csv(join('Swimming Database 2.csv'), encoding='latin-1')
# First, let's check the columns we have and make sure the names 
# are okay and we want all of them.
print("Columns in data frame")
print(df.columns)
# Then print the shape - in this case, the number of rows and columns.
print('DataFrame shape ',df.shape)

df.columns = list(map(lambda x: x.replace(" ", "_"), df.columns))

df[['Event_Name',  'Event_description', 'Team_Code', 'Team_Name', 'Athlete_Full_Name', 'Gender','City', 'Country_Code' ]] =\
df[['Event_Name',  'Event_description', 'Team_Code', 'Team_Name', 'Athlete_Full_Name', 'Gender','City', 'Country_Code' ]].astype("string")

df = df.rename(columns={"Duration_(hh:mm:ss:ff)": "Duration"})
df = df.drop(columns=['Swim_time'])

df['Athlete_birth_date']=pd.to_datetime(df['Athlete_birth_date'],format='%m/%d/%Y').dt.date
df['Athlete_birth_date']=df['Athlete_birth_date'].astype("string")

df['Swim_date']=pd.to_datetime(df['Swim_date'],format='%m/%d/%Y').dt.date
df['Swim_date']=df['Swim_date'].astype("string")

edf = df[['Event_Name','Swim_date']].drop_duplicates()

print("Columns in data frame")
print(df.columns)

print(edf.Event_Name)
edf.describe(include='all')
edf.isnull().values.any()

uri = 'mongodb://admin:Sp00ky!@localhost:27017/?AuthSource=admin'
client = MongoClient(uri)

mydb = client["Swimming"]
mycol = mydb["Events"]
mycol.drop()
for row in edf.itertuples():
    Events = df[df.Event_Name==row.Event_Name][['Athlete_Full_Name',  
                                                'Team_Code',
                                                'Team_Name',
                                                'Rank_Order', 
                                                'Country_Code', 
                                                'Duration']]
    entries = json.dumps({"Event": row.Event_Name,
                          "DateSwim": row.Swim_date,
                          "Swims": Events.to_dict('records')
                             })
    x = mycol.insert_one(json.loads(entries))

# #### Close the MongoDB connection

client.close()