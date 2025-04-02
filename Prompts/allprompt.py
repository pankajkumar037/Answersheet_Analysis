
def answersheetprompt():
    prompt_answersheet = f"""
        Give detailed analysis of marks section.If handwritten marks not written for a Question number just ignore it.and dont hellusinate.
        After that Give Question number and their marks obtained in json format.
    """
    return prompt_answersheet


def questionpaperprompt():
    prompt_Question = f"""
        Analyse the Given question Paper presisely.Give question and their maximum marks in json format.if a  question has more than one subpart then give their subpart but max maarks of combined below that whole subpart.Give output in json format
    """
    return prompt_Question


def question_and_answer_sheet_combined_promt(Answersheet, Question_Paper):
   #few sort prompting for model
    outputs="""

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


    prompt_combining_ocr=f"""
    You are given two JSON objects: {Answersheet}` and :{Question_Paper}.

    - {Question_Paper} contains a list of questions, subparts, descriptions, and maximum marks.
    - {Answersheet}contains the marks obtained for each question.

    Your task is to merge these two JSONs and give output only json object.

    Return a **single valid JSON object** with all questions, subparts, `"max_marks"`, and `"marks_obtained"`.

    yout output will be like {outputs} .you will give just output not code


    """

    return prompt_combining_ocr



def final_prompt(combined_res):
    return f"just tell me the topic and araange them according to obtained marks in ascending order considering this {combined_res}..Give answer in detail"