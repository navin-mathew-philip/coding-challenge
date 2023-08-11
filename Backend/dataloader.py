from pymongo import MongoClient
import pandas as pd

client=MongoClient("mongodb://localhost:27017/")
db=client['fastapi_db']
country_collection=db['country']
city_collection=db['city']
restaurant_collection=db['restaurant']

country_df=pd.read_csv('/home/dxuser/backend/app/data/Country-Code.csv')
city_df=pd.read_csv('/home/dxuser/backend/app/data/City-Code.csv')
restaurant_df=pd.read_csv('/home/dxuser/backend/app/data/restaurants.csv',encoding='latin1')

country_data = country_df.to_dict(orient="records")
city_data=city_df.to_dict(orient="records")
restaurant_data=restaurant_df.to_dict(orient="records")

def load_data_to_db(data,collection,unique_field):

    for entry in data:
        existing_entry = collection.find_one({unique_field: entry[unique_field]})
        if existing_entry is None:
            collection.insert_one(entry)
            print(f"Inserted: {entry}")
        else:
            print(f"Duplicate skipped: {entry}")

    print("Data inserted into MongoDB successfully.")

load_data_to_db(country_data,country_collection,"Country Code")
load_data_to_db(city_data,city_collection,"City Code")
load_data_to_db(restaurant_data,restaurant_collection,"Restaurant ID")


client.close()

