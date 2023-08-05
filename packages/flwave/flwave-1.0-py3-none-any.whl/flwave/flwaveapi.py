'''Copyright (c) 2022, Okechukwu Joshua Ifeanyi
All rights reserved.This source code is licensed under the MIT-style license found in the
LICENSE file in the root directory of this source tree.'''

import requests
import secrets
from random import shuffle


#Function to Make Transaction Ref if None is Given
def _make_trxnref(email_address):
    choice_num=secrets.choice([8,10,12])
    text=list(secrets.token_hex(choice_num)+email_address[:email_address.index('@')])
    shuffle(text)
    text=''.join(text)
    return text


def create_transaction(key: str,amount,email: str,redirect_url: str,url: str=None,txn_ref: str=None,currency: str='NGN',name: str=None,\
        phonenumber: int=None,title: str=None,logo: str=None,descriptions: str=None,subaccounts: list=None,payment_options=None,**meta):
   
    '''This function makes a POST request to flutterwave payment API and returns a unique payment link.
    Parameters:

        key: String (Required) This is the Unique Flutterkey Generated on Flutterwave Platform Note: This key should not be exposed for security concerns
            It can be passed from a python ENV
        
        amount: INT (Required) This is the Amount of Money to charge. valid digits between 0-9 including floats are accepted.

        email: (required) This is the Email Address of the Payer .A Mail will be sent to the Customer Email Upon successful Transaction.

        redirect_url: (required) Link to Redirect User to after successful payment Note: This should be a valid link

        url: `This takes A Valid Url for Payment transaction. default: Payment API

        txn_ref: (optional) This is a unique key identifier for every transaction. If this parameter is not passed then it will be auto-generated.

        currency: (optional) default: NGN 


        name: (optional) Payer's Name 

        phonenumber: (optional) Payer's Phone Number 

        Customizations:
            customize the looks of the payment modal. Parameters to set are 
                'title': Name on Payment Modal. It is recommended a name is added, to boost users confidence.
                'logo': Logo on Payment Modal
                'description': Description on Payment Modal
                Note: All parameters are optional

        subaccounts: (optional) List/Arrays/tuples of subaccounts ID to split payment into (For Split Payments) 
                    Visit Flutterwave Documentation for more details on Split Transactions. 
        
        payment_options: (optional) The Payment Options to be Displayed on Payment Modal

        **meta: (optional) Extra Information to store alongside the Transaction e.g 
                customer_id=23,customer_address=10 Downward Avenue

         '''
    if not url:
        url="https://api.flutterwave.com/v3/payments"

    headers={'Authorization': "Bearer "+ key}
    try:
        float(amount)
        json_object={'amount':float(amount),'currency':currency,'redirect_url':redirect_url}
    except ValueError:
        raise ValueError('Cannot Convert '+str(amount)+' To Float')

    if not txn_ref:
        txn_ref=_make_trxnref(email_address=email)
    json_object['tx_ref']=txn_ref      # Add Transaction Ref
    # Create Customer Details
    customer={'email':email}
    if name:
        customer['name']=name
    if phonenumber:
        customer['phonenumber']=int(phonenumber)

    # Create Customizations
    if title or logo or descriptions:
        customizations={}
        if title: customizations['title']=title
        if logo: customizations['logo']=logo
        if descriptions: customizations['descriptions']=descriptions
    else:
        customizations=""


    # Extra Information
    if meta:
        meta=meta
       
    # Building Json Object
    json_object['customer']=customer

    # Adding Sub accounts
    if subaccounts:
        json_object['subaccounts']=subaccounts
    if payment_options:
        json_object['payment_options']=payment_options

    if meta:
        json_object['meta']=meta

    # make Request
    if customizations:
        json_object['customizations']=customizations
    
    response=requests.post(url,headers=headers,json=json_object)

    return response.json()


# Verfify Transaction API

def verify_transaction(key: str,method: str="txn_ref",txn_ref: str=None,txn_id=None,url: str=None):
    
    '''Note:
    This Function Should Only Be Called When a Transaction Has been Initiated and Completed. This API Verifies The Status of A Transaction

    This function makes a GET request to flutterwave verify Transaction API and returns a Dict Containing Details of Transaction.
    Parameters:
        
        key: String (Required) This is the Unique Flutterkey Generated on Flutterwave Platform Note: This key should not be exposed for security concerns
            It can be passed from a python ENV.

        method: (optional) This specifies the method  and url to be used for verification. it can take either of two parameters "txn_ref" or "txn_id"
                possible_parameters="txn_ref","txn_id"
                default="txn_ref"

        txn_ref: (Optional) must be passed if method="txn_ref". This is the Transaction Reference of a Transaction that has been Initiated and completed.

        txn_id: (Optional) must be passed if method="txn_id". This is the Transaction ID of a Transaction that has been Initiated and completed.

        Note: One of `txn_ref` or `txn_id` must be passed to complete transaction. if both is passed. the url used to verify transaction will depend on
              value selected for `method`.
        
        url: `Takes A Valid Url for Payment transaction. default: Transaction_Reference Verification API'''

    if txn_ref or txn_id:
        if (not method or method=='txn_ref') and txn_ref:
            if not url:
                url='https://api.flutterwave.com/v3/transactions/verify_by_reference'
            response=requests.get(url,headers={'Authorization': "Bearer "+key},params={'tx_ref':txn_ref})
        elif method=='txn_ref' and not txn_ref:
            raise Exception("Provide a 'txn_ref' for method='txn_ref'")

        if method=='txn_id' and txn_id:
            if not url:
                url="https://api.flutterwave.com/v3/transactions/"+str(txn_id)+"/verify"
            else:
                url=url.replace(':id',txn_id)
            response=requests.get(url,headers={'Authorization': "Bearer "+key},params={'id':txn_id})
        elif method=='txn_id' and not txn_id:
            raise Exception("Provide a txn_id for method='txn_id' ")
            
        return response.json()
    else:
        raise Exception("One of txn_ref or txn_id must be passed")

def make_refund(key: str,txn_id,amount=None,url: str=None): 
    '''
        Refunds are not enabled by default.To Learn more about refunds visit: https://developer.flutterwave.com/reference/endpoints/transactions/#verify-a-transaction

    This function makes a POST request to make a refund in a disputed Transaction.
    Parameters:
        
        key: String (Required) This is the Unique Flutterkey Generated on Flutterwave Platform Note: This key should not be exposed for security concerns
            It can be passed from a python ENV.
        
        txn_id: (Required) This is the ID of the transaction.

        amount: (Optional) the amount to be refunded, if not set a full refund will be made'''

    txn_id=str(txn_id)

    headers={'Authorization': "Bearer "+ key}

    if not url:
        url='https://api.flutterwave.com/v3/transactions/'+txn_id+'/refund'
    else:
        url=url.replace(':id',txn_id)

    if amount:
        try:
            float(amount)
        except ValueError:
            raise ValueError('Cannot Convert '+str(amount)+' to Float')

        amount=float(amount)
        json_object={}
        json_object['amount']=amount

        response=requests.post(url=url,headers=headers,json=json_object)

        return response.json()
    else:
        response=requests.post(url=url,headers=headers)

        return response.json()


def transaction_details(key: str,url: str=None,date_start: str=None,date_end: str=None,page=None,customer_email: str=None,status: str=None,tx_ref:str=None,customer_fullname: str=None,currency: str="NGN"):
    
    '''key:(Required) Unique Secret Key for Flutterwave API
    
    url: (Optional) This Uses the Multiple_transaction API by default

    from:(Optional) Date To start Query.   format: "YYYY-MM-DD" e.g "2022-01-01"

    to: (optional) Date to End Query.  Format: "YYYY-MM-DD" e.g "2022-03-01"

    page:(Optional) The Specific Page to Extract : e.g "1"

    customer_email: (Optional) Customer email. Used to query transaction for a specific User

    status:(Optional) Status of Transaction (Can be Used for filter transactions) options: "successful" , "failed"

    tx_ref: (optional) Unique Reference for a single transaction. This is used to Query details of a single transaction

    customer_fullname: (optional) The First and Last Name of the Customer who made the transaction

    currency: (optional) default="NGN" '''

    args=vars().items()

    if not url:
        url="https://api.flutterwave.com/v3/transactions"

    headers={'Authorization': "Bearer "+key}
    params={}

    for parameter,item in args:
        if item:
            if parameter=='date_start':
                params['from']=item
            elif parameter=='date_end':
                params['to']=item
            elif parameter=='key':
                continue
            else:
                params[parameter]=item

    response=requests.get(url=url,headers=headers,params=params)
    return response.json()
