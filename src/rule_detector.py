
def detect_phishing_indicators(message):
    indicators = []

    message = message.lower()

    # 1. Detect urgency words
    urgency_words = ["immediately", "urgent", "expires", "blocked"]

    # 2. Detect sensitive information requests
    sensitive_words = [
        "password",
        "otp",
        "bank details",
        "verify your account"
    ]

    # 3. Detect suspicious or defanged URL patterns
    suspicious_url_patterns = [
        "hxxp://",
        "hxxps://",
        "[.]"
    ]

    for word in urgency_words:
        if word in message:
            indicators.append("Urgency: " + word)

    for word in sensitive_words:
        if word in message:
            indicators.append("Sensitive information request: " + word)

    for pattern in suspicious_url_patterns:
        if pattern in message:
            indicators.append("Suspicious URL pattern: " + pattern)

    return indicators


def calculate_risk(indicators):
    count = len(indicators)

    if count == 0:
        return "Low Risk"
    elif count <= 2:
        return "Medium Risk"
    else:
        return "High Risk"