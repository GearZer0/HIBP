import requests
from urllib.parse import quote


api_key = '' #place api key
user_agent = '' #user agent to be placed
account_list = open('accounts.txt', mode='r', encoding='utf-8').read().split('\n')

headers = {
    'hibp-api-key' : api_key,
    'user-agent': user_agent
}

if __name__ == "__main__":
    for account in account_list:
        if account == "":
            continue
        account = quote(account)
        resp = requests.get('https://haveibeenpwned.com/api/v3/breachedaccount/{}?truncateResponse=false'.format(account),headers=headers).json()
        print(resp)
