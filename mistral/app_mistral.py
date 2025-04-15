from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image
from io import BytesIO
import pandas as pd
import csv
import os
import json, re



#importing our model
from mistral.model_mistaral import model_output_with_image, model_output_text


#importing our prompts
from Prompts.question_paper_prompt import questionpaperprompt
from Prompts.answersheet_ocr_prompt import answersheetprompt
from Prompts.combining_ocr_prompt import question_and_answer_sheet_combined_promt

#importing our image processing function for focusing on marks part
from image_process.image_crop import crop_marks_section


#importing functions for excel conversion of our result
from To_Excel.to_excel import getting_excel_for_Question_Paper
from To_Excel.to_excel import getting_csv_ans_result
from To_Excel.to_excel import final_marks_to_excel




app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/upload", methods=["POST"])
def upload_files():
    global cool  

    answer_file = request.files.get("answer_sheet")
    question_file = request.files.get("question_paper")

    results = {}

  

    if answer_file and question_file:

        #for extracting answersheet
        answer_image = Image.open(answer_file)
        cropped_answer = crop_marks_section(answer_image)
        ans_result = model_output_with_image(cropped_answer, answersheetprompt())


        #for extracting Question marks
        ques_image = Image.open(question_file)
        ques_result = model_output_with_image(ques_image, questionpaperprompt())

        

        #for getting our final Results

        combined = model_output_text(question_and_answer_sheet_combined_promt(ans_result, ques_result))

        ##
        results["Combined Result:"] = combined 

        
        ##taking our model output and parsing it to json

        try:
            match = re.search(r'```json\n(.*?)```', combined, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                parsed_json = json.loads(json_str)
                results["Combined Result:"] = parsed_json
            else:
                results["Combined Result:"] = "Could not parse JSON from model output."
        except Exception as e:
            results["Combined Result:"] = f"Error parsing JSON: {str(e)}"


        
        final_marks_to_excel(results)

        return results


    if answer_file:
        answer_image = Image.open(answer_file)
        cropped_answer = crop_marks_section(answer_image)
        ans_result = model_output_with_image(cropped_answer, answersheetprompt())
        results["Answer Sheet Insights"] = ans_result



        ##taking our model output and parsing it to json
        try:
            match = re.search(r'```json\n(.*?)```', ans_result, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                parsed_json = json.loads(json_str)
                results["Answer Sheet Insights"] = parsed_json
            else:
                results["Answer Sheet Insights"] = "Could not parse JSON from model output."
        except Exception as e:
            results["Answer Sheet Insights"] = f"Error parsing JSON: {str(e)}"

        getting_csv_ans_result(results)
        return results


    if question_file:
        ques_image = Image.open(question_file)
        ques_result = model_output_with_image(ques_image, questionpaperprompt())
        results["Question Paper Insights"] = ques_result


        ##taking our model output and parsing it to json
        
        try:
            match = re.search(r'```json\n(.*?)```', ques_result, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                parsed_json = json.loads(json_str)
                results["Question Paper Insights"] = parsed_json
            else:
                results["Question Paper Insights"] = "Could not parse JSON from model output."
        except Exception as e:
            results["Question Paper Insights"] = f"Error parsing JSON: {str(e)}"


        getting_excel_for_Question_Paper(results)

        return results

@app.route("/download")
def download_file():
    return send_file("output/result.xlsx", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
