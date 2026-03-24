# Step 1: Take input from user
import pandas as pd
tasks = []

n = int(input("Enter number of subjects: "))

for i in range(n):
    print(f"\nEnter details for subject {i+1}")
    
    name = input("Subject name: ")
    deadline = int(input("Days left for exam: "))
    difficulty = int(input("Difficulty (1-5): "))
    hours = int(input("Study hours needed: "))
    
    tasks.append([name, deadline, difficulty, hours])

df = pd.DataFrame(tasks, columns=["Subject", "Deadline", "Difficulty", "Hours"])

# Priority calculation
from sklearn.linear_model import LinearRegression

# Prepare data
X = df[["Deadline", "Difficulty", "Hours"]]

# Dummy training target (your formula as base learning)
y = (df["Difficulty"] * df["Hours"]) / df["Deadline"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Predict priority
df["Priority"] = model.predict(X)

# Sort
df = df.sort_values(by="Priority", ascending=False)

print("\n🔥 Final Study Plan (Table):")
print(df)

print("\n📅 Suggested Study Plan:")

for i, row in df.iterrows():
    print(f"👉 Study {row['Subject']} for {row['Hours']} hours (Priority: {round(row['Priority'],2)})")