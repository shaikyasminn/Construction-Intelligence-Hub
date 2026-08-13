
# Construction Intelligence Hub

## Overview

Construction Intelligence Hub (CIH) is an AI-powered construction project management and operational intelligence platform designed to provide a unified view of construction activities.

The system integrates project management, workforce management, material tracking, budgeting, safety monitoring, AI-powered insights, AI assistance, and executive reporting into a single enterprise portal.

## Objectives

- Centralize construction project information.
- Monitor project progress and operational metrics.
- Manage workforce and material resources.
- Track budgets and financial performance.
- Monitor safety and construction risks.
- Provide AI-powered project insights.
- Generate consolidated executive reports.
- Provide secure user login and account creation.

## Features

### 🏗️ Construction Intelligence Dashboard
- Total projects
- Active projects
- Delayed projects
- Workforce overview
- Material stock alerts
- Operational overview

### 📊 Project Management
- Project tracking
- Project progress monitoring
- Project information management
- Location and project data

### 👥 Workforce Management
- Employee records
- Workforce allocation
- Attendance tracking
- Role-based workforce information

### 📦 Material Management
- Material inventory
- Stock status
- Low-stock alerts
- Supplier information
- Material usage tracking

### 💳 Budget & Finance
- Budget monitoring
- Planned vs actual expenses
- Expense analysis
- Financial project insights

### 🛡️ Safety & Risk Management
- Safety monitoring
- HSE information
- Incident tracking
- PPE compliance
- Risk-related information

### 🤖 AI Insights
- Project health insights
- Predictive analysis
- Schedule delay analysis
- Construction impact analysis

### 💬 AI Assistant
- Construction project assistance
- Operational queries
- AI-powered project support

### 📋 Reporting Agent
The Reporting Agent aggregates information from different project intelligence modules and generates consolidated reports.

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

### 🔐 Authentication
The application includes:

- User login
- Password authentication
- New account creation
- Session-based authentication
- Logout functionality

## Technology Stack

- **Python**
- **Streamlit**
- **Pandas**
- **HTML/CSS**
- **AI/LLM integration**
- **Git & GitHub**

## Project Structure

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
````

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/Construction-Intelligence-Hub.git
```

Navigate into the project:

```bash
cd Construction-Intelligence-Hub
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

## Demo Login

For the current prototype:

```text
Username: admin
Password: admin123
```

New users can also create an account through the **Create Account** option.

> Note: The current authentication is intended for project demonstration purposes and should be replaced with secure database-backed authentication and password hashing for production use.

## Reporting Agent

The Reporting Agent is responsible for consolidating findings from:

* Safety Agent
* Site Risk Agent
* Compliance Agent
* Insurance Agent
* Project Database

It generates a professional consolidated construction report containing project progress, safety findings, risks, compliance, insurance, materials, recommendations, and overall project health.

Reports can be generated and exported as PDF documents.

## Milestones

### Milestone 1

* Core Construction Intelligence Hub
* Dashboard
* Project Management
* Workforce Management
* Material Management

### Milestone 2

* Budget & Finance
* Safety & Risk
* AI Insights
* AI Assistant

### Milestone 3

* Reporting Agent
* Executive reporting
* Report generation
* PDF export
* User authentication
* Login and account creation

## License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

## Author

**Shaik Yasmin**

Construction Intelligence Hub
B.Tech – Computer Science and Engineering

````

### One thing

When you create your GitHub repository, make sure you also select **MIT License**, so GitHub creates the `LICENSE` file automatically.

Then your repo will have:

```text
README.md
LICENSE
app.py
assets/
pages/
utils/
requirements.txt
````

