#!/usr/bin/env python3
import streamlit as st
import json
import os
import html
from typing import List, Optional, Tuple, Any
from streamlit_lottie import st_lottie

# --------------------------
#     PAGE CONFIG
# --------------------------
st.set_page_config(page_title="Marcos Ondruska — Portfolio", page_icon="🎾", layout="wide")

# --------------------------
#     LINKS / CONTACT
# --------------------------
LINKEDIN_URL = "https://www.linkedin.com/in/marcos-ondruska-3b3a749/"
GITHUB_URL   = "https://github.com/drussie"                      # <- set your GitHub profile if you want
X_URL        = "https://x.com/drussie"                           # <- set your X/Twitter handle if you want
EMAIL        = "marcosondruska@gmail.com"
ROUND_ROBIN_APP = "https://marcoswebpage-k3rbpwxme7nzgk5rwdee3c.streamlit.app/"

# --------------------------
#     GLOBAL STYLES
# --------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700&family=Inter:wght@400;600&display=swap');
    :root {
        --brand-gold: #FFD700;
        --brand-mint: #00FF7F;
        --brand-bg1: #0A2540;
        --brand-bg2: #1E90FF;
        --pill-bg: rgba(255,255,255,0.10);
        --pill-brd: rgba(255,255,255,0.28);
        --pill-txt: #EAF2FF;
        --pill-hover: rgba(255,215,0,0.20);
    }
    .stApp { background: linear-gradient(135deg, var(--brand-bg1), var(--brand-bg2)); color: white; }
    .block-container { max-width: 1100px; padding-top: 1rem; padding-bottom: 2rem; margin: 0 auto; }

    h1,h2,h3,.section-header {
      font-family: 'Orbitron', sans-serif;
      letter-spacing: .5px;
      text-shadow: 0 4px 18px rgba(0,0,0,.35);
    }
    .hero-title { color: var(--brand-gold); font-size: 40px; margin: 0 0 6px 0; }
    .hero-sub   { color: #E6F0FF; font-family: 'Inter', sans-serif; font-size: 18px; margin-bottom: 16px; }

    a, .stButton>button { transition: all .2s ease; }
    a { color: var(--brand-mint) !important; text-decoration: none; }
    a:hover { color: var(--brand-gold) !important; text-decoration: underline; }

    .btn-row .stButton>button {
      background: rgba(255,255,255,0.1);
      color: white;
      border: 1px solid rgba(255,255,255,0.25);
      padding: 10px 16px;
      border-radius: 10px;
      box-shadow: 0 8px 24px rgba(0,0,0,.2);
    }
    .btn-row .stButton>button:hover { transform: translateY(-1px); border-color: var(--brand-gold); }

    .card {
      background: rgba(255,255,255,0.07);
      border: 1px solid rgba(255,255,255,0.18);
      border-radius: 14px;
      padding: 16px 18px;
      box-shadow: 0 10px 32px rgba(0,0,0,.25);
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
      margin-bottom: 16px;
    }
    .section-header { font-size: 26px; color: var(--brand-mint); margin: 8px 0 10px; }
    .muted { color: #D6E4FF; opacity: .9; }

    /* Make JUST the About Me header smaller + tighter spacing */
    .section-header.about { 
      font-size: 20px;            /* smaller than default 26px */
      margin: 4px 0 6px;          /* tighter spacing */
    }
    .about-card { 
      padding: 14px 16px;         /* slightly tighter padding */
    }
    .about-card p { 
      margin: 0 0 8px;            /* reduce paragraph gaps */
      line-height: 1.35;          /* tighter line height */
    }

    .stExpander { transition: transform .2s ease; }
    .stExpander:hover { transform: translateY(-2px); }

    /* --- Pill (badge wall) styles --- */
    .pill-wall {
      display: flex;
      flex-wrap: wrap;
      gap: 10px 10px;
      align-items: center;
      margin-top: 6px;
    }
    .pill {
      display: inline-flex;
      align-items: center;
      padding: 6px 12px;
      border-radius: 999px;
      background: var(--pill-bg);
      color: var(--pill-txt);
      border: 1px solid var(--pill-brd);
      font-family: 'Inter', sans-serif;
      font-size: 14px;
      line-height: 1;
      text-decoration: none;
      transition: transform .15s ease, background .15s ease, border-color .15s ease;
      outline: none;
    }
    .pill:hover { background: var(--pill-hover); border-color: var(--brand-gold); transform: translateY(-1px); }
    .pill:focus-visible { box-shadow: 0 0 0 3px rgba(255,215,0,0.35); }

    .cap { color: #CFE2FF; font-size: 12px; margin-top: -10px; }
    </style>
""", unsafe_allow_html=True)

# --------------------------
#     LOTTIE LOADER (resilient)
# --------------------------
def _fix_json_extension(p: str) -> List[str]:
    candidates: List[str] = []
    low = p.lower()
    if low.endswith(".json.json"):
        candidates.append(p)
        candidates.append(p[:-5])   # drop one ".json"
    elif low.endswith(".json"):
        candidates.append(p)
        candidates.append(p + ".json")
    else:
        candidates.append(p + ".json")
        candidates.append(p + ".json.json")
    return candidates

def _normalize_abs(p: str) -> str:
    if not p:
        return p
    p = p.strip().strip('"').strip("'")
    p = os.path.expanduser(p)
    if p.startswith("Users/"):
        p = "/" + p
    return os.path.abspath(p) if not os.path.isabs(p) else p

def _load_lottie_candidates(cands: List[str]) -> Tuple[Optional[Any], Optional[str]]:
    for path in cands:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f), path
        except Exception:
            continue
    return None, None

def load_lottie_prefer_local(name_or_abs_path: str) -> Tuple[Optional[Any], Optional[str]]:
    if name_or_abs_path:
        abs_norm = _normalize_abs(name_or_abs_path)
        data, used = _load_lottie_candidates(_fix_json_extension(abs_norm))
        if data is not None:
            return data, used
    here = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(here)
    search_bases = [
        os.path.join(here, name_or_abs_path),
        os.path.join(project_root, name_or_abs_path),
        os.path.join(here, "assets", name_or_abs_path),
        os.path.join(project_root, "assets", name_or_abs_path),
    ]
    candidates: List[str] = []
    for base in search_bases:
        candidates.extend(_fix_json_extension(base))
    return _load_lottie_candidates(candidates)

# Try to load a tennis-themed Lottie (adjust path name if needed)
lottie_data, lottie_used = load_lottie_prefer_local("Tennis Ball")

# --------------------------
#     HEADER / HERO
# --------------------------
left, right = st.columns([3, 1])
with left:
    st.markdown("<h1 class='hero-title'>Marcos Ondruska</h1>", unsafe_allow_html=True)
    st.markdown(
        "<div class='hero-sub'>Ex-ATP #27 • Olympian (Atlanta 1996) • Former South Africa Davis Cup Captain • "
        "GPTCA A* Certified Coach • Software Developer (ML/Trading)</div>",
        unsafe_allow_html=True
    )
    btn_cols = st.columns([1,1,1,1])
    with btn_cols[0]:
        st.link_button("🔗 LinkedIn", LINKEDIN_URL, use_container_width=True)
    with btn_cols[1]:
        st.link_button("💻 GitHub", GITHUB_URL or "https://github.com/", use_container_width=True)
    with btn_cols[2]:
        st.link_button("𝕏 Profile", X_URL or "https://x.com/", use_container_width=True)
    with btn_cols[3]:
        st.link_button("✉️ Email", f"mailto:{EMAIL}", use_container_width=True)

with right:
    if lottie_data:
        st_lottie(lottie_data, height=200, key="hero_anim")
        if lottie_used:
            st.caption(f"<span class='cap'>Animation: {os.path.basename(lottie_used)}</span>", unsafe_allow_html=True)

# --------------------------
#     ABOUT ME (smaller header + tighter spacing)
# --------------------------
st.markdown("<div class='section-header about'>About Me</div>", unsafe_allow_html=True)
st.markdown("""
<div class="card about-card">
  <p class="muted">I’m a developer with a unique path: from competing as a professional athlete to building software that powers real-world decisions. Today, I focus on creating intelligent, data-driven applications — from algorithmic trading systems to interactive AI tools.</p>
  <p class="muted">My technical toolkit spans Python, Java, JavaScript, C, F#, and Prolog, with experience across both enterprise frameworks (Spring Boot) and modern full-stack stacks (Node.js, React, MongoDB). I’m fluent in PostgreSQL and MongoDB, and enjoy working at the intersection of quantitative finance, AI/ML, and software engineering.</p>
  <p class="muted">Beyond code, I bring a global perspective — fluent in English, Afrikaans, German, and Slovak — and thrive in environments where technology, strategy, and creativity converge.</p>
</div>
""", unsafe_allow_html=True)

# --------------------------
#     TENNIS COACHING
# --------------------------
st.markdown("<div class='section-header'>Tennis Coaching</div>", unsafe_allow_html=True)
st.markdown("""
<div class="card">
  <p class="muted">I bring over 30 years of professional tennis experience to the court — from competing at the highest level (Olympics, ATP Tour, Davis Cup) to coaching players at all levels. My focus is on player development, mindset, and performance strategies that translate into real results.</p>
  <ul class="muted" style="margin-bottom: 0;">
    <li><b>Private Lessons</b> — 1-on-1 coaching tailored to your game</li>
    <li><b>Group Clinics & Camps</b> — competitive learning environments</li>
    <li><b>Performance Consulting</b> — match strategy, mental prep, and video analysis</li>
    <li><b>Junior Development</b> — long-term growth plans for young athletes</li>
  </ul>
</div>
""", unsafe_allow_html=True)

tc_cols = st.columns([1,1,1])
with tc_cols[0]:
    st.link_button("Request a Session", f"mailto:{EMAIL}?subject=Tennis%20Coaching%20Inquiry", use_container_width=True)
with tc_cols[1]:
    st.link_button("View LinkedIn", LINKEDIN_URL, use_container_width=True)
with tc_cols[2]:
    st.link_button("Contact by Email", f"mailto:{EMAIL}", use_container_width=True)

# --------------------------
#     SOFTWARE & DATA PROJECTS
# --------------------------
st.markdown("<div class='section-header'>Software & Data Projects</div>", unsafe_allow_html=True)

with st.expander("📈 Intraday Trading Engine (IB + Python)", expanded=True):
    st.markdown("""
Automated equity strategy using Interactive Brokers (ib_insync), ATR initial stops, EMA trailing stops, Telegram alerts, and PostgreSQL logging. Includes RVOL scanner, premarket breakout logic, and daily diagnostics.
""")

with st.expander("🧭 Market Breadth Dashboard"):
    st.markdown("""
Real-time advances/declines, highs/lows, and up/down volume for macro trading signals, with fallbacks and caching to handle broker data gaps.
""")

with st.expander("🎥 Tennis Video Analytics (YOLOv11x, Homography, Flask)"):
    st.markdown("""
Ball & player tracking, court calibration/homography, rally segmentation, bounce detection, and heatmaps with video overlay.
""")

with st.expander("🎾 Round Robin Tournament App (Streamlit)"):
    st.markdown("""
Generate balanced round-robin schedules for 2–20 players with multiple scoring formats, live standings, and results entry. Designed with an auto-sizing UI container for a clean embed.
""")
    st.link_button("Open App", ROUND_ROBIN_APP, use_container_width=False)

# --------------------------
#     SKILLS — TAG CLOUD / BADGE WALL
# --------------------------
st.markdown("<div class='section-header'>Skills</div>", unsafe_allow_html=True)

SKILLS: List[str] = [
    # Core programming
    "Python", "Java", "JavaScript", "C", "F#", "Prolog",
    # Frameworks & tools
    "Spring Boot", "Node.js", "Express", "React", "Docker", "JUnit", "GitHub",
    # Databases
    "PostgreSQL", "MongoDB", "SQL",
    # Web & CS
    "REST APIs", "OOP", "Data Structures & Algorithms", "Systems Programming", "Networking", "Linux",
    # Specializations
    "Algorithmic Trading", "Quantitative Investing", "AI/ML", "Capital Markets",
    # Practices
    "Unit Testing", "Version Control", "Scrum",
    # Leadership & Languages
    "Team Leadership", "Coaching/Mentorship", "English", "Afrikaans", "German", "Slovak",
]

pills_html = "<div class='card'><div class='pill-wall'>" + "".join(
    f"<span class='pill' tabindex='0'>{html.escape(s)}</span>" for s in SKILLS
) + "</div></div>"
st.markdown(pills_html, unsafe_allow_html=True)

# --------------------------
#     CONNECT
# --------------------------
st.markdown("<div class='section-header'>Connect</div>", unsafe_allow_html=True)
lc1, lc2, lc3, lc4 = st.columns(4)
with lc1:
    st.markdown(f"[LinkedIn]({LINKEDIN_URL})")
with lc2:
    st.markdown(f"[GitHub]({GITHUB_URL or 'https://github.com/'})")
with lc3:
    st.markdown(f"[X (Twitter)]({X_URL or 'https://x.com/'})")
with lc4:
    st.markdown(f"[Email](mailto:{EMAIL})")

# --------------------------
#     FOOTER
# --------------------------
st.markdown("<p style='text-align:center; color:#D0DAFF;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
