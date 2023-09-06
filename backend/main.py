from fastapi import FastAPI
from pydantic import UUID1, BaseModel
from pymongo_get_database import get_database

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
    final_res = map(lambda x: {"id": x["_id"], "cameraScan": x["cameraScan"]}, res)
    # return [{"id": "87bd6bc2-3d4b-11ee-be56-0242ac120002", "cameraScan": ["receipt1"]}, {"id": "95d5396a-3d4b-11ee-be56-0242ac120002", "cameraScan": ["receipt2"]}]
    return list(final_res)

@app.post("/receipts/")
async def post_receipt(receipt: Receipt):
    # TODO save the receipt to the database and return the id
    print(receipt.id)
    data = {
        "_id": receipt.id,
        "cameraScan": receipt.cameraScan,
        "content": receipt.content
    }
    coll = db.receipt_info
    coll.insert_one(data)

    return {"id": receipt.id}