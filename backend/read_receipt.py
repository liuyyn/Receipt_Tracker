import requests
import os 
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

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

    for idx, receipt in enumerate(receipts.documents): 
        print("--------Recognizing receipt #{}--------".format(idx + 1))
        merchant_name = receipt.fields.get("MerchantName")
        if merchant_name:
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
            print("Total: {} has confidence: {}".format(total.value, total.confidence))
        transaction_date = receipt.fields.get("TransactionDate")
        if transaction_date:
            print(
                "Transaction Date: {} has confidence: {}".format(
                    transaction_date.value, transaction_date.confidence
                )
            )
        for idx, item in enumerate(receipt.fields.get("Items").value):
            print(f"...Item #{idx + 1}")
            item_description = item.value.get("Description")
            if item_description:
                print(
                    f"......Description: {item_description.value}"
                )
            total_price = item.value.get("TotalPrice")
            if total_price:
                print(
                    f"......Total Price: {total_price.value}"
                )
            quantity = item.value.get("Quantity")
            if quantity:
                print(
                    f"......Quantity: {quantity.value}"
                )
            price = item.value.get("Price")
            if price:
                print(
                    f"......Price: {price.value}"
                )
            product_code = item.value.get("ProductCode")
            if product_code:
                print(
                    f"......Product Code: {product_code.value}"
                )
            quantity_unit = item.value.get("QuantityUnit")
            if quantity_unit:
                print(
                    f"......Quantity Unit: {quantity_unit.value}"
                )
            
        subtotal = receipt.fields.get("Subtotal")
        if subtotal:
            print("Subtotal: {} has confidence: {}".format(subtotal.value, subtotal.confidence))
        tax = receipt.fields.get("TotalTax")
        if tax:
            print("Total Tax: {} has confidence: {}".format(tax.value, tax.confidence))
        



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





