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

endpoint=os.getenv("ENDPOINT") 
key=os.getenv("KEY")

async def analyze_receipt(base64Receipt):

    # receiptInBytes = base64Receipt.encode() # convert base64 str to bytes

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_analysis_client.begin_analyze_document(
            "prebuilt-receipt", base64Receipt)
    receipts = poller.result()

    # build the receipt object
    r = ReceiptFields()
    for idx, receipt in enumerate(receipts.documents): 
        print("--------Recognizing receipt #{}--------".format(idx + 1))
        merchant_name = receipt.fields.get("MerchantName")
        if merchant_name:
            r.merchantName = merchant_name.value
            print(
                "Merchant Name: {} has confidence: {}".format(
                    merchant_name.value, merchant_name.confidence
                )
            )
        # merchant_address = receipt.fields.get("MerchantAddress")
        # if merchant_address:
        #     print(
        #         f"Merchant Address: {merchant_address.value} has confidence: {merchant_address.confidence}"
        #     )
        total = receipt.fields.get("Total")
        if total:
            r.total = total.value
            print("Total: {} has confidence: {}".format(total.value, total.confidence))
        transaction_date = receipt.fields.get("TransactionDate")
        if transaction_date:
            r.transactionDate = str(transaction_date.value)
            print(
                "Transaction Date: {} has confidence: {}".format(
                    transaction_date.value, transaction_date.confidence
                )
            )
        for idx, item in enumerate(receipt.fields.get("Items").value):
            new_item = Item()
            print(f"...Item #{idx + 1}")
            item_description = item.value.get("Description")
            if item_description:
                new_item.description = item_description.value
                print(
                    f"......Description: {item_description.value}"
                )
            total_price = item.value.get("TotalPrice")
            if total_price:
                new_item.totalPrice = total_price.value
                print(
                    f"......Total Price: {total_price.value}"
                )
            quantity = item.value.get("Quantity")
            if quantity:
                new_item.quantity = quantity.value
                print(
                    f"......Quantity: {quantity.value}"
                )
            price = item.value.get("Price")
            if price:
                new_item.price = price.value
                print(
                    f"......Price: {price.value}"
                )
            product_code = item.value.get("ProductCode")
            if product_code:
                new_item.productCode = product_code.value
                print(
                    f"......Product Code: {product_code.value}"
                )
            quantity_unit = item.value.get("QuantityUnit")
            if quantity_unit:
                new_item.quantityUnit = quantity_unit.value
                print(
                    f"......Quantity Unit: {quantity_unit.value}"
                )
            r.items.append(new_item)
            
        subtotal = receipt.fields.get("Subtotal")
        if subtotal:
            r.subtotal = subtotal.value
            print("Subtotal: {} has confidence: {}".format(subtotal.value, subtotal.confidence))
        tax = receipt.fields.get("TotalTax")
        if tax:
            r.totalTax = tax.value
            print("Total Tax: {} has confidence: {}".format(tax.value, tax.confidence))
    
    return r
        



def read_receipt(data):
    key=os.getenv("KEY")
    modelID=os.getenv("MODELID")
    endpoint=os.getenv("ENDPOINT") 
    url = endpoint + f"formrecognizer/documentModels/{modelID}:analyze?api-version=2023-07-31"
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": key
    }
    d= {"urlSource": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/receipt.png"}
    response = requests.post(url, headers=headers, data=d)
    print(response.json())
    return response.json()





