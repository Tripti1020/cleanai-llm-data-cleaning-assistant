# CleanAI — LLM-Powered Data Cleaning Assistant

CleanAI is an AI-assisted data cleaning application built with **Python, Pandas, Streamlit, and Gemini API**.

It helps users analyze messy CSV datasets, identify common data-quality issues, generate an AI-assisted cleaning plan, apply controlled cleaning operations, and compare dataset quality before and after cleaning.

The project combines traditional data-processing techniques with an LLM-powered workflow while keeping the actual data transformation under programmatic control.

---

## 🚀 Project Overview

Real-world datasets are often messy and require significant preparation before they can be used for analysis or machine learning.

Common problems include:

- Missing values
- Invalid email addresses
- Leading and trailing spaces
- Inconsistent categories
- Invalid numeric formats
- Negative values
- Mixed currency formats
- Multiple date formats
- Duplicate records
- Inconsistent data types

CleanAI provides an interactive workflow to identify and handle these problems.

### Main Workflow

```text
CSV Dataset
     ↓
Data Loading
     ↓
Dataset Validation
     ↓
Automated Profiling
     ↓
Issue Detection
     ↓
Gemini AI Cleaning Plan
     ↓
User Review / Approval
     ↓
Pandas Cleaning Engine
     ↓
Before vs After Quality Analysis
     ↓
Cleaned Dataset + Report
✨ Key Features
📂 Smart CSV Data Loading
Upload CSV files through the Streamlit interface.
Use the included sample dataset for demonstration.
Detect and display dataset information after loading.
Support handling of problematic CSV rows through the application's loading options.
🔍 Dataset Validation

CleanAI validates the dataset before processing it further.

The validation layer checks for:

Empty datasets
Missing columns
Duplicate column names
Completely empty columns
Unnamed columns
Missing values
Duplicate rows
Constant-value columns
Basic dataset structure

Validation errors can stop processing when the dataset structure is unsuitable, while warnings can be displayed without unnecessarily stopping the cleaning workflow.

📊 Automated Data Profiling

The profiling module analyzes the uploaded dataset and provides information about:

Number of rows
Number of columns
Data types
Missing values
Duplicate records
Numeric columns
Text columns
Overall dataset quality

This provides an initial understanding of the dataset before cleaning begins.

🚨 Intelligent Issue Detection

CleanAI automatically detects common data-quality problems.

Examples include:

Invalid email formats
Leading/trailing spaces
Negative numeric values
Mixed currency formats
Multiple date formats
Inconsistent categories
Invalid numeric formats
Missing values
Duplicate records

The detected issues are displayed through the Streamlit interface.

🤖 Gemini AI Cleaning Copilot

CleanAI uses the Gemini API to analyze detected data-quality issues and generate a structured cleaning plan.

The AI layer is used for recommendations and reasoning rather than directly modifying the uploaded DataFrame.

The workflow is:

Detected Issues
      ↓
Gemini AI
      ↓
Cleaning Recommendations
      ↓
Structured Cleaning Plan
      ↓
User Review

This separates AI-assisted decision making from the actual data transformation process.

🧹 Automated Cleaning Engine

The cleaning engine applies approved cleaning actions using Python and Pandas.

Examples of cleaning operations include:

Text normalization
Whitespace cleanup
Numeric formatting
Date conversion
Category standardization
Missing-value handling
Issue-specific transformations

The cleaning engine uses vectorized Pandas operations where appropriate to make transformations more efficient and maintainable.

📈 Before vs After Analysis

CleanAI compares the dataset before and after the cleaning process.

The application provides information such as:

Before quality score
After quality score
Quality change
Cleaning statistics
Cleaned data preview

This helps users understand the effect of the cleaning operations.

📄 Automated Reporting
CleanAI can generate a PDF report containing information about the data-cleaning process.

The report can include:

Dataset information
Data-quality scores
Detected issues
Cleaning information
Before/after analysis
Cleaning metrics
AI analysis information
🏗 System Architecture
🧠 AI + Deterministic Cleaning Architecture

A key design decision in CleanAI is separating AI recommendations from actual data transformation.

Why this approach?

The LLM is responsible for:

Understanding detected data-quality issues
Generating cleaning recommendations
Producing a structured cleaning plan

Python and Pandas are responsible for:

Actual data transformation
Text processing
Numeric processing
Date conversion
Category standardization
Missing-value handling
Dataset modification

This approach provides more control over the actual transformations instead of allowing the LLM to directly manipulate the dataset.

📁 Project Structure
CleanAI
│
├── 📁 assets
├── 📁 reports
├── 📁 sample_data
│   └── messy_customer.csv
├── 📁 src
│   ├── cleaning_engine.py
│   ├── data_loader.py
│   ├── issue_detector.py
│   ├── llm_engine.py
│   ├── profiler.py
│   ├── quality_score.py
│   ├── report_generator.py
│   └── validator.py
│
├── 📄 .env.example
├── 📄 .gitignore
├── 📄 README.md
├── 📄 app.py
└── 📄 requirements.txt

Note: .env contains your API credentials and should never be committed to GitHub.

🧩 Module Responsibilities
Module  Responsibility
app.py  Streamlit interface and application workflow
data_loader.py  CSV loading and import handling
validator.py    Dataset structure and validation checks
profiler.py Automated dataset profiling
issue_detector.py   Detection of data-quality issues
llm_engine.py   Gemini-powered cleaning recommendations
cleaning_engine.py  Pandas-based deterministic cleaning
quality_score.py    Dataset quality scoring
report_generator.py PDF report generation
🛠 Technology Stack
Technology  Purpose
Python  Core programming language
Pandas  Data processing and cleaning
NumPy   Numerical data processing
Streamlit   Interactive web application
Gemini API  AI-assisted cleaning recommendations
Plotly  Data visualization
ReportLab   PDF report generation
python-dotenv   Environment variable management
⚙️ Installation
1. Clone the repository
git clone https://github.com/Tripti1020/cleanai-llm-data-cleaning-assistant.git

2. Create a virtual environment
Windows
python -m venv .venv

Activate the environment:

.venv\Scripts\activate
macOS / Linux
python3 -m venv .venv

Activate:

source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
🔑 Configure Gemini API

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key_here

Do not add your real API key to GitHub.

The project also includes .env.example:

GEMINI_API_KEY=your_gemini_api_key_here
▶️ Run the Application

Start the Streamlit application:

streamlit run app.py

The application will open in your browser.

🧪 Using the Sample Dataset

CleanAI includes a sample dataset:

sample_data/messy_customer.csv

You can use it in two ways:

Option 1 — Upload manually

Use the Upload CSV control in the application.

Option 2 — Try Sample Dataset

Click:

🚀 Try Sample Dataset

The application automatically searches for the sample CSV in the project's sample-data locations.

🔄 Application Workflow
Step 1 — Load Dataset

Upload a CSV or select the sample dataset.

Step 2 — Validate Dataset

CleanAI performs structural validation before continuing.

Step 3 — Profile Dataset

The application analyzes rows, columns, data types, missing values and other characteristics.

Step 4 — Detect Data Issues

Potential data-quality problems are identified.

Step 5 — Generate AI Cleaning Plan

Gemini analyzes the detected issues and proposes cleaning actions.

Step 6 — Review Cleaning Plan

The user can review the proposed actions before execution.

Step 7 — Execute Cleaning

The Pandas-based cleaning engine applies the approved transformations.

Step 8 — Compare Results

CleanAI calculates and displays before/after quality information.

Step 9 — Generate Output

The cleaned dataset and report can be generated for further use.

📊 Example Data-Quality Issues

The included sample dataset demonstrates several types of messy data, including:

Invalid Email
Leading/Trailing Spaces
Negative Values
Mixed Currency Formats
Multiple Date Formats
Inconsistent Categories
Invalid Numeric Format

The exact issues detected may vary depending on the uploaded dataset.

🎯 Design Principles
1. AI-Assisted, Not AI-Dependent

The LLM provides recommendations, while Python and Pandas perform the actual transformations.

2. Modular Architecture

Different responsibilities are separated into dedicated modules.

3. Human Review

The cleaning workflow allows the proposed cleaning plan to be reviewed before execution.

4. Controlled Data Transformation

The LLM is not given unrestricted control over the DataFrame.

5. Explainability

The application exposes detected issues and cleaning results to the user.

6. Reproducibility

Programmatic Pandas operations provide a more consistent execution layer for data transformations.

🔐 Security
API credentials are stored using environment variables.
.env should not be committed to version control.
.env.example contains only a placeholder API key.
API credentials should never be hard-coded into Python files.
🚀 Future Improvements

Potential future improvements include:

Streamlit Cloud deployment
User authentication
Dataset history
Larger dataset support
Advanced anomaly detection
Custom data-quality rules
Additional export formats
Cleaning history and versioning
More detailed AI confidence information
Cloud storage integration
Production monitoring
Automated testing
💼 Skills Demonstrated

This project demonstrates practical experience with:

Python
Pandas
NumPy
Data Cleaning
Data Validation
Data Profiling
Data Quality Analysis
Streamlit
Gemini API
LLM-assisted workflows
Modular application architecture
Data visualization
Automated reporting
Environment configuration
👨‍💻 Author

Tripti

MCA | Data Analytics

Interested in Data Analytics, Python, AI-assisted applications and Data Science.