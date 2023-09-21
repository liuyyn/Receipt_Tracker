from celery import Celery
from celery.schedules import crontab
from read_receipt import analyze_receipt
from pymongo_get_database import get_database
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64



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

@celery_app.task
def send_weekly_email():
    '''
    the function sends an email to the user with the weekly summary of their receipts
    '''
    # get the receipts from the last week
    db = get_database()
    collection = db.receipt_fields
    end_date = datetime.now()
    # start_date = end_date - timedelta(days=7)
    start_date = datetime(2023, 7, 3)
    query = {
        'transactionDate': {
            '$gte': start_date,
            '$lt': end_date
        }
    }
    results = list(collection.find(query))

    # retrieve total price for each receipt to record the total price
    total = 0
    for receipt in results:
        total += receipt['total'] 

    # get credentials for gmail api
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('gmail', 'v1', credentials=creds)

    # send the email with the total amount spent last week
    # CONSTANTS
    recipient_email = 'yuyunliu@hotmail.com'  
    subject = 'Your Weekly Receipts Summary!'
    email_body = f"Your weekly receipts summary is here! You spent ${total} last week."

    # build the email content
    message = MIMEText(email_body)
    message['to'] = recipient_email
    message['subject'] = subject
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        print('Email sent successfully!')
    except Exception as e:
        print(f'Email sending failed: {str(e)}')
        message = None

@celery_app.on_after_configure.connect
def setup_periodic_email_task(sender, **kwargs):
    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        # crontab(hour=7, minute=30, day_of_week=1),
        crontab(),
        send_weekly_email.s(),
        name="send weekly receipts summary email"
    )


