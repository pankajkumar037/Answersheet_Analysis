import csv
import os
import pandas as pd

def getting_excel_for_Question_Paper(result):
    questions = result["Question Paper Insights"]["questions"]
    os.makedirs("output", exist_ok=True)

    with open("output/result_qns.csv", mode="w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Question_Number", "Max Marks","Question"])

        for qdata in questions:
            qno = qdata.get("Question_Number", "")
            max_marks = qdata.get("max_marks", "")
            questions = qdata.get("question", "")
            writer.writerow([qno, max_marks,questions])

    df = pd.read_csv("output/result_qns.csv")
    df.to_excel("output/result_qns.xlsx", index=False, engine='openpyxl')



def getting_csv_ans_result(result):
    insights = result.get("Answer Sheet Insights", {})  
    insights = {k: v for k, v in insights.items() if k.lower() != "total"}

    os.makedirs("output", exist_ok=True)
    csv_filepath = "output/result_ans.csv"
    excel_filepath = "output/result_ans.xlsx"

    if insights: 
        try:
            with open(csv_filepath, mode="w", newline='', encoding='utf-8') as file:  # Explicit encoding
                writer = csv.writer(file)
                writer.writerow(["Question_Number", "Marks_obtained"])
                for qno, marks in sorted(insights.items(), key=lambda x: int(x[0])):
                    writer.writerow([qno, marks])

            df = pd.read_csv(csv_filepath)
            df.to_excel(excel_filepath, index=False, engine='openpyxl')
            print(f"Successfully created Excel file: {excel_filepath}")

        except Exception as e:
            print(f"Error creating or writing to files: {e}")
    else:
        print("No answer sheet insights (other than 'total') found. Skipping Excel creation.")




def final_marks_to_excel(result):
    df_ans = pd.read_csv('output/result_ans.csv')
    df_qns = pd.read_csv('output/result_qns.csv')

    df_qns['Question_Number'] = df_qns['Question_Number'].str.extract(r'Q(\d+)')[0].astype('Int64')

    # Merging on Question_Number
    merged_df = pd.merge( df_qns,df_ans, on='Question_Number', how='left')

    # Reordering columns
    merged_df = merged_df[['Question_Number', 'Max Marks', 'Question', 'Marks_obtained']]

    # Save to CSV
    merged_df.to_csv('output/result.csv', index=False)

    df = pd.read_csv("output/result.csv")
    df.to_excel("output/result.xlsx", index=False)

    