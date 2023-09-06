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
    final_res = map(lambda x: {"id": x["_id"], "cameraScan": x["cameraScan"]}, res) # returns a map object at some memory location
    # return [{"id": "87bd6bc2-3d4b-11ee-be56-0242ac120002", "cameraScan": ["receipt1"]}, {"id": "95d5396a-3d4b-11ee-be56-0242ac120002", "cameraScan": ["receipt2"]}]
    return list(final_res)

@app.post("/receipts/")
async def post_receipt(receipt: Receipt):
    print(receipt.id)
    data = {
        "_id": receipt.id,
        "cameraScan": receipt.cameraScan,
        "content": receipt.content
    }
    coll = db.receipt_info
    coll.insert_one(data)

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

