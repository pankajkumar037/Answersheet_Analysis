def final_prompt(combined_res):
    try:
        return f"just tell me the topic and arrange them according to obtained marks in ascending order considering this {combined_res}..Give answer in detail"
    except Exception as e:
        return f"Error in generating final prompt: {str(e)}"