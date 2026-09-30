# 📝 AI Meeting Notes Analyzer

![web_page](web_page1.png)


![web_page](web_page2.png)


![web_page](web_page3.png)


![web_page](web_page4.png)

An AI-powered meeting analysis application built using **Google Gemini, LangGraph, and Streamlit**.

The application takes a meeting transcript as input and automatically analyzes it to extract important information such as **key topics, meeting summary, action items, task owners, deadlines, and task priorities**.

---

## 📌 Project Overview

In meetings, important decisions, responsibilities, and deadlines are often scattered throughout lengthy discussions. Manually reviewing meeting transcripts can be time-consuming and may result in important action items being missed.

The **AI Meeting Notes Analyzer** automates this process using Generative AI and an Agentic AI workflow.

The user provides a meeting transcript, and the application processes it through multiple specialized agents using **LangGraph**.

The final results are displayed through an interactive **Streamlit interface**.

---

## 🎯 Objectives

The main objectives of this project are:

- Extract important topics from a meeting transcript
- Generate a concise meeting summary
- Identify actionable tasks
- Identify the person responsible for each task
- Extract deadlines associated with action items
- Classify the priority of action items
- Handle meetings where no action items are identified
- Present the analysis through an easy-to-use Streamlit interface

---

## 🚀 Key Features

### 🔑 Key Topic Extraction

Identifies the major topics discussed during the meeting.

Example:

```text
- Website performance improvement
- Database optimization
- Homepage redesign
