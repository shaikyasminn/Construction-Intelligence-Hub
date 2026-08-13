# pages/8_AI_Assistant.py
import sys
import os

# Ensure search path includes the project root and current working directory
root_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(root_dir) == "pages":
    root_dir = os.path.dirname(root_dir)
root_dir = os.path.normpath(root_dir)
if root_dir not in sys.path or sys.path[0] != root_dir:
    if root_dir in sys.path:
        sys.path.remove(root_dir)
    sys.path.insert(0, root_dir)

import streamlit as st
import pandas as pd
from ollama import chat
import PyPDF2
import docx
from utils.helper import init_page, render_banner

init_page("ConstructAI Assistant")

render_banner(
    "ConstructAI Assistant",
    "Interact with our AI Operations Agent. Ask about budgets, materials, schedules, or safety logs."
)

# Fetch Database
db = st.session_state["db"]
projects = db["projects"]
employees = db["employees"]
materials = db["materials"]
safety = db["safety"]

CONSTRUCTION_KEYWORDS = [
    "construction",
    "project",
    "projects",
    "building",
    "civil",
    "site",
    "budget",
    "cost",
    "expense",
    "material",
    "materials",
    "cement",
    "steel",
    "sand",
    "brick",
    "aggregate",
    "inventory",
    "equipment",
    "worker",
    "workers",
    "workforce",
    "engineer",
    "contractor",
    "client",
    "foundation",
    "column",
    "beam",
    "slab",
    "roof",
    "floor",
    "risk",
    "delay",
    "schedule",
    "planning",
    "progress",
    "quality",
    "inspection",
    "safety",
    "hazard",
    "procurement",
    "vendor",
    "supplier",
    "weather",
    "road",
    "bridge",
    "hospital",
    "school",
    "tower",
    "residential",
    "commercial"
]

def is_construction_query(prompt):

    prompt = prompt.lower()

    for keyword in CONSTRUCTION_KEYWORDS:
        if keyword in prompt:
            return True

    return False



def ask_ai(prompt, validate=True, use_database=True):

    if not is_construction_query(prompt):
        return """
❌ Invalid Prompt

This AI Assistant only supports construction-related queries.

Please ask questions about:

• Construction Projects
• Materials
• Safety
• Workforce
• Budget
• Equipment
• Site Progress
• BOQ
• Tender Documents
"""
    try:

        response = chat(

            model="llama3.2",

            messages=[

                {
                    "role":"system",

                    "content":"""
You are ConstructAI, the AI assistant of the Construction Intelligence Hub.

Rules:

1. Answer ONLY construction and project-related questions.

2. Use ONLY the project database provided.

3. Never make assumptions.

4. Never invent project names, budgets, employees, materials or safety information.

5. If the requested information is not available in the database, reply exactly:

"The requested information is not available in the current Construction Intelligence Hub database."

6. Never answer general knowledge questions.

7. If a question is unrelated to construction, reply:

"I am the Construction Intelligence Hub AI Assistant. Please ask only construction and project-related questions."

8. Keep responses professional, concise and accurate.

9. Format answers using bullet points whenever appropriate.
"""
                },

                {
                    "role": "user",
                    "content": f"""
                Project Database

                Projects:
                {projects.to_string(index=False)}

                Employees:
                {employees.to_string(index=False)}

                Materials:
                {materials.to_string(index=False)}

                Safety:
                {safety.to_string(index=False)}

                User Question:
                {prompt}

                Answer ONLY using the project data above.
                If the answer is not available in the project data, clearly say:

                "The requested information is not available in the current Construction Intelligence Hub database."

                Do not make up information.
                """
                }

            ]

        )

        return response["message"]["content"]

    except Exception as e:

        return f"❌ Ollama Error\n\n{e}"
# Predefined Q&A Map
RESPONSES = {
    "Show delayed projects": (
        "### ⚠️ Delayed Projects Report\n\n"
        "Here are the construction projects currently experiencing schedule delays:\n\n"
        "| Project Name | Location | Progress | Lead Engineer | Health Score |\n"
        "| :--- | :--- | :--- | :--- | :--- |\n"
        + "".join([f"| **{row['Project Name']}** | {row['Location']} | {row['Progress']}% | {row['Lead Engineer']} | {row['Health Score']}/100 |\n" 
                   for _, row in projects[projects["Status"] == "Delayed"].iterrows()]) +
        "\n\n**AI Recommendation:** High risk of penalty clauses. Recommend reallocating idle masonry labor to these sites."
    ),
    "Current budget status": (
        "### 💵 Portfolio Financial Statement\n\n"
        f"**Authorized Budget:** ${projects['Budget'].sum():,.2f}\n\n"
        f"**Disbursed Expenses:** ${projects['Spend'].sum():,.2f}\n\n"
        f"**Remaining Committed Balance:** ${projects['Budget'].sum() - projects['Spend'].sum():,.2f}\n\n"
        "**Financial Status:** Overall portfolio is currently **1.4% under planned budget limits**. However, delayed sites show a combined cost overrun variance of **12.4%**."
    ),
    "Material stock status": (
        "### 📦 Critical Material Alerts\n\n"
        "The following items have fallen below their safety threshold levels:\n\n"
        "| Material SKU | Stock Qty | Min. Threshold | Supplier |\n"
        "| :--- | :--- | :--- | :--- |\n"
        + "".join([f"| {row['Material Name']} | {row['Stock Quantity']} {row['Unit']} | {row['Minimum Stock']} | {row['Supplier']} |\n" 
                   for _, row in materials[materials["Status"] == "Low Stock"].iterrows()]) +
        "\n\n*Purchase requisitions have been auto-drafted for review in the Materials management panel.*"
    ),
    "Workforce summary": (
        "### 👥 Active Personnel Breakdown\n\n"
        f"- **Total Roster Count:** {len(employees)} active workers.\n"
        f"- **Engineers-in-Charge:** {len(employees[employees['Role']=='Engineer'])}\n"
        f"- **Trade Supervisors:** {len(employees[employees['Role']=='Supervisor'])}\n"
        f"- **On-site Laborers:** {len(employees[employees['Role']=='Laborer'])}\n\n"
        f"**Roster Health:** Average attendance is at **{employees['Attendance Rate (%)'].mean():.1f}%** with **92%** of personnel fully active today."
    ),
    "Safety score": (
        "### 🛡️ HSE Safety Compliance Index\n\n"
        f"- **Average Safety Rating:** {safety['Safety Score (HSE)'].mean():.1f}/100\n"
        f"- **Days Since Last Incident:** 342 Days\n"
        f"- **Total Flagged Unresolved Hazards:** {safety['Unresolved Hazards'].sum()}\n\n"
        "**Compliance Status:** 100% OSHA inspection compliance. Daily safety audits are active on all sites."
    ),
    "Project completion": (
        "### 📊 Project Milestones Summary\n\n"
        f"- **Total Monitored Sites:** {len(projects)}\n"
        f"- **Active:** {len(projects[projects['Status']=='Active'])}\n"
        f"- **Completed:** {len(projects[projects['Status']=='Completed'])}\n"
        f"- **Delayed:** {len(projects[projects['Status']=='Delayed'])}\n"
        f"- **Planning:** {len(projects[projects['Status']=='Planning'])}\n\n"
        "Go to the **Project Management** page to drill down into specific site schedules and milestone completions."
    ),
    "Generate report": (
        "### 📄 Executive Analytical Briefs\n\n"
        "I have drafted the consolidated executive brief. You can customize the reporting metrics and download files on the **Reports** page. Available exports:\n\n"
        "- PDF Corporate Audit Summary\n- Excel Financial Transactions Ledger\n- CSV Workforce Metrics"
    )
}

# Chat history initialization in Session State
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "content": "Hello! I am **ConstructAI**, your construction operations assistant. How can I help you today? You can choose one of the quick commands below or enter your question."}
    ]

tab1, tab2, tab3, tab4 = st.tabs([
    "💬 AI Assistant",
    "📄 Document Analyzer",
    "📝 Daily Report",
    "❓ Project Q&A"
])

with tab1:
# Layout Columns
    chat_col, suggestions_col = st.columns([3, 1.2])

    with suggestions_col:
        st.markdown("<h4 style='color: #1E3A8A;'>💡 Quick Commands</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.85rem; color:#64748B;'>Select a query to ask ConstructAI instantly:</p>", unsafe_allow_html=True)
        
        # Render interactive button triggers for suggestions
        for prompt in RESPONSES.keys():
            if st.button(prompt, width="stretch", key=f"btn_{prompt.lower().replace(' ', '_')}"):
                # Append user message
                st.session_state["chat_history"].append({"role": "user", "content": prompt})
                # Append assistant message
                response_content = RESPONSES[prompt]
                st.session_state["chat_history"].append({"role": "assistant", "content": response_content})
                st.rerun()

        st.divider()

        if st.button("📊 Generate AI Project Summary", width="stretch"):

            with st.spinner("🤖 AI is generating the project summary..."):

                prompt = f"""
        Generate a professional construction project summary.

        Projects:
        {len(projects)}

        Active Projects:
        {len(projects[projects['Status']=='Active'])}

        Delayed Projects:
        {len(projects[projects['Status']=='Delayed'])}

        Completed Projects:
        {len(projects[projects['Status']=='Completed'])}

        Budget:
        ${projects['Budget'].sum():,.2f}

        Current Spend:
        ${projects['Spend'].sum():,.2f}

        Employees:
        {len(employees)}

        Low Stock Materials:
        {len(materials[materials['Status']=='Low Stock'])}

        Average Safety Score:
        {safety['Safety Score (HSE)'].mean():.1f}

        Give:
        1. Executive Summary
        2. Project Status
        3. Budget Status
        4. Safety Status
        5. Recommendations
        """

                response = chat(
                    model="llama3.2",
                    messages=[
                        {
                            "role":"user",
                            "content":prompt
                        }
                    ]
                )

                st.session_state["chat_history"].append(
                    {
                        "role":"user",
                        "content":"📊 Generate AI Project Summary"
                    }
                )

                st.session_state["chat_history"].append(
                    {
                        "role":"assistant",
                        "content":response["message"]["content"]
                    }
                )

            st.rerun()

    with chat_col:
        # Render chat container
        st.markdown("<h3 style='color: #1E3A8A;'>💬 ConstructAI Chat Window</h3>", unsafe_allow_html=True)
        
        # Render messages from history
        for msg in st.session_state["chat_history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        # Chat Input Box
        user_input = st.chat_input("Ask about projects, budget, safety, or materials...")
        
        if user_input:
            # Append user message
            st.session_state["chat_history"].append({"role": "user", "content": user_input})
            
            # Determine response
            matched_reply = ask_ai(user_input)
            # Append assistant response
            st.session_state["chat_history"].append({"role": "assistant", "content": matched_reply})
            st.rerun()
            
        # Reset button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat History", width="stretch"):
            st.session_state["chat_history"] = [
                {"role": "assistant", "content": "Hello! I am **ConstructAI**, your construction operations assistant. How can I help you today? You can choose one of the quick commands below or enter your question."}
            ]
            st.rerun()

with tab2:

    st.subheader("📄 AI Document Analyzer")

    st.write(
        "Upload a construction document such as a project report, safety report, tender document, or material report."
    )

    uploaded_file = st.file_uploader(
        "Choose a PDF, DOCX or TXT file",
        type=["pdf", "docx", "txt"]
    )

    text = ""

    if uploaded_file:

        # PDF
        if uploaded_file.type == "application/pdf":

            reader = PyPDF2.PdfReader(uploaded_file)

            for page in reader.pages:
                extracted = page.extract_text()

                if extracted:
                    text += extracted + "\n"

        # TXT
        elif uploaded_file.type == "text/plain":

            text = uploaded_file.read().decode("utf-8")

        # DOCX
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":

            document = docx.Document(uploaded_file)

            for para in document.paragraphs:
                text += para.text + "\n"

        # Preview
        if text:

            st.success("✅ Document uploaded successfully.")

            st.text_area(
                "Extracted Text Preview",
                text[:2000],
                height=250
            )
            construction_keywords = [
                "construction",
                "building",
                "project",
                "contractor",
                "site",
                "cement",
                "concrete",
                "steel",
                "foundation",
                "beam",
                "column",
                "brick",
                "excavation",
                "safety",
                "engineer",
                "architect",
                "tender",
                "boq",
                "material"
            ]

            is_construction_document = any(
                word in text.lower() for word in construction_keywords
            )
            if st.button("🤖 Analyze Document", width="stretch"):

                document_types = [
                    "project report",
                    "construction",
                    "safety report",
                    "site inspection",
                    "construction progress",
                    "material report",
                    "material inventory",
                    "tender",
                    "bill of quantities",
                    "boq",
                    "compliance",
                    "hazard",
                    "risk assessment",
                    "incident",
                    "safety audit"
                ]

                text_lower = text.lower()

                is_construction_document = any(
                    doc in text_lower
                    for doc in document_types
                )

                if not is_construction_document:

                    st.error("""
                    ❌ Invalid Document

                    This document is not related to construction.

                    Please upload only:

                    • Construction Project Report
                    • Safety Report
                    • BOQ (Bill of Quantities)
                    • Tender Document
                    • Material Report
                    • Site Inspection Report
                    • Construction Progress Report
                    """)

                    st.stop()

                else:

                    prompt = f"""
            You are an AI Construction Document Analyzer.

            Analyze the following construction document.

            Provide:

            1. Executive Summary
            2. Key Points
            3. Risks
            4. Recommendations

            {text}
            """

                    with st.spinner("🤖 AI is analyzing..."):

                        result = ask_ai(prompt)

                    st.success("Analysis Complete")

                    st.markdown(result)
                st.download_button(
                    "📥 Download Analysis",
                    data=result,
                    file_name="Document_Analysis.txt",
                    mime="text/plain",
                    width="stretch"
                )

        else:

            st.warning("⚠️ No readable text found in this document.")

with tab3:

    st.subheader("📝 AI Daily Site Report Generator")

    st.write("Generate an AI-powered construction daily report.")

    report_date = st.date_input("Report Date")

    site_engineer = st.text_input("Site Engineer", "John Smith")

    if st.button("🚀 Generate Daily Report", width="stretch"):

        prompt = f"""
You are a Construction Project Manager.

Generate a professional Daily Site Report.

Project Statistics

Total Projects: {len(projects)}

Active Projects: {len(projects[projects['Status']=="Active"])}

Delayed Projects: {len(projects[projects['Status']=="Delayed"])}

Completed Projects: {len(projects[projects['Status']=="Completed"])}

Budget:
${projects['Budget'].sum():,.2f}

Current Spend:
${projects['Spend'].sum():,.2f}

Employees:
{len(employees)}

Average Safety Score:
{safety['Safety Score (HSE)'].mean():.1f}

Low Stock Materials:
{len(materials[materials['Status']=="Low Stock"])}

Report Date:
{report_date}

Engineer:
{site_engineer}

Generate

Executive Summary

Today's Progress

Safety Status

Material Status

Budget Status

Risks

Recommendations

Tomorrow Plan
"""

        with st.spinner("Generating Daily Report..."):

            report = ask_ai(prompt)

        st.success("Daily Report Generated")

        st.markdown(report)

        st.download_button(
            "📥 Download Report",
            report,
            file_name="Daily_Report.txt",
            mime="text/plain",
            width="stretch"
        )

with tab4:

    st.subheader("❓ AI Project Question & Answer")

    st.write("Ask questions about your construction projects.")

    question = st.text_input(
        "Ask a question",
        placeholder="Example: Which project has the highest budget?"
    )

    if st.button("🤖 Ask AI", width="stretch"):

        if not question.strip():
            st.warning("Please enter a question.")
            st.stop()

        if not is_construction_query(question):
            st.error("""
    ❌ Invalid Question

    This AI Project Q&A supports only construction-related questions.

    Please ask about:
    • Projects
    • Materials
    • Safety
    • Workforce
    • Budget
    • Equipment
    • Site Progress
    • Risk Assessment
    """)
            st.stop()

        prompt = f"""
    You are ConstructAI.

    Answer the user's question using ONLY the project database provided below.
    If the answer is not available in the database, reply:
    'The requested information is not available in the current Construction Intelligence Hub database.'

    Project Information

    Projects

    {projects.to_string(index=False)}

    Employees

    {employees.to_string(index=False)}

    Materials

    {materials.to_string(index=False)}

    Safety

    {safety.to_string(index=False)}

    Question

    {question}

    Answer professionally.
    """

        with st.spinner("Thinking..."):

            answer = ask_ai(prompt)

        st.success("Answer")

        st.markdown(answer)