import pandas


def tidy(google_survey_responses):
    if not isinstance(google_survey_responses, pandas.DataFrame):
        google_survey_responses = pandas.read_csv(google_survey_responses)

    # Create map of question ids to question texts
    questions = pandas.DataFrame(dict(question=google_survey_responses.columns))
    question_ids = ['q{}'.format(i) for i in questions.index]
    questions.insert(0, 'id', question_ids)

    # Relabel response columns with question ids
    labeled_responses = google_survey_responses.copy()
    labeled_responses.columns = questions.id

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
