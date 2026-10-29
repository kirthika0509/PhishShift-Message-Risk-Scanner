import streamlit as st
import joblib

from src.rule_detector import (
    detect_phishing_indicators,
    calculate_risk
)

# --------------------------------
# 1. Page Configuration
# --------------------------------

st.set_page_config(
    page_title="PhishShift Message Risk Scanner",
    page_icon="🛡️",
    layout="centered"
)

# --------------------------------
# 2. Load the Trained ML Model
# --------------------------------

model = joblib.load("models/phishshift_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

# --------------------------------
# 3. Application Title
# --------------------------------

st.title("🛡️ PhishShift Message Risk Scanner")

st.write(
    "Analyze messages for potential phishing "
    "and social engineering threats."
)

st.caption(
    "This tool provides preliminary risk indicators, "
    "not a guarantee that a message is safe or malicious."
)

# --------------------------------
# 4. Message Input
# --------------------------------

message = st.text_area(
    "Enter your message:",
    placeholder="Paste your email, SMS, or message here...",
    height=150
)

# Initial review threshold
CONFIDENCE_THRESHOLD = 60.0

# --------------------------------
# 5. Analyze Message
# --------------------------------

if st.button("Analyze Message", type="primary"):

    if message.strip():

        # --------------------------------
        # 5A. Machine Learning Prediction
        # --------------------------------

        message_tfidf = vectorizer.transform([message])

        prediction = model.predict(message_tfidf)[0]

        probabilities = model.predict_proba(message_tfidf)[0]

        confidence = max(probabilities) * 100

        # --------------------------------
        # 5B. Rule-Based Detection
        # --------------------------------

        indicators = detect_phishing_indicators(message)

        risk_level = calculate_risk(indicators)

        # --------------------------------
        # 6. Display ML Analysis
        # --------------------------------

        st.subheader("📊 ML Analysis")

        if confidence < CONFIDENCE_THRESHOLD:

            st.warning("⚠️ Review Required")

            st.write(
                "The model is uncertain about this message's category."
            )

            st.write("Suggested Category:", prediction)

            st.write(f"Model Confidence: {confidence:.2f}%")

            st.write(
                "Please review the message manually before "
                "making a decision."
            )

        else:

            st.write("Predicted Category:", prediction)

            st.write(f"Model Confidence: {confidence:.2f}%")

        # --------------------------------
        # 7. Display Suspicious Indicators
        # --------------------------------

        st.subheader("🔎 Suspicious Indicators")

        if indicators:

            for indicator in indicators:
                st.warning(indicator)

        else:

            st.success(
                "No indicators covered by the current rules "
                "were detected."
            )

        # --------------------------------
        # 8. Display Rule-Based Risk
        # --------------------------------

        st.subheader("⚠️ Rule-Based Risk Assessment")

        if risk_level == "High Risk":

            st.error(risk_level)

        elif risk_level == "Medium Risk":

            st.warning(risk_level)

        else:

            st.info(risk_level)

        # --------------------------------
        # 9. Safety Explanation
        # --------------------------------

        st.info(
            "These results are indicators, not proof that a "
            "message is malicious or safe. A legitimate message "
            "can contain suspicious-looking words, and a malicious "
            "message may avoid these indicators. Review the message "
            "and its context before making a decision."
        )

    else:

        st.warning("Please enter a message first.")

# --------------------------------
# 10. Footer
# --------------------------------

st.divider()

st.caption(
    "PhishShift Message Risk Scanner | "
    "Machine Learning + Rule-Based Analysis"
)