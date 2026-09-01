# 📊 AI Data Analyst

> An AI-powered Business Intelligence platform that allows users to analyze PostgreSQL business data using natural language.

## 🚀 Overview

AI Data Analyst is a Generative AI-powered analytics platform that allows users to ask business questions in natural language instead of writing SQL manually.

The application converts natural-language questions into SQL queries using Gemini, executes them against PostgreSQL, automatically selects suitable visualizations, and generates AI-powered business insights.

Users can also explore query results and export analyzed data to CSV or Excel.

---

## ✨ Key Features

- 🤖 Natural Language → SQL
- 🧠 Gemini-powered SQL generation
- 🐘 PostgreSQL database integration
- 🛡️ SQL validation and execution
- 📊 Automatic visualization selection
- 📈 Interactive Plotly charts
- 💡 AI-generated business insights
- 📌 KPI cards and data summaries
- 📄 CSV export
- 📊 Excel export
- 🔍 Generated SQL inspection
- 🎨 Responsive and professional Streamlit UI
- 🔐 Environment-variable based API configuration

---

## 🏗️ How It Works

```text
User Question
      ↓
Gemini AI
      ↓
SQL Generation
      ↓
SQL Validation
      ↓
PostgreSQL
      ↓
Query Result
      ↓
 ┌───────────────┬────────────────┐
 ↓               ↓                ↓
Visualization   AI Insights     Export
 ↓               ↓                ↓
Plotly         Gemini          CSV / Excel

Tech Stack
Technology	Purpose
Python	Core application
Streamlit	Web interface
PostgreSQL	Database
Gemini	Generative AI
Pandas	Data processing
Plotly	Interactive visualization
SQL	Data querying
OpenPyXL	Excel export
python-dotenv	Environment configuration
📂 Project Structure
AI-Data-Analyst/
│
├── app/
│   ├── services/
│   │   ├── ai_analyst_service.py
│   │   ├── insight_service.py
│   │   ├── visualization_service.py
│   │   ├── chart_service.py
│   │   ├── export_service.py
│   │   └── sql_service.py
│   │
│   └── ...
│
├── database/
│
├── data/
│
├── tests/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
⚙️ Installation
1. Clone the repository
git clone https://github.com/Mohansonu/AI-Data-Analyst.git
2. Navigate to the project
cd AI-Data-Analyst
3. Create a virtual environment

Windows:

python -m venv venv
4. Activate the environment
venv\Scripts\activate
5. Install dependencies
pip install -r requirements.txt
🔐 Environment Variables

Create a .env file in the project root.

GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=your_postgresql_database_url

Never commit your .env file to GitHub.

Use .env.example as a reference.

🗄️ Database Setup

The application uses PostgreSQL as the primary database.

Make sure PostgreSQL is running and the required database/tables are available before starting the application.

The application connects to PostgreSQL through the configured environment variables.

▶️ Run the Application

Start Streamlit:

streamlit run app.py

The application will open in your browser.

💬 Example Questions

You can ask questions such as:

What are the top 5 products by revenue?

Show monthly revenue.

Which category generates the highest revenue?

How many customers are there?

Show revenue by state.

Show the revenue trend over time.

Compare revenue across product categories.
📊 Supported Visualizations

Depending on the returned dataset, the application can automatically generate:

Bar charts
Line charts
Area charts
Scatter plots
Histograms
Pie charts
Donut charts
Horizontal bar charts
Multi-line charts
Heatmaps
Maps
KPI cards
Metrics
Tables
🧠 AI Business Insights

After analyzing the query results, the system generates:

📌 Summary

A concise explanation of what the data represents.

🔎 Key Findings

Important trends, patterns, and observations identified from the results.

🎯 Recommendations

Actionable suggestions based on the analyzed business data.

📥 Export

Analysis results can be downloaded as:

CSV
Excel (.xlsx)

This allows users to continue their analysis in spreadsheet applications.

🧪 Testing

Run the test suite using:

pytest
🔒 Security

Sensitive credentials are stored using environment variables.

The following files should never be committed:

.env
.env.*
venv/
.venv/

A .gitignore file is included to prevent accidental commits.

🎯 Project Objective

The goal of this project is to demonstrate how Generative AI can simplify traditional data analytics workflows by allowing users to interact with databases using natural language.

It combines:

Generative AI
SQL
Data Analytics
Data Visualization
Business Intelligence
PostgreSQL
Python

into a single interactive platform.

🔮 Future Enhancements

Potential future improvements include:

📅 Advanced date and time filtering
📊 Custom dashboard creation
💬 Conversational follow-up questions
🔄 Query history
👤 User authentication
📈 Advanced forecasting
📤 Scheduled reports
☁️ Cloud deployment
📱 Mobile-friendly analytics
🔍 Advanced semantic data understanding
👨‍💻 Author

Mohan Sonu

Computer Science Engineering Student | AI & Data Analytics Enthusiast
