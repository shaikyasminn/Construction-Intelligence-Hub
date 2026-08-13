
# 🏗️ Construction Intelligence Hub

## AI-Powered Construction Project Management & Decision Support Platform

Construction Intelligence Hub (CIH) is an AI-powered construction management platform developed to centralize project operations, monitor construction activities, and provide intelligent decision support.

The platform combines a Streamlit-based enterprise dashboard with local Large Language Model (LLM) integration using **Ollama and Llama 3.2**.

---

## 🎯 Project Objective

The main objective of Construction Intelligence Hub is to provide a unified platform for construction project management by integrating:

- Project management
- Workforce management
- Material and inventory management
- Budget and financial monitoring
- Safety and risk management
- AI-powered project insights
- AI conversational assistance
- Executive report generation
- User authentication

The integration of Ollama transforms the dashboard from a static monitoring system into an **AI-powered decision support platform**.

---

## 🚀 Key Features

### 📊 Enterprise Dashboard

Provides an overall view of construction operations including:

- Total projects
- Active projects
- Delayed projects
- Workforce statistics
- Material stock alerts
- Project health information

### 🗂️ Project Management

- Project tracking
- Project progress monitoring
- Project status analysis
- Project information management
- Location and project data

### 👥 Workforce Management

- Employee records
- Workforce allocation
- Job roles
- Attendance information
- Workforce statistics

### 📦 Material Management

- Material inventory
- Stock monitoring
- Low-stock alerts
- Supplier information
- Material usage analysis

### 💰 Budget & Finance

- Project budgets
- Actual expenditure
- Planned vs actual analysis
- Financial monitoring
- Budget recommendations

### 🛡️ Safety & Risk Management

- Safety monitoring
- HSE information
- Incident analysis
- PPE compliance
- Construction risk analysis
- AI-based safety recommendations

### 🤖 AI Decision Center

The AI Decision Center uses **Ollama with Llama 3.2** to generate intelligent construction insights.

Implemented AI functions include:

- AI Project Summary
- Construction Risk Analysis
- Budget Advisor
- Safety Advisor
- Material Advisor
- Executive Report Generation

The application sends project information and user prompts to the local LLM and displays the generated response within the dashboard.

### 💬 ConstructAI Assistant

ConstructAI is a construction-focused AI assistant powered by **Ollama and Llama 3.2**.

It can assist with:

- Construction projects
- Project management
- Budget analysis
- Material estimation
- Workforce management
- Site safety
- Scheduling
- Risk management
- Procurement
- Inventory
- Equipment
- Construction reports
- Building planning

The assistant is restricted to construction and project-management-related queries.

### 📋 Reporting Agent

The Reporting Agent consolidates information from construction intelligence modules and generates professional executive reports.

It supports:

- Daily site reports
- Executive risk summaries
- Audit-ready documentation
- Project health reports
- Safety findings
- Site risk analysis
- Compliance status
- Insurance summary
- Material status
- Recommendations
- Overall project health

Reports can be generated and exported as PDF documents.

### 🔐 Authentication

The application includes a login interface with:

- User login
- Password authentication
- Create Account option
- Session-based authentication
- Logout functionality

---

## 🧠 AI Architecture

```text
User
  │
  ▼
Streamlit Dashboard
  │
  ▼
AI Decision Center / ConstructAI
  │
  ▼
Ollama Local LLM Runtime
  │
  ▼
Llama 3.2
  │
  ▼
AI Generated Response
  │
  ▼
Construction Intelligence Hub
````

Ollama is installed and configured locally and is connected to the Streamlit application through the Python Ollama package.

---

## 🛠️ Technology Stack

| Technology | Purpose                      |
| ---------- | ---------------------------- |
| Python     | Application development      |
| Streamlit  | Interactive web application  |
| Ollama     | Local LLM runtime            |
| Llama 3.2  | AI language model            |
| Pandas     | Data processing              |
| Plotly     | Interactive visualizations   |
| Requests   | Live weather/API integration |
| HTML/CSS   | UI customization             |
| Git/GitHub | Version control              |

---

## 📁 Project Structure

```text
Construction_Intelligence_Hub/
│
├── app.py
├── README.md
├── requirements.txt
│
├── assets/
│   ├── logo.png
│   └── styles.css
│
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Project_Management.py
│   ├── 3_Workforce.py
│   ├── 4_Materials.py
│   ├── 5_Budget.py
│   ├── 6_Safety.py
│   ├── 7_AI_Insights.py
│   ├── 8_AI_Assistant.py
│   └── 9_Reports.py
│
└── utils/
    ├── __init__.py
    ├── helper.py
    └── sample_data.py
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Construction-Intelligence-Hub.git
```

### 2. Navigate to the project

```bash
cd Construction-Intelligence-Hub
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Download and install Ollama from:

[https://ollama.com/](https://ollama.com/)

### 5. Download the Llama 3.2 model

```bash
ollama pull llama3.2
```

### 6. Start Ollama

```bash
ollama serve
```

### 7. Run the application

```bash
python -m streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 🔑 Demo Authentication

For the current prototype:

```text
Username: admin
Password: admin123
```

New users can also create an account through the **Create Account** option.

> Note: The current authentication implementation is intended for project demonstration. Production deployment should use secure database-backed authentication and password hashing.

---

## 📌 Milestones

### Milestone 1 – Core Construction Intelligence Hub

* Enterprise dashboard
* Project management
* Workforce management
* Material management
* Budget management
* Safety monitoring

### Milestone 2 – AI Integration

* Ollama integration
* Llama 3.2 integration
* ConstructAI Assistant
* AI Decision Center
* AI Project Summary
* Risk Analysis
* Budget Advisor
* Safety Advisor
* Material Advisor
* Executive Report Generation
* Live weather integration

The second milestone specifically integrated Ollama and Llama 3.2 to provide intelligent project summaries, risk analysis, safety recommendations, budget insights, material planning, and executive reporting. 

### Milestone 3 – Generative AI & Construction Intelligence

* Construction-focused Generative AI
* Domain-specific query validation
* Project Q&A
* AI-powered construction assistance
* Improved AI reliability and relevance

### Current Enhancements

* Reporting Agent
* PDF report generation
* Professional login interface
* Create Account functionality
* Session-based authentication

---

## 🔒 AI Domain Restriction

ConstructAI is designed specifically for the construction domain.

The AI validates user queries and supports topics such as:

* Construction
* Civil engineering
* Project management
* Budget
* Materials
* Workforce
* Safety
* Scheduling
* Risk
* Procurement
* Inventory
* Equipment
* Construction reports

Unrelated queries are rejected to maintain the intended domain focus.

---

## 🔮 Future Scope

Potential future enhancements include:

* Machine-learning-based project delay prediction
* Construction cost estimation
* Voice-enabled AI Assistant
* IoT sensor integration
* Equipment maintenance prediction
* BIM integration
* Drone-based site monitoring
* Advanced predictive analytics

---

## 👩‍💻 Author

**Shaik Yasmin**

B.Tech – Computer Science and Engineering

**Project:** Construction Intelligence Hub

**Program:** Infosys Springboard

---

## 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

```

This version is much closer to **your actual project and milestones**, especially because it documents the Ollama/Llama 3.2 integration that was part of your Milestone 2 work. :contentReference[oaicite:3]{index=3}

One correction: I would **not claim the login is SQLite/database-backed** in this README, because your current `app.py` uses session state for the prototype login.
```
