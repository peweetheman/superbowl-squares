import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
from api_keys import org_id, api_key 

url = "https://api.neoncrm.com/v2/donations"

def submit_donation(batch_number, donor_name, account_id, donation_amount, credit_card_token, email, billing_address):
    # Construct the donation object
    current_utc_datetime = datetime.utcnow()

    donation_data = {
        "batchNumber": batch_number,
        "donorName": donor_name,
        "accountId": account_id,
        "date": current_utc_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        "sendAcknowledgeEmail": False,
        "amount": donation_amount,
        "anonymousType": True,
        "sendAcknowledgeLetter": False,
        "donorCoveredFeeFlag": False,
        "purpose": {
            "id": "string",
            "name": "string",
            "status": "ACTIVE"
        },
        "source": {
            "id": "string",
            "name": "string",
            "status": "ACTIVE"
        },
        "campaign": {
            "id": "string",
            "name": "string",
            "status": "ACTIVE"
        },
        "donorCoveredFee": 0,
        "solicitationMethod": {
            "id": "string",
            "name": "string",
            "status": "ACTIVE"
        },

        "payments": [
            {
                "amount": donation_amount,
                "paymentStatus": "Pending",
                "note": "Donation made via online credit card",
                "tenderType": 0, # Update this with the correct code for online credit card payments
                "receivedDate": "2024-02-24T01:32:32.873Z",
                "creditCardOnline": {
                    "token": credit_card_token,
                    "cardHolderEmail": email,
                    "billingAddress": billing_address
                }
                # Exclude other payment methods like creditCardOffline, ach, check, wire, inKind
            }
        ],
        "fundraiserAccountId": "N/A",
    }
    example_json = {
    "batchNumber": "string",
    "donorName": "string",
    "id": "string",
    "accountId": "string",
    "date": "2024-02-24T02:46:57.216Z",
    "sendAcknowledgeEmail": True,
    "amount": 0,
    "anonymousType": "No",
    "sendAcknowledgeLetter": True,
    "donorCoveredFeeFlag": True,
    "purpose": {
        "id": "string",
        "name": "string",
        "status": "ACTIVE"
    },
    "source": {
        "id": "string",
        "name": "string",
        "status": "ACTIVE"
    },
    "campaign": {
        "id": "string",
        "name": "string",
        "status": "ACTIVE"
    },
    "donorCoveredFee": 0,
    "solicitationMethod": {
        "id": "string",
        "name": "string",
        "status": "ACTIVE"
    },
    "acknowledgee": {
        "accountId": "string",
        "name": "string",
        "email": "patrickwillwin@gmail.com",
        "address": {
        "addressId": "string",
        "isPrimaryAddress": True,
        "type": {
            "id": "string",
            "name": "string",
            "status": "ACTIVE"
        },
        "validAddress": True,
        "addressLine1": "string",
        "startDate": "string",
        "addressLine2": "string",
        "endDate": "string",
        "addressLine3": "string",
        "city": "string",
        "stateProvince": {
            "code": "string",
            "name": "string",
            "status": "ACTIVE"
        },
        "country": {
            "id": "string",
            "name": "string",
            "status": "ACTIVE"
        },
        "territory": "string",
        "county": "string",
        "zipCode": "string",
        "zipCodeSuffix": "string",
        }
    },
    "fund": {
        "id": "string",
        "name": "string",
        "status": "ACTIVE"
    },
    "payLater": True,
    "payments": [
        {
        "id": "string",
        "amount": 0,
        "paymentStatus": "Pending",
        "note": "string",
        "tenderType": 0,
        "receivedDate": "2024-02-24T02:46:57.216Z",
        "creditCardOnline": {
            "token": "string",
            "cardHolderEmail": "patrickwillwin@gmail.com",
            "billingAddress": {
                "addressLine1": "string",
                "addressLine2": "string",
                "city": "string",
                "stateProvinceCode": "string",
                "territory": "string",
                "countryId": "string",
                "zipCode": "string",
                "zipCodeSuffix": "string"
            }
        }
        }
    ],
    "tribute": {
        "name": "string",
        "type": "Honor"
    },
    "fundraiserAccountId": "string",
    "craInfo": {
        "advantageAmount": 0,
        "advantageDescription": "string"
    },
    "taxDeductibleInfo": {
        "nonDeductibleAmount": 0,
        "nonDeductibleDescription": "string"
    },
    "origin": {
        "originDetail": "string",
        "originCategory": "string"
    }
    }

    
    headers = {
        "Content-Type": "application/json",
    }

    # Use the HTTPBasicAuth class for basic authentication
    auth = HTTPBasicAuth(org_id, api_key)

    # Make the POST request with basic authentication
    response = requests.post(url, auth=auth, headers=headers, json=example_json)
    
    if response.status_code == 200:
        print("Donation submitted successfully.")
        return response.text
    else:
        print(f"Failed to submit donation. Status code: {response.status_code}")
        return response.text

# For the sake of brevity, only placeholders are provided for most parameters
donation_response = submit_donation(
    batch_number="some_batch_number",
    donor_name="John Doe",
    account_id="some_account_id",
    donation_amount=100,
    credit_card_token="dsfaafsd",
    email="patrickwillwin@gmail.com",
    billing_address="123 abc st"
)

print(donation_response)