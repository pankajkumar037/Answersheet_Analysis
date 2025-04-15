def answersheetprompt():
    try:
        prompt_answersheet ="""Extract all the marks according to the Question.Give output in json Format not a single other word by yourself.just json object.Dont include anything of Grade.Every Question number has just only one marks related to it marks.
                          
                            """
        return prompt_answersheet
    except Exception as e:
        return f"Error in generating answersheet prompt: {str(e)}"