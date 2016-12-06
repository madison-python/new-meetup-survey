#!/usr/bin/env python
"""Download MadPy survey responses as a csv.

Google authentication steps:

Create a new project in the Google Developer console,
enable the API for Google Sheets, and create/download
new service account credentials.

Go to the Google Sheet you want to access, and add
as a collaborator the email address associated with the
service account credentials. (It's weird and generated.)

"""
from os import path
import gspread
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

open('madpy-survey-responses.csv', 'wb').write(ws.export())
