def answersheetprompt():
    try:
        prompt_answersheet ="""Extract all the marks according to the Question.Give output in json Format not a single other word by yourself.just json object.Dont include anything of Grade.Every Question number has just only one marks related to it marks.
                                your op will in form:
                                "01": "1",
                                "02": "1",
                                "03": "1",
                                "04": "1",
                                "05": "1",
                                "06": "1"
                                sorted by Question number start from question 1.
                                "This is just a sample"
                            """
        return prompt_answersheet
    except Exception as e:
        return f"Error in generating answersheet prompt: {str(e)}"