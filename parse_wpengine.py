# Account ID, Account Name, First Name, and Created On
# Restful Status API: http://interview.wpengine.io/v1/accounts/{account_id}
# {"account_id": 12345, "status": "good", "created_on": "2011-01-12"}

import pandas as pd
from pandas.io.json import json_normalize
import json
from pandas import read_excel
import requests
import csv
import sys

input_filename = sys.argv[1]
output_filename = sys.argv[2]

wpengine_url = 'http://interview.wpengine.io/v1/accounts/'

def load_xlsx():
    # find your sheet name at the bottom left of your excel file and assign 
    # it to my_sheet 
    my_sheet = 0 # change it to your sheet name
    file_name = input_filename #'input.xlsx' # change it to the name of your excel file
    df = read_excel(file_name, sheet_name = my_sheet)
    dict_df = df.set_index('Account ID').T.to_dict('list')
    # print(dict_df) #Eg: {12345: ['lexcorp', 'Lex', Timestamp('2011-01-12 00:00:00')]}
    return dict_df

def query_api(dict_df):
    dict_query_api = {}
    for each_account in dict_df:
        # print(each_account)
        account_wpengine_url = wpengine_url + str(each_account) #Example: http://interview.wpengine.io/v1/accounts/12345
        # print(account_wpengine_url)

        response = requests.get(account_wpengine_url)
        if str(response.status_code) == "200":
            # print(response.json()) #Eg: {'account_id': 88888, 'status': 'collections', 'created_on': '2015-08-08'}
            dict_query_api[each_account] = response.json()
    return dict_query_api

        # OLD FILE: Account ID, Account Name, First Name, and Created On
        # NEW FILE: Account ID, First Name, Created On, Status, and Status Set On
        # DATA FROM API:  Account ID, Status, Created On
        # DATA FROM XLSX: Account ID, Account Name, First Name, and Created On


def merge_files(dict_df,dict_query_api):
    l2=[]
    for i,j in dict_df.items():
        for k,v in dict_query_api.items():
            if i==k:
                l1=[i,j[1],str(j[2]).split(" ")[0],str(j[2]).split(" ")[0],v['status']]
                l2.append(l1)
    return l2

def print_dict_merged_data_from_csv_and_api_to_new_xls_file(dict_merged_data_from_csv_and_api):
    # with open('output.csv', 'w+') as output:
    with open(output_filename, 'w+') as output:
        writer = csv.writer(output)
        for key, value in dict_merged_data_from_csv_and_api.items():
            df = pd.DataFrame(value)
            df.to_excel('./states.xlsx', sheet_name='States', index=False)

def write_to_file(dict_data):
    fields=['Account ID','First Name','Created On','Status','Status Set On']
    lines=[]
    for k,v in dict_data.items():
        # print(v)
        line=str(v).strip("{").strip("}")
        a=line.split(",")[0].split(":")[1]
        f=line.split(",")[1].split(":")[1].split("'")[1]
        c=line.split(",")[2].split(":")[1].split("'")[1].split(" ")[0]
        s=line.split(",")[4].split(":")[1].split("'")[1]
        line2=[a,f,c,c,s]
        lines.append(line2)

    # with open('output.csv', 'w') as f:
    with open(output_filename, 'w') as f:
        cw=csv.writer(f)
        cw.writerow(fields)
        cw.writerows(lines)


def write_to_file(l1):
    fields=['Account ID','First Name','Created On','Status','Status Set On']
    # print(l1)
    # with open('output.csv', 'w') as f:
    with open(output_filename, 'w') as f:
        cw=csv.writer(f)
        cw.writerow(fields)
        cw.writerows(l1)



dict_df = load_xlsx()     # print(dict_df) # Eg: {ACCOUNT_ID: ['ACCOUNT_NAME', 'FIRST_NAME', CREATED_ON]} ---> {12345: ['lexcorp', 'Lex', Timestamp('2011-01-12 00:00:00')]
dict_query_api = query_api(dict_df)
l1=merge_files(dict_df,dict_query_api)
write_to_file(l1)
