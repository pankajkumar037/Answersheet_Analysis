import streamlit as st
from PIL import Image
from model import model_output_with_image, model_output_text
from Prompts.allprompt import answersheetprompt, questionpaperprompt, question_and_answer_sheet_combined_promt,final_prompt


def main():
    st.title("Insights from Answer Sheet & Question Paper ")
    
    answer_sheet = st.file_uploader("Upload Answer Sheet Page ", type=["jpg"], key="answer")
    question_paper = st.file_uploader("Upload Question Paper ", type=["jpg"], key="question")
    
    
    if answer_sheet:
        #st.image(answer_sheet, caption="Answer Sheet", use_column_width=True)
        st.success("Answer Sheet Uploaded Successfully!")
    else:
        st.warning("Please upload an Answer Sheet.")
    
    if question_paper:
        st.success("Question Paper Uploaded Successfully!")
    else:
        st.info("Please upload an Answer Sheet.")



    if st.button("Get Insights"):
        st.spinner("Generating insights...")

        if answer_sheet and question_paper:
            answer_sheet_res= model_output_with_image(answer_sheet, answersheetprompt())
            question_paper_res= model_output_with_image(question_paper, questionpaperprompt())
            combined_res= model_output_text(question_and_answer_sheet_combined_promt(answer_sheet_res, question_paper_res))
            final_res= model_output_text(final_prompt(combined_res))
            st.write("Finali nsights sorted by obtained marks:",final_res)
        elif answer_sheet:
            answer_sheet_res= model_output_with_image(answer_sheet, answersheetprompt())
            st.write("Answer Sheet Insights:", answer_sheet_res)
        elif question_paper:
            question_paper_res= model_output_with_image(question_paper, questionpaperprompt())
            st.write("Question Paper Insights:", question_paper_res)
        else:
            st.warning("Please upload files to get insights.")


        


if __name__ == "__main__":
    main()
