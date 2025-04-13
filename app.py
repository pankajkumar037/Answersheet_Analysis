from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image
from io import BytesIO
import pandas as pd
import csv
import os

from model import model_output_with_image, model_output_text
from Prompts.question_paper_prompt import questionpaperprompt
from Prompts.answersheet_ocr_prompt import answersheetprompt
from Prompts.combining_ocr_prompt import question_and_answer_sheet_combined_promt
from image_process.image_crop import crop_marks_section

from save_functions.Qn import dump_result_to_pdf

app = Flask(__name__)

cool = False  

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/upload", methods=["POST"])
def upload_files():
    global cool  

    answer_file = request.files.get("answer_sheet")
    question_file = request.files.get("question_paper")

    results = {}

    def getting_csv_ans_result(result):
        insights = result["Answer Sheet Insights"]
        insights = {k: v for k, v in insights.items() if k != "Total"}
        os.makedirs("output", exist_ok=True)
        with open("output/result.csv", mode="w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Qno", "Marks"])
            for qno, marks in sorted(insights.items(), key=lambda x: int(x[0][1:])):
                writer.writerow([qno, marks])



    if answer_file and question_file:


        ##
        answer_image = Image.open(answer_file)
        cropped_answer = crop_marks_section(answer_image)
        ans_result = model_output_with_image(cropped_answer, answersheetprompt())
        print("Answer Sheet Result:", ans_result)

        ##
        ques_image = Image.open(question_file)
        ques_result = model_output_with_image(ques_image, questionpaperprompt())

        
        print("Question Paper Result:", ques_result)

        ##

        combined = model_output_text(question_and_answer_sheet_combined_promt(ans_result, ques_result))
        print("Combined Result:", combined)

        ##
        results["Combined Result:"] = combined 

        import json, re
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



        dump_result_to_pdf(results)
        cool = True

        return results


    if answer_file:
        answer_image = Image.open(answer_file)
        cropped_answer = crop_marks_section(answer_image)
        ans_result = model_output_with_image(cropped_answer, answersheetprompt())
        results["Answer Sheet Insights"] = ans_result

        import json, re
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
        cool = False
        return results

    if question_file:
        ques_image = Image.open(question_file)
        ques_result = model_output_with_image(ques_image, questionpaperprompt())
        results["Question Paper Insights"] = ques_result

        import json, re
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

        dump_result_to_pdf(results)
        cool = True
        return results

@app.route("/download")
def download_file():
    if cool:
        return send_file("output/results.pdf", as_attachment=True)
    else:
        return send_file("output/result.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
