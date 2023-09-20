from fastapi import FastAPI
from pydantic import BaseModel
from pymongo_get_database import get_database
import os
from read_receipt import analyze_receipt
from utils import compress_image
from celery_app import save_receipt_fields

class Receipt(BaseModel):
    id: str
    cameraScan: list
    content: str = None


app = FastAPI()
db = get_database()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/receipts")
async def get_receipts():
    coll = db.receipt_info
    res = list(coll.find({}))
    final_res = map(lambda x: {"id": x["_id"], "cameraScan": x["cameraScan"]}, res) # returns a map object at some memory location
    # return [{"id": "87bd6bc2-3d4b-11ee-be56-0242ac120002", "cameraScan": ["receipt1"]}, {"id": "95d5396a-3d4b-11ee-be56-0242ac120002", "cameraScan": ["receipt2"]}]
    return list(final_res)

@app.post("/receipts/")
async def post_receipt(receipt: Receipt):
    print(receipt.id)
    # compress the image
    img_data = compress_image(receipt.cameraScan[0])

    data = {
        "_id": receipt.id,
        "cameraScan": [img_data["compressed_img"]],
        "content": receipt.content
    }
    print(type(data["cameraScan"]))
    coll = db.receipt_info
    coll.insert_one(data)

    # read the receipt fields and store in db using celery (we dont need to wait for this to finish - calling the azure service takes some time)
    save_receipt_fields.delay(receipt.id, img_data["png_image"])

    return {"id": receipt.id}    

@app.get("/search")
async def get_search_results(query_str: str):
    '''
    the function should return a list of receipts that match the query_str
    query_str: string to search for
    '''

    query_lst = query_str.split()
    regex_query_lst = list(map(lambda x: f".*{x}.*", query_lst))
    coll = db.receipt_info
    res = list(coll.aggregate([
        {
            "$search": { 
                "index": "default",
                "regex": {
                    "query": regex_query_lst,
                    "path": "content",
                    "allowAnalyzedField": True,
                }
            }
        }
    ]))
    final_res = map(lambda x: {"id": x["_id"], "cameraScan": x["cameraScan"]}, res)

    return list(final_res)

