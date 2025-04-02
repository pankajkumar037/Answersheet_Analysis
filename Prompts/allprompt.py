def answersheetprompt():
    try:
        prompt_answersheet = f"""
            Give detailed analysis of marks section. If handwritten marks not written for a Question number just ignore it and don't hallucinate.
            After that, give Question number and their marks obtained in JSON format.
        """
        return prompt_answersheet
    except Exception as e:
        return f"Error in generating answersheet prompt: {str(e)}"

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

def final_prompt(combined_res):
    try:
        return f"just tell me the topic and arrange them according to obtained marks in ascending order considering this {combined_res}..Give answer in detail"
    except Exception as e:
        return f"Error in generating final prompt: {str(e)}"
