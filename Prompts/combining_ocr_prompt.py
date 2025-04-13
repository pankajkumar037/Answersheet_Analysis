def question_and_answer_sheet_combined_promt(Answersheet, Question_Paper):
    try:
       
        prompt_combining_ocr = f"""
        You are given two JSON objects: {Answersheet} and {Question_Paper}.

        - {Question_Paper} contains a list of questions, subparts, descriptions, and maximum marks.
        - {Answersheet} contains the marks obtained for each question.

        Your task is to merge these two JSONs and give output only as a JSON object.
        if a Question has more than one subpart,then then give their subpart but max marks of combined below that whole subpart not individual subpart.
        Return a **single valid JSON object** with all questions, subparts, "max_marks", and "marks_obtained".

        You will give just the output as json object, not code.
        """
        return prompt_combining_ocr
    except Exception as e:
        return f"Error in generating combined prompt: {str(e)}"