import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from util import get_country_code, get_city_code, get_restaurant


class Location(BaseModel):
    city: str
    country: str

    model_config = {
        "json_schema_extra": {"examples": [{"city": "Bangalore", "country": "India"}]}
    }


app = FastAPI()


@app.get("/api")
def healthcheck():
    return {"status": "healthy"}


@app.post("/location")
async def location(
    location: Location,
    has_table_booking: bool = False,
    has_online_delivery: bool = False,
    cusines: Union[str, None] = None,
):
    country_code = get_country_code(location.country)
    city_code = get_city_code(location.city)

    # print(has_online_delivery,has_table_booking,cusines)

    if country_code == 0:
        return "Invalid country name"
    elif city_code == 0:
        return "Invalid city name"
    else:
        restaurants = get_restaurant(
            int(city_code),
            int(country_code),
            has_table_booking,
            has_online_delivery,
            cusines,
        )

        if restaurants != 0:
            for restaurant in restaurants:
                restaurant["_id"] = str(restaurant["_id"])

            return restaurants

        else:
            return "No restaurants found matching the given filters"
