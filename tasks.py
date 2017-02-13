from invoke import task
import google_survey

RESPONSES_CSV = 'responses.csv'
QUESTIONS_CSV = 'questions.csv'


@task
def responses(ctx, output_csv_name=None, random_state=None,
              download_only=False):
    """Download the responses to the new meetup survey."""
    creds = 'madpy-service-account-key.json'

    try:
        random_state = int(random_state)
    except TypeError:
        random_state = None

    responses = google_survey.get_responses('MadPy (Responses)', creds,
                                            random_state=random_state)
    output_csv_name = output_csv_name or RESPONSES_CSV
    if not download_only:
        questions = google_survey.get_questions('madpy-survey-url.txt')
        new_column_names = questions.set_index('title')['id'].to_dict()
        responses = google_survey.tidy_responses(responses, new_column_names)
    responses.to_csv(output_csv_name, index=False)


@task
def questions(ctx, output_csv_name=None):
    """Download the survey HTML to parse survey info."""
    questions = google_survey.get_questions('madpy-survey-url.txt')
    output_csv_name = output_csv_name or QUESTIONS_CSV
    questions.to_csv(output_csv_name, index=False)
