
import pandas as pd
from pathlib import Path

# Load the cleaned dataset
input_path = Path("data/processed/phishshift_cleaned.csv")
df = pd.read_csv(input_path)

# Find messages that have more than one label
conflict_counts = df.groupby("Message")["Label"].nunique()
conflict_messages = conflict_counts[conflict_counts > 1].index

# Exclude conflicting messages from training data
training_df = df[~df["Message"].isin(conflict_messages)].copy()

# Save as a separate file
output_path = Path("data/processed/phishshift_training.csv")
training_df.to_csv(output_path, index=False)

print("Original cleaned rows:", len(df))
print("Conflicting messages excluded:", len(conflict_messages))
print("Training dataset rows:", len(training_df))
print("Saved to:", output_path)
