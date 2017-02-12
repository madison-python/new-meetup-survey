from os import path
import requests


def get(survey_url, output):
    """Get the survey html from a url.

    Args:
        survey_url: Actual url or path to a text file containing the url.
        output: Destination for html page once retrieved.
    """
    if path.exists(survey_url):
        survey_url = open(survey_url).read().strip()

    response = requests.get(survey_url)
    with open(output, 'wb') as handle:
        handle.write(response.content)
