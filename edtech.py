import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

def generate_roadmap(user_info, goal):
    prompt = f"""
Act as a career roadmap mentor.
The student has the following background: {user_info}
Their career goal is: {goal}
Generate an 8-week roadmap to help them achieve this goal. 
Each week should have: 
- Topic
- Short description
- One or two resources (preferably free: YouTube, Coursera, edX, or PDFs)
- Estimated time
"""
    response = openai.ChatCompletion.create(
        model="mistralai/mistral-7b-instruct",  # or try meta-llama/llama-3-8b-instruct
        messages=[
            {"role": "system", "content": "You are a professional career coach helping students build personalized learning roadmaps."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']



# --- Streamlit UI Starts Here ---

st.set_page_config(page_title="Career GPS", layout="wide")

st.title("📍 Career GPS: Your Personalized Career Roadmap")
st.markdown("Welcome! Let's build your custom career roadmap step by step.")

# Section 1: Upload Resume or Enter Skills
st.header("Step 1: Tell us about your background")
option = st.radio("How would you like to input your background?", ["Type it manually", "Upload Resume"])

user_info = ""

if option == "Type it manually":
    user_info = st.text_area("Enter your current skills, past courses, or projects", placeholder="E.g., I know Python and basic SQL. I watched some YouTube tutorials on data analysis.")
elif option == "Upload Resume":
    uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
    if uploaded_file:
        user_info = uploaded_file.read().decode("utf-8", errors="ignore")

# Section 2: Career Goal
st.header("Step 2: Choose your career goal")
career_goal = st.text_input("What do you want to become?", placeholder="E.g., Data Analyst")

# Generate Button
if st.button("🚀 Generate My Roadmap"):
    if user_info and career_goal:
        with st.spinner("Generating your personalized roadmap..."):
            roadmap = generate_roadmap(user_info, career_goal)
            st.success("Here's your roadmap! 💡")
            st.markdown(roadmap)
    else:
        st.warning("Please provide both your background and a career goal.")

# Footer
st.markdown("---")
st.caption("Made with ❤️ at the Hackathon using OpenAI + Streamlit")