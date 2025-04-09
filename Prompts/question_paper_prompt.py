def questionpaperprompt():
    try:
        prompt_Question = f"""
            Analyse the given question paper precisely. Give questions and their maximum marks in JSON format.
            If a question has more than one subpart, then give their subpart but max marks of combined below that whole subpart.
            Give output in JSON format.
        """
        return prompt_Question
    except Exception as e:
        return f"Error in generating question paper prompt: {str(e)}"