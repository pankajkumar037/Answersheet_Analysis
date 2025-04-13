import json
from fpdf import FPDF

def dump_result_to_pdf(result_dict, output_path="output/results.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Courier", size=10)  # Courier is monospaced, great for raw JSON

    # Convert dict to pretty-printed JSON string
    result_str = json.dumps(result_dict, indent=2)

    # Split into lines and write line by line to handle multi-line text
    for line in result_str.splitlines():
        pdf.multi_cell(0, 5, line)

    pdf.output(output_path)
    
