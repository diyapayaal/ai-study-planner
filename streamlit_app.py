import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="AI Study Planner", layout="centered")

# Clean Dark UI
st.markdown("""
<style>
/* Background */
.stApp {
    background-color: #0b0f14;
    color: #e5e7eb;
}

/* Headings */
h1 {
    font-size: 2.5rem;
    font-weight: 700;
    color: #ffffff;
}
h2, h3 {
    color: #d1d5db;
}

/* Input boxes */
input, .stNumberInput input {
    background-color: #111827 !important;
    color: #e5e7eb !important;
    border: 1px solid #374151 !important;
    border-radius: 8px;
}

/* Button */
.stButton>button {
    width: 100%;
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    height: 2.8em;
    font-weight: 600;
    border: none;
}

/* Card style */
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("AI Smart Study Planner")
st.markdown("Minimal. Focused. Effective.")

st.divider()

# Input
st.subheader("Study Input")

num_subjects = st.number_input("Number of Subjects", min_value=1, step=1)

tasks = []

for i in range(int(num_subjects)):
    st.markdown(f"### Subject {i+1}")
    
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Subject Name", key=f"name_{i}")
        difficulty = st.slider("Difficulty", 1, 5, key=f"difficulty_{i}")

    with col2:
        deadline = st.number_input("Days Left", min_value=1, key=f"deadline_{i}")
        hours = st.number_input("Study Hours", min_value=1, key=f"hours_{i}")

    tasks.append([name, deadline, difficulty, hours])

st.divider()

# Generate
if st.button("Generate Plan"):

    df = pd.DataFrame(tasks, columns=["Subject", "Deadline", "Difficulty", "Hours"])

    df["Priority"] = (df["Difficulty"] * df["Hours"]) / df["Deadline"]
    df = df.sort_values(by="Priority", ascending=False)

    # Table
    st.subheader("Plan Overview")
    st.dataframe(df, use_container_width=True)

    # Graph
    st.subheader("Priority Analysis")
    st.bar_chart(df.set_index("Subject")["Priority"])

    # Top focus
    top = df.iloc[0]
    st.subheader("Primary Focus")
    st.markdown(f"""
    <div style="padding:12px;border:1px solid #374151;border-radius:8px;background:#111827">
        <b>{top['Subject']}</b><br>
        Priority: {round(top['Priority'],2)}<br>
        Study Time: {top['Hours']} hrs
    </div>
    """, unsafe_allow_html=True)

    # Suggestions
    st.subheader("Insights")

    for _, row in df.iterrows():
        if row["Deadline"] <= 2:
            st.write(f"- {row['Subject']} requires immediate attention.")
        elif row["Difficulty"] >= 4:
            st.write(f"- {row['Subject']} needs deeper focus sessions.")

    # Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Plan", csv, "study_plan.csv", "text/csv")