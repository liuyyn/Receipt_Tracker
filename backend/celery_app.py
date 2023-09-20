from celery import Celery
from read_receipt import analyze_receipt
from pymongo_get_database import get_database

celery_app = Celery('celery_app', broker='pyamqp://guest@localhost//')

@celery_app.task
def add(x, y):
    return x + y

@celery_app.task
def save_receipt_fields(id, png_image):
    '''
    the function reads the png image and calls the azure api to get the receipt fields and save these fields to the db 
    '''
    db = get_database()
    collection = db.receipt_fields
    fields = analyze_receipt(png_image)
    collection.insert_one({**{"_id": id}, **fields.model_dump()})




