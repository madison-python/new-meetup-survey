#!/usr/bin/env python
"""Download Madpy survey responses and deidentify them before saving to csv."""
from os import path
import gspread
import pandas
from oauth2client.service_account import ServiceAccountCredentials

# Requirements for getting Google survey responses
sheet_name = 'MadPy (Responses)'
service_account_creds = 'madpy-service-account-key.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    service_account_creds, scopes='https://spreadsheets.google.com/feeds',
)
google_sheets = gspread.authorize(credentials)

try:
    ws = google_sheets.open(sheet_name).sheet1
except gspread.SpreadsheetNotFound:
    print('spreadsheet %s not found, is it shared with the creds email?' % sheet_name)

df = pandas.DataFrame(ws.get_all_records())

# Deidentify responses
cols_to_remove = ['Email Address', 'Timestamp', 'Additional comments?']
df.drop(cols_to_remove, axis=1, inplace=True)
df = df.sample(len(df))

df.to_csv('responses-deidentified.csv', index=False)
