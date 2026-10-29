from pathlib import Path

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GroupShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# 1. Load the dataset
data_path = Path("data/processed/phishshift_training.csv")
df = pd.read_csv(data_path)

df = df.dropna(subset=["Message", "Label"]).copy()
df["Message"] = df["Message"].astype(str)

# 2. Create approximate template groups
# These are text-based estimates, not verified campaign IDs.
df["Template_Group"] = (
    df["Message"]
    .str.lower()
    .str.replace(r"https?://\S+|www\.\S+", " URL ", regex=True)
    .str.replace(r"\b\d+\b", " NUMBER ", regex=True)
    .str.replace(r"[^a-z\s]", " ", regex=True)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# 3. Check grouping
print("Total messages:", len(df))
print("Unique approximate template groups:",
      df["Template_Group"].nunique())

# 4. Split by approximate template groups
splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=42
)

train_idx, test_idx = next(
    splitter.split(
        df["Message"],
        df["Label"],
        groups=df["Template_Group"]
    )
)

train_df = df.iloc[train_idx]
test_df = df.iloc[test_idx]

print("\nTraining messages:", len(train_df))
print("Testing messages:", len(test_df))

print("\nTraining label counts:")
print(train_df["Label"].value_counts())

print("\nTesting label counts:")
print(test_df["Label"].value_counts())

# 5. Check whether the test labels exist in training
missing_labels = set(test_df["Label"]) - set(train_df["Label"])

if missing_labels:
    print("\nEvaluation cannot reliably cover all test labels.")
    print("Labels missing from training:", missing_labels)

else:
    # 6. Convert messages into TF-IDF features
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))

    X_train = vectorizer.fit_transform(train_df["Message"])
    X_test = vectorizer.transform(test_df["Message"])

    y_train = train_df["Label"]
    y_test = test_df["Label"]

    # 7. Train and evaluate the model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("\nApproximate Template-Holdout Accuracy:",
          round(accuracy * 100, 2), "%")

    print("\nClassification Report:")
    print(classification_report(
        y_test,
        predictions,
        zero_division=0
    ))

    # 8. Save the evaluation report
    Path("reports").mkdir(exist_ok=True)

    report = classification_report(
        y_test,
        predictions,
        output_dict=True,
        zero_division=0
    )

    pd.DataFrame(report).transpose().to_csv(
        "reports/template_holdout_report.csv"
    )

    print("\nReport saved to reports/template_holdout_report.csv")
    print(
        "Note: These are approximate template groups, "
        "not verified campaign groups."
    )