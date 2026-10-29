
import pandas as pd

df = pd.read_csv("data/processed/phishshift_cleaned.csv")

conflicts = (
    df.groupby("Message")["Label"]
    .nunique()
)

conflict_messages = conflicts[conflicts > 1].index

result = df[df["Message"].isin(conflict_messages)]

result.to_csv(
    "data/processed/label_conflicts.csv",
    index=False
)

print("Conflicting messages:", len(conflict_messages))
print("Saved to data/processed/label_conflicts.csv")
