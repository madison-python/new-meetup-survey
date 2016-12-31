#!/usr/bin/env python
"""Download Madpy survey responses as an excel file."""
from os import path
import gspread
import pandas
from oauth2client.service_account import ServiceAccountCredentials


service_account_creds = 'madpy-service-account-key.json'
assert path.exists(service_account_creds), \
       'creds file "%s" not found' % service_account_creds

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    service_account_creds, scopes = 'https://spreadsheets.google.com/feeds',
)

gc = gspread.authorize(credentials)

title = 'MadPy (Responses)'
try:
    ws = gc.open(title).sheet1
except gspread.SpreadsheetNotFound:
    print('spreadsheet %s not found, is it shared with the creds email?' % title)

df = pandas.DataFrame(ws.get_all_records())

# Deidentify data
cols_to_remove = ['Email Address', 'Timestamp', 'Additional comments?']
df.drop(cols_to_remove, axis=1, inplace=True)
df = df.sample(len(df), random_state=1)

df.to_excel('responses-deidentified.xlsx', index=False)
