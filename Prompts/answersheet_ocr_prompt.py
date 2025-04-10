def answersheetprompt():
    try:
        prompt_answersheet ="Extract all the marks according to the Question.Give output in json Format"
        return prompt_answersheet
    except Exception as e:
        return f"Error in generating answersheet prompt: {str(e)}"