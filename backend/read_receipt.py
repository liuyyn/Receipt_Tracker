import requests
import os 
from pydantic import BaseModel
from typing import List
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

class Item(BaseModel):
    description: str = None
    totalPrice: float = 0.0
    quantity: int = 0
    price: float = 0.0
    productCode: str = None
    quantityUnit: str = None

class ReceiptFields(BaseModel):
    merchantName: str = None
    # MerchantAddress: str
    total: float = 0.0
    transactionDate: str = None
    items: List[Item] = []
    subtotal: float = 0.0
    totalTax: float = 0.0

def get_receipt_fields(bytesReceipt):
    '''
    this function calls the azure api to get the receipt fields from a receipt image
    returns the result receipt object from the api
    '''
    # receiptInBytes = base64Receipt.encode() # convert base64 str to bytes
    endpoint=os.getenv("ENDPOINT") 
    key=os.getenv("KEY")
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_analysis_client.begin_analyze_document(
            os.getenv("MODELID"), bytesReceipt)

    return poller.result()

def build_receipt_object(receipts):
    '''
    this function builds a receipt object from the receipts fields object returned by the azure api
    returns the receipt object
    '''
    r = ReceiptFields()
    for _, receipt in enumerate(receipts.documents): 
        merchant_name = receipt.fields.get("MerchantName")
        if merchant_name:
            r.merchantName = merchant_name.value
        # merchant_address = receipt.fields.get("MerchantAddress")
        # if merchant_address:
        #     print(
        #         f"Merchant Address: {merchant_address.value} has confidence: {merchant_address.confidence}"
        #     )
        total = receipt.fields.get("Total")
        if total:
            r.total = total.value
        transaction_date = receipt.fields.get("TransactionDate")
        if transaction_date:
            r.transactionDate = str(transaction_date.value)
        for _, item in enumerate(receipt.fields.get("Items").value):
            new_item = Item()
            item_description = item.value.get("Description")
            if item_description:
                new_item.description = item_description.value
            total_price = item.value.get("TotalPrice")
            if total_price:
                new_item.totalPrice = total_price.value
            quantity = item.value.get("Quantity")
            if quantity:
                new_item.quantity = quantity.value
            price = item.value.get("Price")
            if price:
                new_item.price = price.value
            product_code = item.value.get("ProductCode")
            if product_code:
                new_item.productCode = product_code.value
            quantity_unit = item.value.get("QuantityUnit")
            if quantity_unit:
                new_item.quantityUnit = quantity_unit.value
            r.items.append(new_item)
            
        subtotal = receipt.fields.get("Subtotal")
        if subtotal:
            r.subtotal = subtotal.value
        tax = receipt.fields.get("TotalTax")
        if tax:
            r.totalTax = tax.value
    return r


def analyze_receipt(bytesReceipt):
    
    # get the receipt fields from the azure api
    receipts = get_receipt_fields(bytesReceipt)

    # build the receipt object
    receipt_object = build_receipt_object(receipts)
    
    return receipt_object




