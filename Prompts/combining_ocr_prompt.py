def question_and_answer_sheet_combined_promt(Answersheet, Question_Paper):
    try:
        outputs = """
        {
        "questions": [
            {
            "question_number": "Q1",
            "description": "Instruction execution cycle",
            "max_marks": 5,
            "marks_obtained": 2
            }
        ]
        }
        """

        prompt_combining_ocr = f"""
        You are given two JSON objects: {Answersheet} and {Question_Paper}.

        - {Question_Paper} contains a list of questions, subparts, descriptions, and maximum marks.
        - {Answersheet} contains the marks obtained for each question.

        Your task is to merge these two JSONs and give output only as a JSON object.

        Return a **single valid JSON object** with all questions, subparts, "max_marks", and "marks_obtained".

        Your output will be like {outputs}. You will give just the output, not code.
        """
        return prompt_combining_ocr
    except Exception as e:
        return f"Error in generating combined prompt: {str(e)}"