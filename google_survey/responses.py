#!/usr/bin/env python
"""Download Madpy survey responses as an excel file."""
from os import path
import gspread
import pandas
from oauth2client.service_account import ServiceAccountCredentials


def get_responses(sheet_name, service_account_creds, deidentify_responses=True,
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


def tidy_responses(google_survey_responses, new_column_names=None):
    if not isinstance(google_survey_responses, pandas.DataFrame):
        google_survey_responses = pandas.read_csv(google_survey_responses)

    # Create map of question ids to question texts
    if new_column_names is None:
        new_column_names = {name: 'q{}'.format(i)
                            for i, name in enumerate(google_survey_responses.columns)}

    # Relabel response columns with question ids
    labeled_responses = google_survey_responses.copy()
    labeled_responses.rename(columns=new_column_names, inplace=True)

    # Assign a unique identifier for each survey taker
    person_ids = ['p{}'.format(i) for i in labeled_responses.index]
    labeled_responses.insert(0, 'person', person_ids)

    # Melt the data from wide to long
    response_strs = pandas.melt(labeled_responses, 'person',
                                var_name='question', value_name='response_str')

    # Split response strings into one response per row
    responses = melt_responses(response_strs)

    return responses


def melt_responses(response_strs):
    melted_responses = _melt_response_strs(response_strs.response_str)
    return response_strs.merge(melted_responses, left_index=True,
                               right_index=True)


def _melt_response_strs(response_strs):
    response_list = [split_response(response, ix)
                     for ix, response in response_strs.iteritems()]
    response_ser = pandas.concat(response_list)
    response_df = response_ser.reset_index(level='response_n')
    return response_df


def split_response(response_str, ix=0):
    try:
        responses = [response.strip() for response in response_str.split(',')]
    except AttributeError:
        responses = [response_str]

    index_pairs = zip([ix]*len(responses), range(len(responses)))
    multi_index = pandas.MultiIndex.from_tuples(list(index_pairs),
                                                names=['index', 'response_n'])
    return pandas.Series(responses, index=multi_index, name='response')
