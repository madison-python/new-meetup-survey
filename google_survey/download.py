#!/usr/bin/env python
"""Download Madpy survey responses as an excel file."""
from os import path
import gspread
import pandas
from oauth2client.service_account import ServiceAccountCredentials


def download(sheet_name, service_account_creds, deidentify_responses=True,
             random_state=None):
    """Download a Google Sheet containing the responses to a Google Survey."""
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        service_account_creds, scopes = 'https://spreadsheets.google.com/feeds',
    )

    gc = gspread.authorize(credentials)

    try:
        ws = gc.open(sheet_name).sheet1
    except gspread.SpreadsheetNotFound:
        print('spreadsheet %s not found, is it shared with the creds email?' % sheet_name)

    df = pandas.DataFrame(ws.get_all_records())

    if deidentify_responses:
        df = deidentify(df, random_state=random_state)

    return df


def deidentify(df, random_state=None):
    cols_to_remove = ['Email Address', 'Timestamp', 'Additional comments?']
    deidentified = df.drop(cols_to_remove, axis=1)
    shuffled = deidentified.sample(len(deidentified), random_state=random_state)
    return shuffled

