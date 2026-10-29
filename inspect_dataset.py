
import pandas as pd

df = pd.read_excel("data/raw/phishing_nlp_dataset.xlsx")

labels = [
    "NOT-Malicious General Class",
    "Phishing",
    "Malware",
    "Scareware",
    "Baiting",
    "Pretexting"
]

def extract_label(row):
    for column in ["Corpus", "Labels"]:
        value = row[column]

        if isinstance(value, str):
            text = value.rstrip()

            for label in labels:
                if text.endswith("\t" + label):
                    return label

    return None


df["Recovered_Label"] = df.apply(extract_label, axis=1)

print("Total messages:", len(df))
print("\nLabel counts:")
print(df["Recovered_Label"].value_counts(dropna=False))

