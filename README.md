# 🛡️ PhishShift Message Risk Scanner

Analyze messages for potential phishing and social engineering threats using machine learning and rule-based checks.

> **Important:** This tool provides preliminary risk indicators. It cannot guarantee that a message is safe or malicious. Always review suspicious messages and their context before taking action.

## 📌 Project Overview

PhishShift Message Risk Scanner is a web application built with Python and Streamlit. It analyzes a message and displays a machine-learning prediction, model confidence, suspicious indicators, and a rule-based risk assessment.

The application is designed to help users recognize warning signs commonly associated with phishing and social engineering messages.

## ✨ Features

- **Machine-learning analysis:** Predicts the message category using the project's trained model.
- **Confidence display:** Shows the model's confidence for its prediction.
- **Suspicious-indicator detection:** Highlights selected warning signs, such as urgency language and requests for sensitive information.
- **Rule-based risk assessment:** Provides a risk level based on the application's configured rules.
- **Empty-input validation:** Prompts the user to enter a message when the input is empty.
- **Web interface:** Provides an interface built with Streamlit.
- **Online deployment:** The app is available through Streamlit Community Cloud.

## 🧰 Technologies Used

- Python
- Streamlit
- Machine learning (using the model and libraries configured in this project)
- Rule-based text checks
- Git and GitHub
- Streamlit Community Cloud

## 🚀 Try the Live Application

**Live app:** https://phishshift-message-risk-scanner-wqczyr4duxmyt5wux39ajq.streamlit.app

## 💻 Run the Project Locally

### Prerequisites

- Python installed on your computer
- Git (optional, if you clone the repository)
- Internet access to install the required packages

### 1. Clone the repository

```bash
git clone https://github.com/kirthika0509/PhishShift-Message-Risk-Scanner.git
cd PhishShift-Message-Risk-Scanner
```

### 2. Create and activate a virtual environment (recommended)

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
streamlit run app.py
```

Streamlit will show a local URL in the terminal. Open that URL in your browser.

## 📝 How to Use

1. Open the application.
2. Enter or paste the message you want to inspect.
3. Click **Analyze Message**.
4. Review the predicted category and model confidence.
5. Check the suspicious indicators and rule-based risk assessment.
6. Consider the message's source and context before deciding what to do.

## 🧪 Basic Functional Checks

The following checks have been tried during project testing:

| Test case | Observed behavior |
|---|---|
| Suspicious prize message | Phishing was suggested; suspicious indicators were displayed |
| Ordinary meeting message | No suspicious indicators were detected; low risk was reported |
| Suspicious bank-account message | Phishing was suggested; high risk was reported |
| Empty message | The app displayed a prompt to enter a message |

These are basic functional checks, not a complete evaluation of model accuracy. Predictions and confidence scores can vary depending on the message and model.

## ⚠️ Limitations and Safety

- A high-risk result is a warning, not proof that a message is malicious.
- A low-risk result does not guarantee that a message is safe.
- Legitimate messages may contain urgent language, and malicious messages may not contain obvious warning words.
- Model confidence is not the same as verified real-world accuracy.
- Do not enter passwords, verification codes, banking details, or other private information into test messages.
- Verify requests through an official website or contact method rather than relying only on a message's links or contact details.

## 📁 Main Project Files

- `app.py` — Streamlit application entry point.
- `requirements.txt` — Python package dependencies.
- `.gitignore` — Files and folders Git should ignore.
- Other model, data, and helper files — used by the project as included in the repository.

## 🔮 Future Improvements

- Evaluate the model on a separate, labeled test dataset.
- Report evaluation metrics such as precision, recall, F1-score, and a confusion matrix.
- Expand testing to include different phishing and legitimate-message examples.
- Improve detection while reducing false positives.
- Add clear explanations for why a message receives a particular risk level.

## 👩‍💻 Author

**Project:** PhishShift Message Risk Scanner  
**GitHub repository:** https://github.com/kirthika0509/PhishShift-Message-Risk-Scanner

---

*This project is an educational and preliminary message-analysis tool. It should support, not replace, careful human judgment.*
