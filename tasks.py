from invoke import task
import google_survey

@task
def download(ctx):
    creds = 'madpy-service-account-key.json'
    responses = google_survey.download('MadPy (Responses)', creds)
    responses.to_csv('responses-deidentified.csv', index=False)
