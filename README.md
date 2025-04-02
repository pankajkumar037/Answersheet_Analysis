📝 Answersheet Analysis

📌 Overview
This project analyzes answersheets by extracting handwritten marks and combining them with the corresponding question paper to provide a detailed evaluation. It utilizes Google's Generative AI (Gemini) for intelligent processing.

🚀 Installation
1. Clone the Repository
2. cd answersheet_analysis
3. Install Dependencies
    pip install -r requirements.txt`

4.Set Up API Key
Create a .env file in the root directory.

Add your Google API key inside the .env file:

GOOGLE_API_KEY=your_api_key_here
You can replace this with another service provider if needed.

🐂 Project Structure

/ANSWERSHEET_ANALYSIS
  ├── experiment/           # Experimental scripts
  ├── Prompts/              # Prompt templates
  ├── test_image/           # Sample test images
  ├── .env                  # API keys (add manually)
  ├── .gitignore            # Ignore unnecessary files
  ├── app.py                # Main application script
  ├── LICENSE               # License information
  ├── model.py              # Core model implementation
  ├── README.md             # Project documentation
  └── requirements.txt      # Required dependencies


🐜 Usage
Run the model using:
streamlit run app.py

You can use both Question Paper and Answersheet or any one of them

