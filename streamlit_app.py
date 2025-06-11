import streamlit as st
import pickle
import pandas as pd
import os
import sys

# Add parent directory to Python path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load trained ML models
with open("models/ml_models/pass_fail_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/ml_models/score_predictor.pkl", "rb") as f:
    score_model = pickle.load(f)

# App Title
st.title("📘 AI-Powered Personalized Learning Assistant (Lite Version)")

# Greeting Section
name = st.text_input("Enter your name")
if name:
    st.success(f"Hi {name.upper()}, let’s start learning!")

# --- Pass/Fail Prediction ---
st.subheader("🎯 Predict Student Pass/Fail")
time_spent = st.slider("Time Spent (seconds)", 60, 600, 120)
past_score = st.slider("Past Score (%)", 0, 100, 50)

if st.button("Predict Pass/Fail"):
    input_df = pd.DataFrame([[time_spent, past_score]], columns=["time_spent", "past_score"])
    result = model.predict(input_df)
    st.success("✅ Result: PASS" if result[0] == 1 else "❌ Result: FAIL")

# --- Score Prediction ---
st.subheader("📈 Predict Future Score")
r_time_spent = st.slider("Time Spent (seconds)", 60, 600, 150, key="score1")
r_difficulty = st.selectbox("Topic Difficulty (1 = Easy, 3 = Hard)", [1, 2, 3])
r_attempts = st.slider("Number of Attempts", 1, 5, 2)

if st.button("Predict Score"):
    input_df = pd.DataFrame([[r_time_spent, r_difficulty, r_attempts]],
                            columns=["time_spent", "difficulty", "num_attempts"])
    predicted_score = score_model.predict(input_df)[0]
    st.success(f"🎯 Predicted Score: {round(predicted_score, 2)} out of 100")
