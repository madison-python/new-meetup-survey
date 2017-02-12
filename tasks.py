from invoke import task
import google_survey


GOOGLE_SURVEY_RESPONSES = 'responses-deidentified.csv'
TIDIED_SURVEY_RESPONSES = 'responses-tidied.csv'


@task
def download(ctx, output_csv_name=None, random_state=None):
    """Download the responses to the madpy new meetup google survey."""
    output_csv_name = output_csv_name or GOOGLE_SURVEY_RESPONSES
    creds = 'madpy-service-account-key.json'

    responses = google_survey.download('MadPy (Responses)', creds,
                                       random_state=int(random_state))
    responses.to_csv(output_csv_name, index=False)


@task
def tidy(ctx, google_survey_responses=None, output_csv_name=None):
    """Tidy the responses to the google survey."""
    google_survey_responses = google_survey_responses or GOOGLE_SURVEY_RESPONSES
    output_csv_name = output_csv_name or TIDIED_SURVEY_RESPONSES

    tidied = google_survey.tidy(google_survey_responses)
    tidied.to_csv(output_csv_name, index=False)
