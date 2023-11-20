#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd # pandas handles panel data
import json # Allows automatic conversion to json data format
from pymongo import MongoClient #We just want the MongoClient part today
from os.path import join


# # # Structure the Swimming dataset into documents
#  This uses Python to convert a source file csv into a 1:few structure for MongoDB.
#  This program reads the full csv file into a dataframe called df.
#  
# https://data.world/romanian-data/swimming-dataset-top-200-world-times/workspace/data-dictionary
#  The csv has been uploaded into your module in Brightspace.

# ## Understanding your data
# 
# There is a 'data dictionary' of sorts on the original website, but it doesn't tell us enough.

# In[2]:


# Investigate the dataset that you are using.  First, load the dataset.

df = pd.read_csv(join('Swimming Database 2.csv'), encoding='latin-1')
# First, let's check the columns we have and make sure the names 
# are okay and we want all of them.
print("Columns in data frame")
print(df.columns)
# Then print the shape - in this case, the number of rows and columns.
print('DataFrame shape ',df.shape)


# #### In this case, the column names have spaces, so we won't be able to use dot notation.  We'll replace the spaces by "_"

# In[3]:


df.columns = list(map(lambda x: x.replace(" ", "_"), df.columns))


# ### Make sure each attribute has the correct data  type

# In[4]:


df.dtypes


# In[5]:


df[['Event_Name',  'Event_description', 'Team_Code', 'Team_Name', 'Athlete_Full_Name', 'Gender','City', 'Country_Code' ]] =\
df[['Event_Name',  'Event_description', 'Team_Code', 'Team_Name', 'Athlete_Full_Name', 'Gender','City', 'Country_Code' ]].astype("string")


# #### We still have two dates and two times - are the times the same?
# 'Swim_time', 'Swim_date','Athlete_birth_date','Duration_(hh:mm:ss:ff)'

# In[6]:


df[['Swim_time','Duration_(hh:mm:ss:ff)']]


# #### In this case, they're the same.  Normally we could check programmatically, but not today.
# Rename Duration_(hh:mm:ss:ff) to Duration and drop Swim_time.

# In[7]:


df = df.rename(columns={"Duration_(hh:mm:ss:ff)": "Duration"})
df = df.drop(columns=['Swim_time'])


# In[8]:


df.columns


# ## Dates and times
# Json conversion expects strings for dates and times, but the format needs to be correct.  If it is not, convert it to datetime, then back to string.
# 

# In[9]:


df['Athlete_birth_date'].head()


# In[10]:


df['Athlete_birth_date']=pd.to_datetime(df['Athlete_birth_date'],format='%m/%d/%Y').dt.date
df['Athlete_birth_date']=df['Athlete_birth_date'].astype("string")


# In[11]:


df['Athlete_birth_date'].head()


# In[12]:


df['Swim_date']=pd.to_datetime(df['Swim_date'],format='%m/%d/%Y').dt.date
df['Swim_date']=df['Swim_date'].astype("string")


# In[13]:


df.tail(2)


# ### Exploring
#  - Let's look to see how many unique values there are in each column

# In[14]:


print('Unique values')
print(df.nunique())
# Print the top five rows
print('Top 5 rows')
print(df.head(2))
print(df.tail(2))


# ### Promising relationships:
#  - It looks like we could consider grouping under any of the following:
#         - Team Code and Team Name (we should check that they have a 1:1 matching)
#         - Event Name (how does the Event_description correspond to this? Are they related?)
#         - Country and City?  
#         - Athletes and their swims?

# In[15]:


# |Isthere a 1:1 matching between team_code and team_name?
for i in  sorted(df.Team_Code.unique()):
    if len(df[df.Team_Code==i].Team_Name.unique())!=1:
        print(i)


# #### Explore the relationship between event description and event name

# In[16]:


print(df.Event_description.unique())


# In[17]:


for i in sorted(df.Event_description.unique()):
       if len(df[df.Event_description==i].Event_Name.unique())!=1:
        print(i)


# #### Okay, they aren't 1:1.  Let's see what event descriptions are there for each event name

# In[18]:


for i in sorted(df.Event_Name.unique()):
    print('\n', i, '\n', df[df.Event_Name==i].Event_description.unique())


# ## Take one of the groupings and design a collection around it.  

# In[19]:


for i in sorted(df.Athlete_Full_Name.unique()):
     if len(df[df.Athlete_Full_Name==i].Athlete_birth_date.unique())!=1:
        print(i,"Not 1 birth date")
     if len(df[df.Athlete_Full_Name==i].Team_Code.unique())!=1:
        print(i,"Not 1 Team Code", len(df[df.Athlete_Full_Name==i].Team_Code.unique()))
     if len(df[df.Athlete_Full_Name==i].Gender.unique())!=1:
        print(i,"Not 1 Gender")


# In[ ]:





# ### Design
# 
# We will have a 1:few between Athlete and Swim.
# The columns are 'Event_Name', 'Swim_time', 'Swim_date', 'Event_description', 'Team_Code', 'Team_Name', 'Athlete_Full_Name', 'Gender', 'Athlete_birth_date', 'Rank_Order', 'City', 'Country_Code', 'Duration_(hh:mm:ss:ff)'
# 
# If we design one document per athlete, let's take the unique athlete information from:
#     'Athlete_Full_Name', 'Gender', 'Athlete_birth_date'
# 
# We  can then have an embedded array of the athlete's swims, from:
# 'Event_Name', 'Event_description', 'Swim_time', 'Swim_date', 'Team_Code','Team_Name' 'Rank_Order', 'City', 'Country_Code', 'Duration_(hh:mm:ss:ff)'
# 

# #### Json serializable data can't be dates or times.  Let's use the string version of our time.

# In[21]:


print('Event_Name', df.Event_Name.isnull().sum())
print('Event_description', df.Event_description.isnull().sum())
print('Swim_date', df.Swim_date.isnull().sum())
print('Rank_Order', df.Rank_Order.isnull().sum())
print('City', df.City.isnull().sum())
print('Duration', df.Duration.isnull().sum())


# In[22]:


df[df.City.isnull()]


# In[23]:


df["City"].fillna("Not Specified", inplace = True)


# In[24]:


df[['Event_Name', 
    'Event_description', 
    'Swim_date', 
    'Rank_Order', 
    'City', 
    'Country_Code', 
    'Duration']].isnull().values.any()


# ### Extracting the documents

# #### Set up an athlete's dataframe

# In[25]:


adf = df[['Athlete_Full_Name', 'Gender', 'Athlete_birth_date']].drop_duplicates()


# In[26]:


print(adf.Athlete_Full_Name)


# In[27]:


adf.describe(include='all')


# In[28]:


adf.isnull().values.any()


# ### Connect to MongoDB and make a collection

# In[29]:


# #### Set up the database and collection you will use.
uri = 'mongodb://admin:Sp00ky!@localhost:27017/?AuthSource=admin'
client = MongoClient(uri)

mydb = client["Swimming"]
mycol = mydb["Athlete"]
mycol.drop()

#


# #### Loop through each athlete to create a document

# In[30]:


for row in adf.itertuples():
    print(row.Athlete_Full_Name, type(row))
    theirswims = df[df.Athlete_Full_Name==row.Athlete_Full_Name][['Event_Name', 
                                                                  'Event_description', 
                                                                  'Swim_date', 
                                                                  'Team_Code',
                                                                  'Team_Name',
                                                                  'Rank_Order', 
                                                                  'City', 
                                                                  'Country_Code', 
                                                                  'Duration']]
    entries = json.dumps({"Name": row.Athlete_Full_Name,
                          "Birth_Date": row.Athlete_birth_date,
                          "Gender":row.Gender,
                          "Swims": theirswims.to_dict('records')
                             })
    x = mycol.insert_one(json.loads(entries))


# In[32]:


# #### Close the MongoDB connection

client.close()


# In[ ]:





# In[ ]:




