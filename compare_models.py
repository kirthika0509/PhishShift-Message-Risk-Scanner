from pathlib import Path

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

from src.rule_detector import detect_phishing_indicators


# 1. Load dataset
data_path = Path("data/processed/phishshift_training.csv")
df = pd.read_csv(data_path)

X = df["Message"].fillna("").astype(str)
y = df["Label"]

# 2. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# 3. Convert messages into TF-IDF features
vectorizer = TfidfVectorizer(ngram_range=(1, 2))

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


# 4. Define ML models
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Multinomial Naive Bayes": MultinomialNB()
}

results = []


# 5. Train and evaluate ML models
for name, model in models.items():

    print("\n" + "=" * 60)
    print("Model:", name)

    model.fit(X_train_tfidf, y_train)
    predictions = model.predict(X_test_tfidf)

    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(
        y_test, predictions, average="macro", zero_division=0
    )

    recall = recall_score(
        y_test, predictions, average="macro", zero_division=0
    )

    f1 = f1_score(
        y_test, predictions, average="macro", zero_division=0
    )

    results.append({
        "Method": name,
        "Accuracy (%)": round(accuracy * 100, 2),
        "Macro Precision (%)": round(precision * 100, 2),
        "Macro Recall (%)": round(recall * 100, 2),
        "Macro F1 (%)": round(f1 * 100, 2)
    })

    print(classification_report(
        y_test, predictions, zero_division=0
    ))


# 6. Evaluate the rule-based detector separately
print("\n" + "=" * 60)
print("Rule-Based Detector Evaluation")

rule_indicators = [
    detect_phishing_indicators(message)
    for message in X_test
]

# An indicator-based detector cannot directly predict
# the six original dataset categories.
# For a basic binary evaluation, treat every non-benign
# label as malicious and the benign label as non-malicious.
actual_binary = (
    y_test != "NOT-Malicious General Class"
).astype(int)

# A message is flagged when at least one rule is triggered.
predicted_binary = pd.Series(
    [1 if indicators else 0 for indicators in rule_indicators],
    index=y_test.index
)

rule_accuracy = accuracy_score(actual_binary, predicted_binary)

rule_precision = precision_score(
    actual_binary, predicted_binary, zero_division=0
)

rule_recall = recall_score(
    actual_binary, predicted_binary, zero_division=0
)

rule_f1 = f1_score(
    actual_binary, predicted_binary, zero_division=0
)

print("Binary accuracy:", round(rule_accuracy * 100, 2), "%")
print("Binary precision:", round(rule_precision * 100, 2), "%")
print("Binary recall:", round(rule_recall * 100, 2), "%")
print("Binary F1:", round(rule_f1 * 100, 2), "%")

print("\nRule-based binary classification report:")
print(classification_report(
    actual_binary,
    predicted_binary,
    labels=[0, 1],
    target_names=["Non-malicious", "Malicious"],
    zero_division=0
))


# 7. Save ML comparison
results_df = pd.DataFrame(results)

print("\nML MODEL COMPARISON")
print(results_df.to_string(index=False))

Path("reports").mkdir(exist_ok=True)

results_df.to_csv(
    "reports/model_comparison.csv",
    index=False
)

# Save rule-based metrics separately because it is
# evaluated as a binary detector, not a six-class model.
rule_results = pd.DataFrame([{
    "Method": "Rule-Based Detector",
    "Task": "Binary: malicious vs non-malicious",
    "Accuracy (%)": round(rule_accuracy * 100, 2),
    "Precision (%)": round(rule_precision * 100, 2),
    "Recall (%)": round(rule_recall * 100, 2),
    "F1 (%)": round(rule_f1 * 100, 2)
}])

rule_results.to_csv(
    "reports/rule_based_evaluation.csv",
    index=False
)

print("\nML comparison saved to reports/model_comparison.csv")
print("Rule evaluation saved to reports/rule_based_evaluation.csv")