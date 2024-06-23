from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId


app = FastAPI()

# DataBase Connection
mongo_url = "mongodb://localhost:27017/"
client = MongoClient(mongo_url)
db = client.Fast_API
collection = db.fast_api_collection

# Using PyDantic Modoel for the Schema/structure of the Document


class Item(BaseModel):
 name: Optional[str] = None
 prof: Optional[str] = None
 home_town: Optional[str] = None
 interests: Optional[str] = None


@app.get("/", response_model=List[Item])
def get_all_items():
 items = list(collection.find())
 return items


@app.post("/", response_model=Item)
def create_new_list(data: Item):
 collection.insert_one(data.dict())

 return data


@app.patch("/{item_id}", response_model=Item)
def update_one_document(item_id: str, data: Item):

 updated_item = collection.find_one_and_update(
     {"_id": ObjectId(item_id)},
     {"$set": data.dict(exclude_unset=True)},
     return_document=True
 )

 return updated_item


@app.delete("/{item_id}")
def delete_one_item(item_id: str):

 deleted_item = collection.find_one_and_delete(
     {"_id": ObjectId(item_id)}
 )

 if deleted_item == None:
  raise HTTPException(status_code=404, detail="Item Not Found")

 return {"message": "Item is delete!"}


# @app.delete("/{item_id}")
# def delete_one_item(item_id: str):

#  deleted_item = collection.delete_one(
#      {"_id": ObjectId(item_id)}
#  )
#  print(deleted_item)

#  if deleted_item.deleted_count == 0:
#   raise HTTPException(status_code=404, detail="Item Not Found")

#  return {"message": "item is deleted"}
