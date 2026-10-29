
import pandas as pd
from sklearn.model_selection import train_test_split

# Load training dataset
df = pd.read_csv("data/processed/phishshift_training.csv")

# Separate messages and labels
X = df["Message"]
y = df["Label"]

# Split into 80% training and 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Total messages:", len(df))
print("Training messages:", len(X_train))
print("Testing messages:", len(X_test))

print("\nTraining label counts:")
print(y_train.value_counts())

print("\nTesting label counts:")
print(y_test.value_counts())
