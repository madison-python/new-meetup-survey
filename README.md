# new meetup survey

View and analyze the results of a Google Survey in python.

## Madpy

Madpy is a new python user group based in Madison, WI. We conducted a survey about what people wanted to see in the meetings. This repo contains some basic python code for viewing and understanding the results of the survey in python.

## Google authentication steps

This repo uses `gspread` to download the results of the Google Survey via Google's Sheet API. To use `gspread` you first need to create a new project in the Google Developer console, and enable the API for Google Sheets.

The next step is to create and download new service account credentials. Place these credentials in a file named 'madpy-service-account-key.json' in the root of this repo. **Do not** commit this file to the repo.

The final step is to allow this new service account to access the results of the Google Survey. Inside this json file should be a strange looking, machine generated email address. Go to the Google Sheet containing the results of the Google Survey and add as a collaborator the email address associated with the service account.

## Creating a virtualenv for this project

    $ virtualenv --python python3 ~/.venvs/madpy
    $ source ~/.venvs/madpy/bin/activate
    (madpy)$ pip install -r requirements.txt

## Downloading and deidentifying survey data

    (madpy)$ python get_deidentified_responses.py  # creates data/deidentified.csv

## Analyze the data jupyter notebooks

    (madpy)$ jupter notebook  # starts tornado server, open in browser
