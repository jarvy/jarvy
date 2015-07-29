

class Settings:

    def __init__(self):
        pass

    # default settings

    master_title = 'Mr.'
    master_name = 'Semih'
    master_surname = 'Yagcioglu'
    master_gender = 'female'
    master_formal_address = 'sir'
    master_email_username = None
    master_email_password = None
    jarvy_name = 'jarvy'
    jarvy_gender = 'female'

    # messages
    sorry_messages = ['I am sorry, I could not understand that', 'Oh oh',
                      'I am afraid, I can\'t talk about that',
                      'I am thinking but this beats me...', 'Allright allright, I give up', 'Who knows',
                      'Don\'t get me wrong but I don\'t know all the answers',
                      'Hey, why don\'t you ask me another question while I think more about that?',
                      'Believe me I am trying but, I simply could not answer that',
                      'I think I do not understand you',
                      'Hmmm, I am doing my best,just be patient, OK?']
    farewell_messages = ['good bye', 'bye', 'see you', 'farewell']
    positive_answers = ['Yes', 'Of course', 'Definitely']
    negative_answers = ['No', 'Nope', 'I don\'t think so', 'Sorry']
    personal_message_for_jarvy = ['you', 'yourself']
    personal_message_for_master = ['me', 'myself', 'I']
    rudimentary_question_tags = ['who', 'why', 'when', 'where', 'what', 'which', 'how']

    # algorithm parameters
    number_of_search_results = 10
    trusted_source_treshold = 3
    number_of_minimum_sentences = 3  # should reconsider this


