def questionpaperprompt():
    try:
        prompt_Question = f"""
            Extract questions and their maximum marks in JSON format.
            If a question has more than one subpart, then give their subpart but max marks of combined below that whole subpart.
            Give output in json Format not a single other word by yourself just json object.
            your Output should  contain only asked part not antthing other details.

        """
        return prompt_Question
    except Exception as e:
        return f"Error in generating question paper prompt: {str(e)}"