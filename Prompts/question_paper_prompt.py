sample="""
    {
    "questions": [
      {
        "Question_Number": "Q1",
        "max_marks": "15",
        "question": "Short answer questions",
        "sub_questions": [
          {
            "sub_question": "a. RTL is used to describe"
          },
        
        ]
      },
      {
        "Question_Number": "Q2",
        "max_marks": "5",
        "question": "With the help of flow diagram discuss instruction execution cycle."
      },
      {
        "Question_Number": "Q3",
        "max_marks": "6",
        "question": "Present a report on the use of common bus system for data transfer? Illustrate data transfer using common bus system through example."
      },
      {
        "Question_Number": "Q4",
        "max_marks": "4",
        "question": "Explain memory reference and register reference instructions with suitable examples."
      }
    ]
  }

  

"""

def questionpaperprompt():
    try:
        prompt_Question = f"""
            Extract questions and their maximum marks in JSON format.
            If a question has more than one subpart, then give their subpart but max marks of combined below that whole subpart.
            And for Question_Number,Give just one time for a Question if ithas subpart or not.
            Give output in json Format not a single other word by yourself just json object.
            your Output should  contain only asked part not antthing other details.
            Take inspiration from {sample},this is just an example.

        """
        return prompt_Question
    except Exception as e:
        return f"Error in generating question paper prompt: {str(e)}"