from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/receipts")
async def get_receipts():
    return [{"id": "87bd6bc2-3d4b-11ee-be56-0242ac120002", "cameraScan": ["receipt1"]}, {"id": "95d5396a-3d4b-11ee-be56-0242ac120002", "cameraScan": ["receipt2"]}]
