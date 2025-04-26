# answersheet_analysis_app.py

import streamlit as st
import os
import pandas as pd
from PIL import Image
import json
import matplotlib.pyplot as plt
import seaborn as sns

from PIL import Image, UnidentifiedImageError
from io import BytesIO
import pandas as pd
import csv
import json, re
from dotenv import load_dotenv

from model import model_output_with_image, model_output_text, model_output_with_pdf

# Import prompts
from Prompts.question_paper_prompt import questionpaperprompt
from Prompts.answersheet_ocr_prompt import answersheetprompt
from Prompts.combining_ocr_prompt import question_and_answer_sheet_combined_promt

# Excel handlers
from To_Excel.to_excel import getting_excel_for_Question_Paper, getting_csv_ans_result, final_marks_to_excel

# Image cropper
from image_process.image_crop import crop_marks_section

st.set_page_config(layout="wide")
results_question = {}
results_answer = {}

# === Streamlit UI ===
st.markdown("""
    <style>
        .main > div {
            padding-left: 2rem;
            padding-right: 2rem;
        }
        .stButton>button {
            height: 3em;
            font-size: 1.1em;
        }
        .stFileUploader, .stSelectbox, .stDownloadButton {
            margin-bottom: 1.5em;
        }
        .block-container {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📄 Answer Sheet Analysis (Class 1 to 12)")

with st.sidebar:
    st.header("🔧 Settings")
    class_name = st.selectbox("Select Class", [f"Class {i}" for i in range(1, 13)])
    st.markdown("---")

st.header("Step 1: Upload Question Paper (PDF)")
question_pdf = st.file_uploader("Upload Question Paper PDF", type="pdf")

if question_pdf:
    Question_data = model_output_with_pdf(question_pdf, questionpaperprompt())
    print(Question_data)

    results_question["Question Paper Insights"] = Question_data

    try:
        match = re.search(r'```json\n(.*?)```', Question_data, re.DOTALL)
        if match:
            parsed_json = json.loads(match.group(1).strip())
            results_question["Question Paper Insights"] = parsed_json
        else:
            results_question["Question Paper Insights"] = "Could not parse JSON from model output."
    except Exception as e:
        results_question["Question Paper Insights"] = f"Error parsing JSON: {str(e)}"

    getting_excel_for_Question_Paper(results_question)
    df = pd.read_csv('output/result_qns.csv')
    st.write(df)

# For answer sheets
st.header("Step 2: Upload Answer Sheet(s) (Images)")
answer_imgs = st.file_uploader("Upload Answer Sheets (One or Many Images)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if answer_imgs:
    all_answer_data = []

    for idx, img in enumerate(answer_imgs, start=1):
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
    st.write(df)

st.header("📊 Insights")

if answer_imgs:
    df = pd.read_csv("output/combined_answers.csv", index_col=0)

    if "Total_Marks" not in df.columns:
        df["Total_Marks"] = df.sum(axis=1)

    st.subheader("📌 Total Marks per Answer Sheet")
    with st.container():
        fig, ax = plt.subplots(figsize=(8, 3))
        df["Total_Marks"].plot(kind='bar', ax=ax, color="skyblue")
        ax.set_title("Total Marks")
        ax.set_ylabel("Marks")
        ax.set_xlabel("Answer Sheets")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    st.subheader("📌 Average Score per Question")
    with st.container():
        avg_scores = df.drop(columns="Total_Marks").mean()
        fig1, ax1 = plt.subplots(figsize=(10, 2.5))
        avg_scores.plot(marker='o', color='green', ax=ax1)
        ax1.set_title("Average Score per Question")
        ax1.set_xlabel("Question Number")
        ax1.set_ylabel("Average Score")
        ax1.grid(True)
        st.pyplot(fig1)

    st.subheader("📌 Most Mistaken Questions")
    with st.container():
        low_avg_questions = avg_scores.sort_values().head(5)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.dataframe(low_avg_questions)

        with col2:
            fig2, ax2 = plt.subplots(figsize=(5, 2.5))
            sns.barplot(x=low_avg_questions.index.astype(str), y=low_avg_questions.values, palette='Reds', ax=ax2)
            ax2.set_title("Top 5 Most Mistaken Questions")
            ax2.set_xlabel("Question")
            ax2.set_ylabel("Avg Score")
            st.pyplot(fig2)

    st.subheader("📌 Lowest Scoring Answer Sheets")
    with st.container():
        weak_students = df["Total_Marks"].sort_values().head(3)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.dataframe(weak_students)

        with col2:
            fig3, ax3 = plt.subplots(figsize=(5, 2.5))
            sns.barplot(x=weak_students.index, y=weak_students.values, palette='Blues', ax=ax3)
            ax3.set_title("Weakest Students")
            ax3.set_ylabel("Total Marks")
            st.pyplot(fig3)

    st.subheader("📌 Heatmap of Answer Sheet Responses")
    with st.expander("Show Heatmap"):
        fig4, ax4 = plt.subplots(figsize=(12, 4))
        sns.heatmap(df.drop(columns="Total_Marks"), annot=False, cmap="coolwarm", ax=ax4)
        ax4.set_title("Responses Heatmap")
        ax4.set_xlabel("Question Number")
        ax4.set_ylabel("Answer Sheet")
        st.pyplot(fig4)

    st.subheader("📌 Average Score vs Max Mark per Question")
    try:
        with st.container():
            # Load max marks from external CSV
            
            max_marks_df = pd.read_csv("output/result_qns.csv")  # ensure this file is in your working directory
            max_marks_df['Question_Number'] = max_marks_df['Question_Number'].astype(str)

            # Prepare dataframe with average scores
            question_cols = df.drop(columns="Total_Marks").columns
            question_numbers = [col.replace("Q", "") for col in question_cols]  # assuming columns are named Q1, Q2, etc.

            # Compute average score per question
            avg_scores = df[question_cols].mean()

            # Match max marks using the external file
            max_marks_series = max_marks_df.set_index('Question_Number').loc[question_numbers]['Max Marks']
            max_marks_series.index = question_cols  # align index names to question columns like Q1, Q2...

            # Combine into a single DataFrame
            comparison_df = pd.DataFrame({
                "Average Score": avg_scores,
                "Max Mark": max_marks_series
            })

            # Plotting
            fig5, ax5 = plt.subplots(figsize=(12, 4))
            comparison_df.plot(kind='bar', ax=ax5, width=0.75)
            ax5.set_title("Average Score vs Max Mark per Question")
            ax5.set_ylabel("Marks")
            ax5.set_xlabel("Question")
            ax5.tick_params(axis='x', rotation=45)
            ax5.legend(loc='upper right')

            st.pyplot(fig5)
    
    except Exception as e:
        st.error(f"Question in Answer sheet is less: {e}")

    st.subheader("⬇️ Download Processed Data")
    csv = df.to_csv().encode('utf-8')
    st.download_button("Download CSV", csv, "processed_answers.csv", "text/csv")