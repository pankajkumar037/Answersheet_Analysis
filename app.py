from flask import Flask, render_template, request, jsonify, send_file, session
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import pandas as pd
import os
import json
import re
from dotenv import load_dotenv
import base64
import matplotlib.pyplot as plt
import seaborn as sns


from Prompts.question_paper_prompt import questionpaperprompt
from Prompts.answersheet_ocr_prompt import answersheetprompt
from Prompts.combining_ocr_prompt import question_and_answer_sheet_combined_promt

from image_process.image_crop import crop_marks_section


from To_Excel.to_excel import getting_excel_for_Question_Paper, getting_csv_ans_result, final_marks_to_excel


from model import model_output_with_image, model_output_with_pdf, model_output_text

app = Flask(__name__)
app.secret_key = "56161hyjgs"


OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/upload", methods=["POST"])
def upload_files():
    question_file = request.files.get("question_paper")
    answer_files = request.files.getlist("answer_sheets")

    session['qns_uploaded'] = False
    session['ans_uploaded'] = False

    results_question = {}
    results_answer = {}

    if question_file:
        session['qns_uploaded'] = True
        question_content = model_output_with_pdf(question_file, questionpaperprompt())
        results_question["Question Paper Insights"] = _parse_json_output(question_content, "Question Paper Insights")
        getting_excel_for_Question_Paper(results_question)


    if answer_files:
        all_answer_data = []

        for idx, img in enumerate(answer_files, start=1):
            answer_image = Image.open(img)
            cropped_answer = crop_marks_section(answer_image)
            ans_result = model_output_with_image(cropped_answer, answersheetprompt())
            results_answer["Answer Sheet Insights"] = ans_result

            try:
                match = re.search(r'```json\n(.*?)```', ans_result, re.DOTALL)
                if match:
                    parsed_json = json.loads(match.group(1).strip())
                    results_answer["Answer Sheet Insights"] = parsed_json
                else:
                    results_answer["Answer Sheet Insights"] = "Could not parse JSON from model output."
                    parsed_json = {}
            except Exception as e:
                results_answer["Answer Sheet Insights"] = f"Error parsing JSON: {str(e)}"
                parsed_json = {}

            row_data = {f"{i}": parsed_json.get(str(i), "") for i in range(1, 43)}
            row_data["Question_Num"] = f"Answersheet_{idx}"
            all_answer_data.append(row_data)

            df = pd.DataFrame(all_answer_data)
            df.set_index("Question_Num", inplace=True)
            df.to_csv("output/combined_answers.csv")
            session['ans_uploaded'] = True

            charts_data = _generate_charts()
            

    if answer_files and question_file:
        return jsonify({"insights": "insights", "charts": charts_data})
    elif answer_files:
        return jsonify({"insights": "insights", "charts": charts_data})
    else:
        return results_question



def _parse_json_output(model_output, section_title):
    try:
        match = re.search(r'```json\n(.*?)```', model_output, re.DOTALL)
        if match:
            return json.loads(match.group(1).strip())
        else:
            return f"Could not parse JSON from {section_title} output."
    except Exception as e:
        return f"Error parsing JSON from {section_title}: {str(e)}"

def _generate_charts(df_path="output/combined_answers.csv", qns_result_path="output/result_qns.csv"):
    charts = []
    try:
        df = pd.read_csv(df_path, index_col=0)
    except FileNotFoundError:
        print(f"Error: Could not find the answer sheet data file at {df_path}")
        return charts

    if "Total_Marks" not in df.columns:
        # Assuming numerical columns represent question scores
        numeric_cols = df.select_dtypes(include='number').columns
        df['Total_Marks'] = df[numeric_cols].sum(axis=1, skipna=True)

    # Total Marks per Answer Sheet
    plt.figure(figsize=(8, 3))
    df["Total_Marks"].plot(kind='bar', color="skyblue")
    plt.title("Total Marks per Answer Sheet")
    plt.ylabel("Marks")
    plt.xlabel("Answer Sheets")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    charts.append({'id': 'totalMarksChart', 'image': f'data:image/png;base64,{image_base64}'})
    plt.close()

    # Average Score per Question
    numeric_cols_avg = df.select_dtypes(include='number').columns.drop('Total_Marks', errors='ignore')
    if not numeric_cols_avg.empty:
        avg_scores = df[numeric_cols_avg].mean()
        plt.figure(figsize=(10, 2.5))
        avg_scores.plot(marker='o', color='green')
        plt.title("Average Score per Question")
        plt.xlabel("Question Number")
        plt.ylabel("Average Score")
        plt.grid(True)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        charts.append({'id': 'avgScoresChart', 'image': f'data:image/png;base64,{image_base64}'})
        plt.close()

        # Most Mistaken Questions
        low_avg_questions = avg_scores.sort_values().head(5)
        plt.figure(figsize=(6, 3))
        sns.barplot(x=low_avg_questions.index.astype(str), y=low_avg_questions.values, hue=low_avg_questions.index.astype(str), palette='Reds', legend=False)
        plt.title("Top 5 Most Mistaken Questions")
        plt.xlabel("Question")
        plt.ylabel("Average Score")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        charts.append({'id': 'mistakesChart', 'image': f'data:image/png;base64,{image_base64}'})
        plt.close()

    # Lowest Scoring Answer Sheets
    if 'Total_Marks' in df.columns:
        weak_students = df["Total_Marks"].sort_values().head(3)
        plt.figure(figsize=(6, 3))
        sns.barplot(x=weak_students.index, y=weak_students.values, hue=weak_students.index, palette='Blues', legend=False)
        plt.title("Lowest Scoring Answer Sheets")
        plt.ylabel("Total Marks")
        plt.xlabel("Answer Sheet")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        charts.append({'id': 'weakStudentsChart', 'image': f'data:image/png;base64,{image_base64}'})
        plt.close()

    # Heatmap of Answer Sheet Responses
    numeric_cols_heatmap = df.select_dtypes(include='number').columns.drop('Total_Marks', errors='ignore')
    if not numeric_cols_heatmap.empty:
        plt.figure(figsize=(12, 4))
        sns.heatmap(df[numeric_cols_heatmap], annot=False, cmap="coolwarm")
        plt.title("Answer Sheet Responses Heatmap")
        plt.xlabel("Question Number")
        plt.ylabel("Answer Sheet")
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        charts.append({'id': 'heatmapChart', 'image': f'data:image/png;base64,{image_base64}'})
        plt.close()

    # Average Score vs Max Mark per Question
    try:
        max_marks_df = pd.read_csv(qns_result_path)
        if 'Question_Number' in max_marks_df.columns and 'Max Marks' in max_marks_df.columns and not numeric_cols_avg.empty:
            max_marks_df['Question_Number'] = max_marks_df['Question_Number'].astype(str)
            avg_scores_df = avg_scores.to_frame(name='Average Score')
            avg_scores_df.index.name = 'Question_Number'
            merged_df = pd.merge(avg_scores_df.reset_index(), max_marks_df, on='Question_Number', how='inner')

            plt.figure(figsize=(12, 4))
            width = 0.35
            x = range(len(merged_df))
            plt.bar([i - width/2 for i in x], merged_df['Average Score'], width, label='Average Score', color='skyblue')
            plt.bar([i + width/2 for i in x], merged_df['Max Marks'], width, label='Max Marks', color='orange')
            plt.xlabel("Question Number")
            plt.ylabel("Marks")
            plt.title("Average Score vs Max Mark per Question")
            plt.xticks(x, merged_df['Question_Number'], rotation=45, ha='right')
            plt.legend()
            plt.tight_layout()
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            charts.append({'id': 'avgVsMaxChart', 'image': f'data:image/png;base64,{image_base64}'})
            plt.close()
    except FileNotFoundError:
        print(f"Error: Could not find the question paper result file at {qns_result_path}")

    return charts

@app.route("/download")
def download_file():
    ans_uploaded_session = session.get('ans_uploaded', False)
    qns_uploaded_session = session.get('qns_uploaded', False)

    if ans_uploaded_session and qns_uploaded_session:
        return send_file("output/combined_answers.csv", as_attachment=True)
    elif ans_uploaded_session:
        return send_file("output/combined_answers.csv", as_attachment=True)
    elif qns_uploaded_session:
        return send_file("output/result_qns.xlsx", as_attachment=True)
    else:
        return "Please upload files first to enable downloading."
if __name__ == "__main__":
    app.run(debug=True)