#!/usr/bin/env python3
import streamlit as st
import json
import os
from typing import List, Optional, Tuple, Any
from streamlit_lottie import st_lottie

# --------------------------
#     PAGE CONFIG
# --------------------------
st.set_page_config(page_title="Marcos Ondruska — Portfolio", page_icon="🎾", layout="wide")

# --------------------------
#     CONFIGURE YOUR LINKS
# --------------------------
LINKEDIN_URL = "https://www.linkedin.com/in/marcos-ondruska-3b3a749/"
GITHUB_URL   = "https://github.com/"            # <- put your GitHub username here
X_URL        = "https://x.com/"                 # <- put your X/Twitter handle here
EMAIL        = ""                               # <- optional, e.g. "hello@marcosondruska.com"

# Optional: Quick links to live apps
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
    }
    .stApp { background: linear-gradient(135deg, var(--brand-bg1), var(--brand-bg2)); color: white; }

    /* Headings */
    h1,h2,h3,.section-header {
      font-family: 'Orbitron', sans-serif;
      letter-spacing: .5px;
      text-shadow: 0 4px 18px rgba(0,0,0,.35);
    }
    .hero-title { color: var(--brand-gold); font-size: 40px; margin: 0 0 6px 0; }
    .hero-sub   { color: #E6F0FF; font-family: 'Inter', sans-serif; font-size: 18px; margin-bottom: 16px; }

    /* Buttons/links */
    a, .stButton>button {
      transition: all .2s ease;
    }
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

    /* Cards */
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

    .stExpander { transition: transform .2s ease; }
    .stExpander:hover { transform: translateY(-2px); }

    /* Tighten default Streamlit paddings a bit */
    .block-container { padding-top: 1rem; padding-bottom: 2rem; }
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
    # If absolute/relative path provided, try variants
    if name_or_abs_path:
        abs_norm = _normalize_abs(name_or_abs_path)
        data, used = _load_lottie_candidates(_fix_json_extension(abs_norm))
        if data is not None:
            return data, used

    # Otherwise, try local filenames near app root
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

# --------------------------
#     HEADER / HERO
# --------------------------
# Try to load a tennis-themed Lottie (adjust path if needed)
lottie_data, lottie_used = load_lottie_prefer_local("Tennis Ball")

left, right = st.columns([3, 1])
with left:
    st.markdown("<h1 class='hero-title'>Marcos Ondruska</h1>", unsafe_allow_html=True)
    st.markdown(
        "<div class='hero-sub'>Ex-ATP #27 • Olympian (Atlanta 1996) • Former South Africa Davis Cup Captain • "
        "GPTCA A* Certified Coach • Software Developer (CS, ML/AI & Trading Systems)</div>",
        unsafe_allow_html=True
    )
    # Quick action buttons
    btn_cols = st.columns([1,1,1,1])
    with btn_cols[0]:
        st.link_button("🔗 LinkedIn", LINKEDIN_URL, use_container_width=True)
    with btn_cols[1]:
        st.link_button("🎾 Round Robin App", ROUND_ROBIN_APP, use_container_width=True)
    with btn_cols[2]:
        st.link_button("💻 GitHub", GITHUB_URL or "https://github.com/", use_container_width=True)
    with btn_cols[3]:
        st.link_button("𝕏 Profile", X_URL or "https://x.com/", use_container_width=True)

with right:
    if lottie_data:
        st_lottie(lottie_data, height=200, key="hero_anim")
        if lottie_used:
            st.caption(f"Animation: `{os.path.basename(lottie_used)}`")

# --------------------------
#     SNAPSHOT / ABOUT
# --------------------------
st.markdown("<div class='section-header'>Snapshot</div>", unsafe_allow_html=True)
st.markdown("""
<div class="card">
<ul class="muted">
  <li><b>ATP Career-High Singles:</b> #27 • <b>Miami Open</b> semifinalist</li>
  <li><b>Olympian (1996, Atlanta):</b> defeated Goran Ivanišević</li>
  <li><b>Davis Cup Captain (South Africa):</b> led promotion from Euro/Africa Group 4 → Group 1</li>
  <li><b>GPTCA A* Certified Coach:</b> ATP-certified professional coaching designation</li>
  <li><b>Coached:</b> Vincent Spadea (former ATP #40), supported Jennifer Capriati during 2004 US Open SF run</li>
  <li><b>Software & Data:</b> Python, Streamlit, ib_insync, yfinance, ML/AI (RL/Transformers), PostgreSQL</li>
  <li><b>Current Focus:</b> Building trading systems, computer vision for tennis analytics, and web apps</li>
</ul>
</div>
""", unsafe_allow_html=True)

# --------------------------
#     FEATURED PROJECTS
# --------------------------
st.markdown("<div class='section-header'>Featured Projects</div>", unsafe_allow_html=True)

# Project 1: Round Robin App
with st.expander("🎾 Round Robin Tennis Scheduler (Streamlit)", expanded=True):
    st.markdown("""
- Create round-robin schedules for 2–20 players
- Dynamic UI with auto-sizing "card" container and robust button handling
- Points/Games/Best-of formats, standings, and results entry
""")
    st.link_button("Open App", ROUND_ROBIN_APP, use_container_width=False)

# Project 2: Trading Systems
with st.expander("📈 Intraday Trading System (IB + Python)"):
    st.markdown("""
- ib_insync live trading scripts: ATR initial stops, EMA trailing stops, Telegram alerts
- RVOL scanner, premarket breakout logic, and account/risk controls
- Postgres PnL tracking, daily diagnostics, and robust error handling
""")
    if GITHUB_URL:
        st.markdown(f"[View GitHub]({GITHUB_URL})")

# Project 3: Tennis Video Analytics
with st.expander("🎥 Tennis Analytics (YOLOv11x, Homography, Flask)"):
    st.markdown("""
- Ball & player tracking, court calibration/homography
- Rally segmentation and bounce detection visualization
- Multithreaded processing, PostgreSQL storage, and heatmaps
""")

# Project 4: ML/LLM Learning & Tools
with st.expander("🧠 ML/LLM Learning & Tools"):
    st.markdown("""
- Deep learning coursework (Fall 2025) with a focus on Transformers and explainability (SHAP)
- Building tokenizers and experimenting with small LLMs locally (Apple M3)
""")

# --------------------------
#     EXPERIENCE HIGHLIGHTS
# --------------------------
st.markdown("<div class='section-header'>Experience Highlights</div>", unsafe_allow_html=True)
st.markdown("""
<div class="card">
<b>Tennis Professional & Coach</b><br/>
GPTCA A* Certified • Ex-ATP Top 30 • Olympian • Davis Cup Captain<br/>
<i>Player Development · High-Performance Coaching · Program Leadership</i>
</div>
<div class="card">
<b>Software Developer (Python)</b><br/>
Algorithmic Trading · Data Engineering · Web Apps (Streamlit) · Computer Vision (YOLO)<br/>
<i>ib_insync · yfinance · PostgreSQL · Flask · RL/Transformers · Visualization</i>
</div>
""", unsafe_allow_html=True)

# --------------------------
#     LINKS
# --------------------------
st.markdown("<div class='section-header'>Connect</div>", unsafe_allow_html=True)
lc1, lc2, lc3 = st.columns(3)
with lc1:
    st.markdown(f"[LinkedIn]({LINKEDIN_URL})")
with lc2:
    st.markdown(f"[GitHub]({GITHUB_URL or 'https://github.com/'})")
with lc3:
    st.markdown(f"[X (Twitter)]({X_URL or 'https://x.com/'})")

if EMAIL:
    st.markdown(f"<p class='muted'>Email: <a href='mailto:{EMAIL}'>{EMAIL}</a></p>", unsafe_allow_html=True)

# --------------------------
#     FOOTER
# --------------------------
st.markdown("<p style='text-align:center; color:#D0DAFF;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
