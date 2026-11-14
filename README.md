# IIS A2 — AI Answer Verification

## Project Overview

This project is a prototype of an intelligent interactive system designed to help users evaluate the reliability of AI-generated answers.

The system uses two LLM API calls. AI1 generates an answer to the user's question, while AI2 examines the factual claims in that answer and provides a preliminary assessment.

Users can also give feedback, report potential problems and request a reassessment.

**Important:** The system currently relies on LLM knowledge for fact assessment. It does not independently retrieve or verify external sources.

## Project Status

**Implemented:**
- AI1 answer generation using an LLM API.
- AI2 preliminary fact assessment using the original question and AI1's answer.
- Streamlit web interface for questions and results.
- Session state management to preserve results during interaction.
- User feedback and issue reporting.
- Request Recheck, allowing AI2 to reconsider its previous assessment using user feedback.

**Not implemented / Planned:**
- Automatic retrieval and independent verification of external sources.
- Persistent storage of feedback and reports.
- Automatic learning or model training from user feedback.

## Technology Stack

- **Python:** Application logic and API integration.
- **Streamlit:** Web interface and interaction management.
- **OpenAI Python SDK:** Communication with an OpenAI-compatible LLM API.
- **Qwen:** LLM used for answer generation and preliminary assessment.
- **python-dotenv:** Loading local configuration.

AI1and AI2are separate API calls with different instructions. They do not require two separate API keys.

## How to Run

**1. Install dependencies**

Python is required. The project was developed using Python 3.12.

Run:

`python -m pip install -r requirements.txt`

**2. Configure the API**

Copy `.env.example` to `.env`, then provide a valid `LLM_API_KEY`.

Alternatively, configure `LLM_API_KEY` as an operating-system environment variable.

The API endpoint and model name are configured using `LLM_BASE_URL` and `LLM_MODEL`.

Do not publish API keys.

**3. Start the application**

Run:

`python -m streamlit run app.py`

Open `http://localhost:8501` in a browser.

**4. Use the system**

Enter a question and click **Ask AI**. After reviewing AI1's answer and AI2's assessment, the user can select a feedback option.

If the assessment seems incorrect, the user can submit an issue and select **Request Recheck**.

Browser automatic translation may interfere with the interface. Using the original webpage language is recommended.

## Development Record

The initial development took place locally before Git version control was initialised. The stages below are a retrospective summary of that work.

**Stage 1 — Initial Python Prototype**
Created basic Python functions and used simulated responses to understand input, output, function parameters and data flow.

**Stage 2 — LLM API Integration**
Connected the program to an LLM API. Implemented answer generation and a second API call for preliminary factual assessment.

Updated AI2 to receive both the original question and AI1's answer to preserve context.

**Stage 3 — Streamlit Interface**
Developed a web interface with a question input field, Ask AI button, and separate sections for AI1 and AI2.

**Stage 4 — Feedback and State Management**
Added feedback buttons and used Streamlit session state to retain answers during interaction without unnecessarily repeating API calls.

**Stage 5 — Failure and Recovery**
Added issue reporting and Request Recheck. Users can explain why they disagree with an assessment, and AI2 can reconsider its previous judgement.

The reassessment does not automatically train the model or independently verify sources.

## AI Assistance

ChatGPT was used to support learning Python, understanding API calls, designing functions, debugging code, improving prompts, and implementing Streamlit interactions.

I reviewed and modified the suggested code and tested the application manually, including its answer-generation, feedback and reassessment flows.

AI-generated suggestions and factual assessments were not assumed to be correct without review. External source verification remains a limitation of the current system.

## Additional Notes

- API credentials are excluded from Git version control.
- Feedback and results are stored temporarily in the current Streamlit session.
- The application has been tested locally and has not been deployed as a public online service.
- The initial Git commit represents the existing locally developed prototype, not the beginning of the development process.