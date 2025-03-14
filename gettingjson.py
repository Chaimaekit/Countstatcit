from fastapi.responses import JSONResponse
from faker import Faker
from pymongo import MongoClient
from fastapi import FastAPI
import uvicorn
import requests


app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")#changes
db = client["COUNTRIES"]
collection = db["countries"]

url = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/refs/heads/master/json/countries%2Bstates%2Bcities.json"


# def insert_countries():
#  with open('countries.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)
#     for element in data:
#         if collection.find_one("name": element["name"]): 
#             pass
#         else:
#             collection.insert_one(element)

def insert_url_countries(url):
    response = requests.get(url) 
    if response.status_code == 200: 
        data = response.json() 
        for element in data:
            if collection.find_one({"name": element["name"]}):
                pass
            else:
                collection.insert_one(element) 
    else:
        print("Failed to fetch data !!")



@app.get("/showall")
async def show_all():
    documents = collection.find().to_list(None)
    for doc in documents:
        doc["_id"] = str(doc["_id"])
    return {"The countries are ": documents}

@app.get("/search_country/{query}")
async def search_by_name(query: str):
    documents = collection.find({"name": query})
    result = []

    for doc in documents:
        doc["_id"] = str(doc["_id"]) 
        result.append(doc)
    if not result:
        return {"No country found with that name"}
    return JSONResponse(content=result)


@app.get("/check/")
async def search_by_name():
    fake = Faker()
    country = fake.country()
    print(f"searching for {country}")
    documents = collection.find({"name": country})
    result = []

    for doc in documents:
        doc["_id"] = str(doc["_id"]) 
        result.append(doc)
    if not result:
        return {"No country found with that name "}
    return JSONResponse(content=result)


@app.get("/search_state/{query}")
async def search_by_state(query: str):
    documents = collection.find({"states.name": query})
    result = []

    for doc in documents:
        doc["_id"] = str(doc["_id"]) 
        result.append(doc)
    if not result:
        return {"No state found with that name "}
    return JSONResponse(content=result)


@app.get("/search_city/{query}")
async def search_by_city(query: str):
    documents = collection.find({"states.cities.name": query})
    result = []

    for doc in documents:
        doc["_id"] = str(doc["_id"]) 
        result.append(doc)
    if not result:
        return {"No city found with that name "}
    return JSONResponse(content=result)

insert_url_countries(url)

if __name__== "__main__":
    uvicorn.run(app, host="0.0.0.0",port=8080)