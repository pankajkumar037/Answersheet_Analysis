def answersheetprompt():
    try:
        prompt_answersheet = f"""
            Give detailed analysis of marks section. If handwritten marks not written for a Question number just ignore it and don't hallucinate.
            After that, give Question number and their marks obtained in JSON format.
        """
        return prompt_answersheet
    except Exception as e:
        return f"Error in generating answersheet prompt: {str(e)}"