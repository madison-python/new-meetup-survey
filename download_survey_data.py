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
import gspread
from oauth2client.service_account import ServiceAccountCredentials


credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'madpy-service-account-key.json',
    scopes = 'https://spreadsheets.google.com/feeds',
)

gc = gspread.authorize(credentials)
ws = gc.open('MadPy (Responses)').sheet1

open('madpy-survey-responses.csv', 'wb').write(ws.export())
