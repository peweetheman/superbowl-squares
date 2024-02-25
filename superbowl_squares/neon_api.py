import requests
from datetime import datetime
from django.conf import settings  # Assuming your Neon CRM credentials are stored in settings
from api_keys import org_id, api_key 

def create_donation(first_name, last_name, email, amount, card_number, expiration_month, expiration_year, card_type, cvv2, card_holder):    
    url = "https://api.neoncrm.com/neonws/services/api/donation/createDonation"
    session_id=get_neoncrm_session_key()
    params = {
        "responseType": "json",
        "userSessionId": session_id,
        "donation.accountId": get_create_account_id(session_id, first_name, last_name, email),
        "donation.amount": amount,
        "donation.campaign.name": "Superbowl Squares 2025",
        "Payment.amount": amount,
        "donation.date": datetime.now().strftime("%Y-%m-%d"),
        "Payment.tenderType.id": 4,  # Assuming this is a constant for credit card payments
        "Payment.creditCardOnlinePayment.cardNumber": card_number,
        "Payment.creditCardOnlinePayment.expirationMonth": expiration_month,
        "Payment.creditCardOnlinePayment.expirationYear": expiration_year,
        "Payment.creditCardOnlinePayment.cardType.name": card_type,
        "Payment.creditCardOnlinePayment.CVV2": cvv2,
        "Payment.creditCardOnlinePayment.cardHolder": card_holder,
        "Payment.creditCardOnlinePayment.cardHolderEmail": email
    }
    
    response = requests.post(url, params=params)
    
    if response.status_code == 200:
        # Assuming the API returns a JSON response
        transaction_status = response.json()["createDonation"]["transaction"]["transactionStatus"]
        print(transaction_status)
        return transaction_status == "SUCCEED"

    else:
        # Handle errors or unsuccessful requests
        return {"error": "Request failed with status code {}".format(response.status_code)}


# Function to extract account id from the API response
def extract_account_id(search_results):
    for result in search_results.get("nameValuePairs", []):
        for pair in result.get("nameValuePair", []):
            if pair.get("name") == "Account ID":
                return pair.get("value")
    return None

# Function to perform search
def search_account(params):
    base_url = "https://api.neoncrm.com/neonws/services/api/account/listAccounts"
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        response_data = response.json()
        accounts = response_data.get("listAccountsResponse", {}).get("searchResults", {})
        if accounts:
            account_id = extract_account_id(accounts)
            if account_id:
                return account_id
    return None

def get_create_account_id(session_id, first_name, last_name, email):
    create_account_url = "https://api.neoncrm.com/neonws/services/api/account/createIndividualAccount"

    # Search by Email
    params_email = [
        ("responseType", "json"),
        ("outputfields.idnamepair.id", ""),
        ("outputfields.idnamepair.name", "Account ID"),
        ("userSessionId", session_id),
        ("searches.search.key", "Email"),
        ("searches.search.searchOperator", "EQUAL"),
        ("searches.search.value", email),
    ]
    account_id = search_account(params_email)

    # If no account found by email, try to find by first name and last name
    if not account_id:
        params = [
            ("responseType", "json"),
            ("outputfields.idnamepair.id", ""),
            ("outputfields.idnamepair.name", "Account ID"),
            ("userSessionId", session_id),
            ("searches.search.key", "First Name"),
            ("searches.search.searchOperator", "EQUAL"),
            ("searches.search.value", first_name),
            ("searches.search.key", "Last Name"),
            ("searches.search.searchOperator", "EQUAL"),
            ("searches.search.value", last_name),
        ]
        account_id = search_account(params)
    
    # If still no account found, create a new one
    if not account_id:
        create_params = {
            "userSessionId": session_id,
            "individualAccount.primaryContact.firstName": first_name,
            "individualAccount.primaryContact.lastName": last_name,
            "individualAccount.primaryContact.email1": email,
        }
        response = requests.post(create_account_url, params=create_params)
        if response.status_code == 200:
            response_data = response.json()
            # Correctly parsing the account ID from the create account response
            account_id = response_data.get("createIndividualAccountResponse", {}).get("accountId")
            if account_id:
                print(f"Created new account with ID: {account_id}")
            else:
                print("Account creation successful, but could not parse account ID.")
        else:
            print(f"Failed to create account. Status code: {response.status_code}, Response: {response.text}")
    
    print("account id: ", account_id)
    return account_id

    
def get_neoncrm_session_key():
    url = "https://api.neoncrm.com/neonws/services/api/common/login"
    params = {
        "login.apiKey": api_key,
        "login.orgid": org_id
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        # Parse the JSON response to extract the userSessionId
        response_data = response.json()
        if response_data.get("loginResponse", {}).get("operationResult") == "SUCCESS":
            session_key = response_data["loginResponse"]["userSessionId"]
            print("Login successful. Session ID:", session_key)
            return session_key
        else:
            print("Login failed:", response_data.get("loginResponse", {}).get("responseMessage"))
            return None
    else:
        print("Request failed with status code", response.status_code)
        return None

if __name__ == "main":
    # Example usage
    x = create_donation(
        first_name="patrick",
        last_name="phillips",
        email="patrickwillwin@gmail.com",
        amount=1.00,
        card_number="4444111111111111",
        expiration_month="01",
        expiration_year="2020",
        card_type="Visa",
        cvv2="999",
        card_holder="Example Person"
    )
    print(x)