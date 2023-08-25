from fastapi import FastAPI
from pydantic import BaseModel

class Receipt(BaseModel):
    id: str
    cameraScan: list

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/receipts")
async def get_receipts():
    return [{"id": "87bd6bc2-3d4b-11ee-be56-0242ac120002", "cameraScan": ["receipt1"]}, {"id": "95d5396a-3d4b-11ee-be56-0242ac120002", "cameraScan": ["receipt2"]}]

@app.post("/receipts/")
async def post_receipt(receipt: Receipt):
    # TODO save the receipt to the database and return the id
    print(receipt.id)
    return receipt.id