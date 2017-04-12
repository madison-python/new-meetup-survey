# New Meetup Survey

View and analyze the results of a Google Survey in python.

## Madpy

Madpy is a new python user group based in Madison, WI. We conducted a survey about what people wanted to see in the meetings. This repo contains some basic python code for viewing and understanding the results of the survey in python.

## Google authentication steps

This repo uses `gspread` to download the results of the Google Survey via Google's Sheet API. You don't need to follow these steps for the Madpy survey because I've already downloaded the survey results (and deidentified them) and saved them to this repo as "data/deidentified.csv". But if you want to do this sort of thing in a project of your own, it's nice to know how to setup `gspread`.

To use `gspread` you first need to create a new project in the Google Developer console, and enable the API for Google Sheets. The next step is to create and download new service account credentials. Place these credentials in a file named 'madpy-service-account-key.json' in the root of this repo. **Do not** commit this file to the repo.

The final step is to allow this new service account to access the results of the Google Survey. Inside this json file should be a strange looking, machine generated email address. Go to the Google Sheet containing the results of the Google Survey and add as a collaborator the email address associated with the service account.

## Creating a virtualenv for this project

Virtual environments are great so you can play around with new python projects and packages, and not worry about affecting your other projects.

    $ virtualenv --python python3 ~/.venvs/madpy
    $ source ~/.venvs/madpy/bin/activate
    (madpy)$ pip install -r requirements.txt

## Downloading and deidentifying survey data

    (madpy)$ python get_deidentified_responses.py  # creates data/deidentified.csv

## Analyze the data in jupyter notebooks

To play with the jupyter notebooks, you need to start up the jupyter notebook server.

    (madpy)$ jupyter notebook  # starts tornado server, opens in browser

If you just want to see the notebooks, they render nicely on GitHub. Here are the links:

1. [Tidying Google survey response data.](https://github.com/madison-python/new-meetup-survey/blob/master/1-getting-google-survey-responses.ipynb)
2. [Scraping Google survey questions.](https://github.com/madison-python/new-meetup-survey/blob/master/2-parsing-google-survey-questions.ipynb)
3. [Visualizing Google survey results.](https://github.com/madison-python/new-meetup-survey/blob/master/3-visualizing-survey-results.ipynb)
