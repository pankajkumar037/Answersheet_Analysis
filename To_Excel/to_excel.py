import csv
import os
import pandas as pd

def getting_excel_for_Question_Paper(result):
    questions = result["Question Paper Insights"]["questions"]
    os.makedirs("output", exist_ok=True)

    with open("output/result.csv", mode="w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Qno", "Marks", "Subpart/Question"])

        for i, q in enumerate(questions, 1):
            qno = f"Q{i}"
            data = q.get(qno)

            if isinstance(data, dict):  
                max_marks = data.get("max_marks", 0)
                subparts = data.get("subparts", [])
                num_parts = len(subparts)

                marks_per_part = round(max_marks / num_parts, 2) if num_parts else 0

                for part in subparts:
                    writer.writerow([qno, marks_per_part, part])
            else:  
                marks = q.get("max_marks", "")
                writer.writerow([qno, marks, data])


    df = pd.read_csv("output/result.csv")
    df.to_excel("output/result.xlsx", index=False)



def getting_csv_ans_result(result):
        insights = result["Answer Sheet Insights"]
        insights = {k: v for k, v in insights.items() if k != "Total"}
        os.makedirs("output", exist_ok=True)
        with open("output/result.csv", mode="w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Qno", "Marks"])
            for qno, marks in sorted(insights.items(), key=lambda x: int(x[0][1:])):
                writer.writerow([qno, marks])

        df = pd.read_csv("output/result.csv")
        df.to_excel("output/result.xlsx", index=False)



def final_marks_to_excel(result):
    questions = result["Combined Result:"]
    os.makedirs("output", exist_ok=True)

    with open("output/result.csv", mode="w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Question Number", "Marks Obtained", "Max Marks"])

        for qno, qdata in questions.items():
            marks_obtained = qdata.get("marks_obtained", "")
            max_marks = qdata.get("max_marks", "")
            writer.writerow([qno, marks_obtained, max_marks])

    df = pd.read_csv("output/result.csv")
    df.to_excel("output/result.xlsx", index=False)

    