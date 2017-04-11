#!/usr/bin/env python
"""Download Madpy survey responses and deidentify them before saving to csv."""
from os import path
import pandas
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Requirements for getting Google survey responses with gspread
sheet_name = 'MadPy (Responses)'
service_account_creds = 'madpy-service-account-key.json'

# Connect to the Google Sheets API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    service_account_creds, scopes='https://spreadsheets.google.com/feeds',
)
google_sheets = gspread.authorize(credentials)

# Get the first sheet of the workbook
try:
    worksheet = google_sheets.open(sheet_name).sheet1
except gspread.SpreadsheetNotFound:
    print('spreadsheet %s not found, is it shared with the creds email?' % sheet_name)

# Turn the spreadsheet representation into a pandas.DataFrame
df = pandas.DataFrame(worksheet.get_all_records())

# Deidentify responses by removing columns and shuffling rows
cols_to_remove = ['Email Address', 'Timestamp', 'Additional comments?']
df.drop(cols_to_remove, axis=1, inplace=True)
df = df.sample(len(df))

# Save the result
df.to_csv('data/deidentified.csv', index=False)
