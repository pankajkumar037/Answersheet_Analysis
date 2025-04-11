def answersheetprompt():
    try:
        prompt_answersheet ="Extract all the marks according to the Question.Give output in json Format.Dont include anything of Grade.just question wise marks and total marks. "
        return prompt_answersheet
    except Exception as e:
        return f"Error in generating answersheet prompt: {str(e)}"