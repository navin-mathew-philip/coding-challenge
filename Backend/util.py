import pandas as pd
from pymongo import MongoClient

client=MongoClient("mongodb://localhost:27017/")
db=client['fastapi_db']


def get_city_code(city:str):
    """
        Retruns the city code from City-Code.csv file
          if city is present
          else returns 0
    """
    
    city_collection=db['city']
    city=city_collection.find_one({"City":city})
    if city:
        return city.get('City Code')
    else:
        return 0

def get_country_code(country:str):
    """
        Returns the country code from Country-Code.csv file
          if country is present
          else returns 0
    """
    country_collection=db['country']
    country=country_collection.find_one({"Country":country})
    if country:

        return country.get('Country Code')
    else:
        return 0


def get_restaurant(
        city_code:int, 
        country_code:int,
        has_table_booking:bool=False,
        has_online_delivery:bool=False,
        cusines:str=None
        ):
    """
        Retruns the restaurant from Restaurant.csv file
          if city_code and country_code are present
          else returns 0
    """

    if has_online_delivery:
        has_online_delivery='Yes'
    else:
        has_online_delivery=''

    if has_table_booking:
        has_table_booking='Yes'
    else:
        has_table_booking=''

    if cusines==None:
        cusines=''
    
    restaurant_collection=db['restaurant']

    query={
            "City Code":city_code, 
            "Country Code":country_code,
            "Has Table booking":{"$regex":has_table_booking,"$options":"i"},
            "Has Online delivery":{"$regex":has_online_delivery,"$options":"i"},
            "Cuisines":{"$regex":cusines,"$options": "i"}
        }
    restaurants=restaurant_collection.find(query).sort("Aggregate rating",-1)
    restaurants=list(restaurants)

    if len(restaurants)!=0:
        # for restaurant in restaurants:
        #     print(restaurant)
        return restaurants
    else:
        return 0
  
  
# res=get_restaurant(2,162,True,False)
# print(res)