import streamlit as st
import json
from streamlit_lottie import st_lottie

# Page config for better look
st.set_page_config(page_title="Marcos Ondruska - Portfolio", page_icon="🚀", layout="wide")

# Custom CSS for flashiness: Gradient background, hover effects, Orbitron font
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron&display=swap');
    .stApp {
        background: linear-gradient(to right, #0A2540, #1E90FF);
        color: white;
    }
    a {
        color: #00FF7F !important;
        transition: color 0.3s;
    }
    a:hover {
        color: #FFD700 !important;
    }
    .section-header {
        font-size: 2em;
        color: #00FF7F;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        font-family: 'Orbitron', sans-serif;
    }
    .stExpander {
        transition: transform 0.3s;
    }
    .stExpander:hover {
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# Load Lottie animation from local file
def load_lottie_file(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading animation: {e}. Using fallback.")
        return None

# Load the local Lottie file
lottie_coding = load_lottie_file("Tennis Ball.json")  # Adjust to your file name

# Fallback if Lottie fails
if lottie_coding is None:
    st.markdown("<p style='color: #FFD700;'>Animation unavailable, but check out my portfolio below! 😎</p>", unsafe_allow_html=True)

# Header with effect selector
effect = st.selectbox("Choose an effect", ["Balloons", "Snow"], key="effect_selector")
if effect == "Balloons":
    st.balloons()
else:
    st.snow()

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h1 style='color: #FFD700; font-family: Orbitron, sans-serif;'>Welcome to My Portfolio! 👋</h1>", unsafe_allow_html=True)
    st.write("I'm [Your Name], a [Your Profession] passionate about [your interests]. Here's what I've been up to.")
with col2:
    if lottie_coding:
        st_lottie(lottie_coding, height=200, key="coding_anim")  # Flashy animation

# About Section
st.markdown("<div class='section-header'>About Me</div>", unsafe_allow_html=True)
st.write("""
I'm a creative developer with experience in Python, AI, and web apps. I love building tools that solve real problems in fun ways!
- **Education**: [Your Degree/University]
- **Skills**: Python, Streamlit, Data Science, etc. 💻
""")

# Achievements/Projects Section (LinkedIn-style)
st.markdown("<div class='section-header'>What I've Done 🏆</div>", unsafe_allow_html=True)
projects = [
    {"name": "Project 1", "desc": "Built an AI chatbot that [description].", "link": "https://github.com/yourusername/project1"},
    {"name": "Project 2", "desc": "Developed a data viz app for [description].", "link": "https://github.com/yourusername/project2"},
]
for proj in projects:
    with st.expander(proj["name"], expanded=False):
        st.write(proj["desc"])
        st.markdown(f"[View on GitHub]({proj['link']})")

# Links Section
st.markdown("<div class='section-header'>Connect with Me 🔗</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown("[GitHub](https://github.com/yourusername)")
with col2:
    st.markdown("[X.com (Twitter)](https://x.com/yourusername)")

# Footer
st.markdown("<p style='text-align: center; color: #A9A9A9;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)