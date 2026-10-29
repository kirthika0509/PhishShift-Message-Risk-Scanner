
import pandas as pd
from pathlib import Path

# 1. Load original dataset
input_path = Path("data/raw/phishing_nlp_dataset.xlsx")
df = pd.read_excel(input_path)

labels = [
    "NOT-Malicious General Class",
    "Phishing",
    "Malware",
    "Scareware",
    "Baiting",
    "Pretexting"
]

# 2. Recover labels from both columns
def extract_label(row):
    for column in ["Corpus", "Labels"]:
        value = row[column]

        if isinstance(value, str):
            text = value.rstrip()

            for label in labels:
                if text.endswith("\t" + label):
                    return label

    return None

df["Label"] = df.apply(extract_label, axis=1)

# 3. Combine message parts and remove label suffixes
def get_message(row):
    parts = []

    for column in ["Corpus", "Labels"]:
        value = row[column]

        if isinstance(value, str):
            text = value.rstrip()

            for label in labels:
                suffix = "\t" + label
                if text.endswith(suffix):
                    text = text[:-len(suffix)]
                    break

            if text.strip():
                parts.append(text.strip())

    return " ".join(parts).strip()

df["Message"] = df.apply(get_message, axis=1)

# 4. Keep only rows with valid message and label
clean_df = df[["Message", "Label"]].copy()
clean_df = clean_df.dropna(subset=["Message", "Label"])
clean_df = clean_df[
    (clean_df["Message"].str.strip() != "") &
    (clean_df["Label"].isin(labels))
]


# 5. Check duplicate messages with conflicting labels

label_counts_per_message = clean_df.groupby("Message")["Label"].nunique()

conflicting_messages = label_counts_per_message[
    label_counts_per_message > 1
].index

print("\nMessages with different labels:")
print(
    clean_df[clean_df["Message"].isin(conflicting_messages)]
    .sort_values("Message")
    .to_string(index=False)
)

print("\nNumber of messages with conflicting labels:",
      len(conflicting_messages))

# Remove only exact duplicates with the same message AND label
clean_df = clean_df.drop_duplicates(
    subset=["Message", "Label"]
).reset_index(drop=True)
# 6. Save cleaned dataset
output_path = Path("data/processed")
output_path.mkdir(parents=True, exist_ok=True)

clean_df.to_csv(
    output_path / "phishshift_cleaned.csv",
    index=False
)

# 7. Display results
print("Original rows:", len(df))
print("Cleaned rows:", len(clean_df))
print("Missing values:\n", clean_df.isnull().sum())
print("Duplicate messages:", clean_df["Message"].duplicated().sum())
print("\nLabel counts:\n", clean_df["Label"].value_counts())
print("\nSaved to:", output_path / "phishshift_cleaned.csv")


print("\nSample cleaned messages:")
print(clean_df.head(5).to_string(index=False))

print("\nRows per label:")
print(clean_df.groupby("Label").size())

print("\nShort or suspiciously small messages:")
print(
    clean_df.loc[
        clean_df["Message"].str.len() < 20,
        ["Message", "Label"]
    ].to_string(index=False)
)

print("\nOriginal label counts:")
print(df["Label"].value_counts(dropna=False))

print("\nRows without a recovered label:")
print(
    df.loc[
        df["Label"].isna(),
        ["Corpus", "Labels"]
    ].to_string(index=False)
)

print("\nRows removed during cleaning:")
print("Rows removed:", len(df) - len(clean_df))

