def answersheetprompt():
    try:
        prompt_answersheet ="""Extract all the marks according to the Question.Give output in json Format not a single other word by yourself.just json object.Dont include anything of Grade.Every Question number has just only one marks related to it marks.
                                your op will in form:
                                "1": "1",
                                "2": "1",
                                "3": "1",
                                "4": "1",
                                "5": "1",
                                "6": "1"
                                first key is question number and second is marks obtained.
                                you output should start striclty from 1 and go on till the last question number. currenlty you are giveing  1 to 10 in last do not do that.
                                "This is just a sample".
                            """
        return prompt_answersheet
    except Exception as e:
        return f"Error in generating answersheet prompt: {str(e)}"