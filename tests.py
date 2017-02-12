from google_survey.tidy import split_response


def test_split_responses():
    response_str = 'a, b, c'
    responses = split_response(response_str)
    assert responses.tolist() == ['a', 'b', 'c']
