📝 Answersheet Analysis

📌 Overview
This project analyzes answersheets by extracting handwritten marks and combining them with the corresponding question paper to provide a detailed evaluation. It utilizes Google's Generative AI (Gemini) for intelligent processing.

🚀 Installation
1. Clone the Repository
2. Navigate to the project directory:
   ```bash
   cd answersheet_analysis
   ```
3. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set Up API Key:
   - Create a `.env` file in the root directory.
   - Add your Google API key inside the `.env` file:
     ```
     MISTRAL_API_KEY=your_api_key_here
     ```
   - You can replace this with another service provider if needed.

📂 Project Structure
```
ANSWERSHEET_ANALYSIS/
├── image_process/          # Image cropping and preprocessing
│   ├── __init__.py
│   └── image_crop.py
│
├── notebooks/              # Jupyter notebooks (optional analysis)
│
├── output/                 # Folder to store evaluation results
│
├── Prompts/                # Prompt templates for AI evaluations
│
├── save_functions/         # Functions for saving in pdf
│   ├── __init__.py
│   └── Qn.py
│
├── static/                 # Static files like JS and CSS
│   ├── script.js
│   └── style.css
│
├── templates/              # HTML templates for Flask rendering
│   └── index.html
│
├── test_image/             # Sample test images (add your own)
│
├── .env                    # Environment variables like API keys
├── .gitignore              # Files/folders to ignore in Git
├── app.py                  # Flask application entry point
├── LICENSE                 # License information
├── model.py                # Core model for evaluation
├── README.md               # Project overview and instructions
└── requirements.txt        # Python dependencies


📜 Usage
Run the model using:
```bash
Python app.py
```
You can use both the Question Paper and Answersheet, or any one of them independently.

