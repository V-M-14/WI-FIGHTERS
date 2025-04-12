import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

def generate_roadmap(user_info, goal):
    prompt = f"""
Act as a friendly and professional career roadmap mentor.

The student has the following background: {user_info}
Their career goal is: {goal}

Your job is to generate a **realistic and personalized** career roadmap to help the student reach their goal.

**Instructions**:
- Do NOT fix the roadmap to 8 weeks. Use your best judgment to decide how many weeks or phases are needed.
- For each week or phase, include:
  - A clear topic or goal
  - A short, engaging description
  - Links for learning resources (YouTube, Coursera, edX, or PDFs) **mandatory**
  - Estimated time commitment
- Make the tone conversational and encouraging — as if you're directly guiding the student.

When suggesting resources, only include links from verified websites like:
- YouTube (with working video titles)
- Coursera (with exact course name)
- FreeCodeCamp
- EdX
If unsure of the exact link, only mention the course name and platform.
Avoid making up URLs.


📍 At the end, include a **Final Milestone** titled
- This should feel like a personal note to the student.
- Explain what they’ve accomplished and how they can now apply for jobs, internships, or freelance gigs.
- Be supportive and motivating, as if you're celebrating their journey and encouraging them to take the leap.

Avoid generic or robotic tone. Be helpful, uplifting, and practical.
"""
    response = openai.ChatCompletion.create(
        model="mistralai/mistral-7b-instruct",  # or meta-llama/llama-3-8b-instruct
        messages=[
            {"role": "system", "content": "You are a professional career coach helping students build personalized learning roadmaps."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']




# --- Streamlit UI Starts Here ---
if not st.session_state.get('logged_in'):
        st.warning("Please login first.")
        st.stop()

st.set_page_config(page_title="Career GPS", layout="wide")

# Top row with "Track My Progress" and "Logout" buttons
spacer_col, button_col1, button_col2 = st.columns([0.8, 0.1, 0.1]) 

with button_col1:
    if st.button("Track My Progress", use_container_width=True, key="track_progress_button"):
        st.switch_page("pages/Progress_tracker.py") # Make sure this path is correct

with button_col2:
    if st.button("Logout", use_container_width=True, key="logout_button"):
        st.session_state.clear()
        st.switch_page("main.py")  

        
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