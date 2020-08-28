import requests
from urllib.parse import quote
import csv
import os
import datetime


api_key = ''  # place api key
user_agent = ''  # user agent to be placed
output_file = "out.csv"  # output file to save data
account_list = open('accounts.txt', mode='r',
                    encoding='utf-8').read().split('\n')

headers = {
    'hibp-api-key': api_key,
    'user-agent': user_agent
}


def saveRecords(dataset):
    with open(output_file, mode='a+', encoding='utf-8', newline="") as csvFile:
        fieldnames = ["Email", "Pwned?", "Name",
                      "Breached Domain", "LastPwnedDate"]
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        if os.stat(output_file).st_size == 0:
            writer.writeheader()
        writer.writerow({"Email": dataset[0], "Pwned?": dataset[1], "Name": dataset[2],
                         "Breached Domain": dataset[3], "LastPwnedDate": dataset[4]})


if __name__ == "__main__":
    for account in account_list:
        if account == "":
            continue
        email = account
        account = quote(account)
        pwned = "Yes"
        try:
            resp = requests.get(
                'https://haveibeenpwned.com/api/v3/breachedaccount/{}?truncateResponse=false'.format(account), headers=headers).json()
        except:
            pwned = "No"
            name = ""
            domain = ""
            last_date = ""
            dataset = []
            dataset.append(email)
            dataset.append(pwned)
            dataset.append(name)
            dataset.append(domain)
            dataset.append(last_date)
            for data in dataset:
                print(data)
            print("="*30)
            saveRecords(dataset)
            continue
        last_date = None
        names = []
        domains = []
        for info in resp:
            name = info.get('Name', '')
            domain = info.get('Domain', '')
            names.append(name)
            domains.append(domain)
            if last_date is None:
                last_date = info.get('BreachDate', '')
            else:
                this_date = datetime.datetime.strptime(info.get('BreachDate', last_date),"%Y-%m-%d")
                prev_date = datetime.datetime.strptime(last_date,"%Y-%m-%d")
                if this_date > prev_date:
                    last_date = info.get('BreachDate', last_date)
        name = ",".join(names)
        domain = ",".join(domains)
        dataset = []
        dataset.append(email)
        dataset.append(pwned)
        dataset.append(name)
        dataset.append(domain)
        dataset.append(last_date)
        for data in dataset:
            print(data)
        print("="*30)
        saveRecords(dataset)
