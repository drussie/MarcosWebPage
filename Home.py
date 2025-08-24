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
GITHUB_URL   = "https://github.com/drussie"
X_URL        = "https://x.com/drussie"
EMAIL        = "marcosondruska@gmail.com"
ROUND_ROBIN_APP = "https://marcoswebpage-k3rbpwxme7nzgk5rwdee3c.streamlit.app/"

# --------------------------
#     GLOBAL STYLES (Dark‑Neon baseline)
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

    a { color: var(--brand-mint) !important; text-decoration: none; }
    a:hover { color: var(--brand-gold) !important; text-decoration: underline; }

    /* Uniform dark pill buttons */
    .btn-like {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 10px 16px;
      width: 100%;
      border-radius: 14px;
      background: rgba(0,0,0,0.55);
      color: var(--brand-mint) !important;
      border: 1px solid rgba(255,255,255,0.18);
      box-shadow: 0 8px 24px rgba(0,0,0,.20);
      transition: transform .15s ease, border-color .15s ease, color .15s ease;
      text-decoration: none !important;
      font-weight: 600;
    }
    .btn-like:hover { transform: translateY(-1px); border-color: var(--brand-gold); color: var(--brand-gold) !important; }

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

    /* About Me tweaks */
    .section-header.about { font-size: 20px; margin: 4px 0 6px; }
    .about-card { padding: 14px 16px; }
    .about-card p { margin: 0 0 8px; line-height: 1.35; }

    .stExpander { transition: transform .2s ease; }
    .stExpander:hover { transform: translateY(-2px); }

    /* Badges */
    .pill-wall { display: flex; flex-wrap: wrap; gap: 10px 10px; align-items: center; margin-top: 6px; }
    .pill {
      display: inline-flex; align-items: center; padding: 6px 12px; border-radius: 999px;
      background: var(--pill-bg); color: var(--pill-txt); border: 1px solid var(--pill-brd);
      font-family: 'Inter', sans-serif; font-size: 14px; line-height: 1; text-decoration: none;
      transition: transform .15s ease, background .15s ease, border-color .15s ease; outline: none;
    }
    .pill:hover { background: var(--pill-hover); border-color: var(--brand-gold); transform: translateY(-1px); }
    .pill:focus-visible { box-shadow: 0 0 0 3px rgba(255,215,0,0.35); }

    .cap { color: #CFE2FF; font-size: 12px; margin-top: -10px; }

    /* Split columns highlight box */
    .metric {
      border-radius: 14px;
      background: rgba(0,0,0,.45);
      border: 1px solid rgba(255,255,255,.18);
      padding: 12px 14px;
      text-align: center;
    }

    /* Neon gradient frame (for Dark‑Neon style) */
    .neon-frame {
      border-radius: 20px;
      padding: 2px;
      background: linear-gradient(90deg, #f0f, #6f6fff, #00e5ff);
    }
    .neon-inner {
      border-radius: 18px;
      background: rgba(10, 10, 15, 0.85);
      border: 1px solid rgba(255,255,255,0.08);
      padding: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------
#     LOTTIE LOADER (resilient)
# --------------------------
def _fix_json_extension(p: str) -> List[str]:
    candidates: List[str] = []
    low = p.lower()
    if low.endswith(".json.json"):
        candidates.append(p); candidates.append(p[:-5])
    elif low.endswith(".json"):
        candidates.append(p); candidates.append(p + ".json")
    else:
        candidates.append(p + ".json"); candidates.append(p + ".json.json")
    return candidates

def _normalize_abs(p: str) -> str:
    if not p: return p
    p = p.strip().strip('"').strip("'")
    p = os.path.expanduser(p)
    if p.startswith("Users/"): p = "/" + p
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
        if data is not None: return data, used
    here = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(here)
    search_bases = [
        os.path.join(here, name_or_abs_path),
        os.path.join(project_root, name_or_abs_path),
        os.path.join(here, "assets", name_or_abs_path),
        os.path.join(project_root, "assets", name_or_abs_path),
    ]
    candidates: List[str] = []
    for base in search_bases: candidates.extend(_fix_json_extension(base))
    return _load_lottie_candidates(candidates)

lottie_data, lottie_used = load_lottie_prefer_local("Tennis Ball")

# --------------------------
#     HELPERS
# --------------------------
def link_button_like(label: str, url: str):
    st.markdown(
        f"<a class='btn-like' href='{html.escape(url)}' rel='noopener'>{html.escape(label)}</a>",
        unsafe_allow_html=True
    )

def pills_wall(items):
    html_pills = "<div class='card'><div class='pill-wall'>" + "".join(
        f"<span class='pill' tabindex='0'>{html.escape(s)}</span>" for s in items
    ) + "</div></div>"
    st.markdown(html_pills, unsafe_allow_html=True)

# --------------------------
#     CONTENT DATA
# --------------------------
SKILLS: List[str] = [
    "Python", "Java", "JavaScript", "C", "F#", "Prolog",
    "Spring Boot", "Node.js", "Express", "React", "Docker", "JUnit", "GitHub",
    "PostgreSQL", "MongoDB", "SQL",
    "REST APIs", "OOP", "Data Structures & Algorithms", "Systems Programming", "Networking", "Linux",
    "Algorithmic Trading", "Quantitative Investing", "AI/ML", "Capital Markets",
    "Unit Testing", "Version Control", "Scrum",
    "Team Leadership", "Coaching/Mentorship", "English", "Afrikaans", "German", "Slovak",
]

# --------------------------
#     STYLE SWITCHER (sidebar)
# --------------------------
with st.sidebar:
    st.markdown("### Style")
    style = st.radio(
        "Choose a layout",
        options=["Split‑Screen", "Minimal Hero", "Card Grid", "Dark‑Neon"],
        index=0,
        horizontal=False
    )
    st.markdown("---")
    st.markdown("### Quick Links")
    link_button_like("🔗 LinkedIn", LINKEDIN_URL)
    link_button_like("💻 GitHub", GITHUB_URL or "https://github.com/")
    link_button_like("𝕏 Profile", X_URL or "https://x.com/")
    st.markdown("---")
    st.caption("Swap styles to compare layouts. All content stays the same, only the presentation changes.")

# --------------------------
#     RENDERERS (4 styles)
# --------------------------
def render_split_screen():
    left, right = st.columns([1.2, 1])
    with left:
        st.markdown("<h1 class='hero-title'>Marcos Ondruska</h1>", unsafe_allow_html=True)
        st.markdown(
            "<div class='hero-sub'>Ex-ATP #27 • Olympian (Atlanta 1996) • Former South Africa Davis Cup Captain • "
            "GPTCA A*, USTA High Performance Certified Coach • Software Developer (ML/Trading, Spring Boot, MERN)</div>",
            unsafe_allow_html=True
        )
        btn_cols = st.columns([1,1,1])
        with btn_cols[0]:
            link_button_like("🔗 LinkedIn", LINKEDIN_URL)
        with btn_cols[1]:
            link_button_like("💻 GitHub", GITHUB_URL or "https://github.com/")
        with btn_cols[2]:
            link_button_like("𝕏 Profile", X_URL or "https://x.com/")

        # Metrics row
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown("<div class='metric'><div style='font-size:28px;font-weight:700;'>15+</div><div class='muted' style='font-size:12px;'>Apps & Tools</div></div>", unsafe_allow_html=True)
        with m2:
            st.markdown("<div class='metric'><div style='font-size:28px;font-weight:700;'>ATP A*</div><div class='muted' style='font-size:12px;'>GPTCA Certified</div></div>", unsafe_allow_html=True)
        with m3:
            st.markdown("<div class='metric'><div style='font-size:28px;font-weight:700;'>RL/ML</div><div class='muted' style='font-size:12px;'>Trading + Sports</div></div>", unsafe_allow_html=True)

    with right:
        if lottie_data:
            st_lottie(lottie_data, height=240, key="hero_anim_split")
            if lottie_used:
                st.caption(f"<span class='cap'>Animation: {os.path.basename(lottie_used)}</span>", unsafe_allow_html=True)
        st.markdown("<div class='section-header about'>About Me</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card about-card">
          <p class="muted">I’m a developer with a unique path: from competing as a professional athlete to building software that powers real-world decisions. Today, I focus on creating intelligent, data-driven applications — from algorithmic trading systems to interactive AI tools.</p>
          <p class="muted">My technical toolkit spans Python, Java, JavaScript, C, F#, and Prolog, with experience across both enterprise frameworks (Spring Boot) and modern full-stack stacks (Node.js, React, MongoDB). I’m fluent in PostgreSQL and MongoDB, and enjoy working at the intersection of quantitative finance, AI/ML, and software engineering.</p>
          <p class="muted">Beyond code, I bring a global perspective — fluent in English, Afrikaans, German, and Slovak — and thrive in environments where technology, strategy, and creativity converge.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Software & Data Projects</div>", unsafe_allow_html=True)
    with st.expander("📈 Intraday Trading Engine (IB + Python)"):
        st.markdown("Automated equity strategy using Interactive Brokers (ib_insync), ATR initial stops, EMA trailing stops, Telegram alerts, and PostgreSQL logging. Includes RVOL scanner, premarket breakout logic, and daily diagnostics.")
    with st.expander("🧭 Market Breadth Dashboard"):
        st.markdown("Real-time advances/declines, highs/lows, and up/down volume for macro trading signals, with fallbacks and caching to handle broker data gaps.")
    with st.expander("🎥 Tennis Video Analytics (YOLOv11x, Homography, Flask)"):
        st.markdown("Ball & player tracking, court calibration/homography, rally segmentation, bounce detection, and heatmaps with video overlay.")
    with st.expander("🎾 Round Robin Tournament App (Streamlit)"):
        st.markdown("Generate balanced round-robin schedules for 2–20 players with multiple scoring formats, live standings, and results entry. Designed with an auto-sizing UI container for a clean embed.")
        st.markdown(f"<a class='btn-like' href='{ROUND_ROBIN_APP}'>Open App</a>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Skills</div>", unsafe_allow_html=True)
    pills_wall(SKILLS)

    st.markdown("<div class='section-header'>Connect</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card">
      <p style="margin:0 0 6px;"><b>LinkedIn:</b> <a href="{LINKEDIN_URL}">{LINKEDIN_URL}</a></p>
      <p style="margin:0 0 6px;"><b>GitHub:</b> <a href="{GITHUB_URL}">{GITHUB_URL}</a></p>
      <p style="margin:0 0 6px;"><b>X:</b> <a href="{X_URL}">{X_URL}</a></p>
      <p style="margin:0;"><b>Email:</b> {html.escape(EMAIL)}</p>
    </div>
    """, unsafe_allow_html=True)

def render_minimal():
    st.markdown("<p class='muted' style='text-transform:uppercase;letter-spacing:.15em;'>Hello, I’m Marcos</p>", unsafe_allow_html=True)
    st.markdown("<h1 class='hero-title' style='font-size:52px;'>Tennis Professional & Software Developer</h1>", unsafe_allow_html=True)
    st.markdown("<p class='muted' style='max-width:780px;'>I help people and products perform at elite levels. Currently building AI‑powered trading systems and tennis analytics tools.</p>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        link_button_like("See Portfolio", GITHUB_URL or "#")
    with c2:
        link_button_like("Résumé", LINKEDIN_URL)
    with c3:
        link_button_like("Email", f"mailto:{EMAIL}")

    # 3 glass cards
    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown("<div class='card'><div class='muted' style='font-size:12px;'>Current Focus</div><div style='font-weight:600;'>Transformer forecasting · RL for trading · Tennis vision</div></div>", unsafe_allow_html=True)
    with g2:
        st.markdown("<div class='card'><div class='muted' style='font-size:12px;'>Recent</div><div style='font-weight:600;'>GPTCA A* Certification · Mortgage/Car calc mini‑apps</div></div>", unsafe_allow_html=True)
    with g3:
        st.markdown(f"<div class='card'><div class='muted' style='font-size:12px;'>Links</div><div style='font-weight:600;'><a href='{GITHUB_URL}'>GitHub</a> · <a href='{LINKEDIN_URL}'>LinkedIn</a> · <a href='{X_URL}'>X</a></div></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Skills</div>", unsafe_allow_html=True)
    pills_wall(SKILLS)

def render_card_grid():
    st.markdown("<h2 class='section-header'>Projects</h2>", unsafe_allow_html=True)

    # Six cards (2x3 grid)
    rows = [
        {
            "title": "Multi‑Agent Trading System",
            "desc": "RL + Transformers for intraday signals, with IB integration and risk controls.",
            "tags": ["Python","RL","IB"]
        },
        {
            "title": "Tennis Analytics Dashboard",
            "desc": "YOLO‑based ball tracking, bounce maps, rally metrics, and visual reports.",
            "tags": ["Computer Vision","Flask","OpenCV"]
        },
        {
            "title": "Mini‑Apps Hub",
            "desc": "Mortgage & car loan calculators, round‑robin generator, and more.",
            "tags": ["HTML","Tailwind","PWA"]
        },
        {
            "title": "High‑Performance Coaching",
            "desc": "ATP‑level insights for juniors and adults — technique, tactics, mindset.",
            "tags": ["GPTCA A*","Programs"]
        },
        {
            "title": "AI Research Notes",
            "desc": "Transformer explainability, SHAP, and hierarchical reasoning experiments.",
            "tags": ["Transformers","Explainability"]
        },
        {
            "title": "Writing",
            "desc": "Short posts on trading psychology, developer ergonomics, and practice.",
            "tags": ["Essays","Notes"]
        }
    ]

    # render 3 columns
    for i in range(0, len(rows), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j >= len(rows):
                continue
            item = rows[i+j]
            with col:
                tag_html = " ".join([f"<span class='pill' style='font-size:12px'>{html.escape(t)}</span>" for t in item["tags"]])
                col.markdown(
                    f"<div class='card'>"
                    f"<div style='font-weight:700;font-size:18px;'>{html.escape(item['title'])}</div>"
                    f"<div class='muted' style='font-size:14px;margin:.35rem 0 .5rem'>{html.escape(item['desc'])}</div>"
                    f"<div class='pill-wall'>{tag_html}</div>"
                    f"</div>", unsafe_allow_html=True
                )

def render_dark_neon():
    st.markdown(
        "<div class='neon-frame'><div class='neon-inner'>"
        "<h1 style='font-size:44px;margin:0 0 8px 0;'>"
        "<span style='background: linear-gradient(90deg,#f0f,#7a7aff,#00e5ff); -webkit-background-clip:text; background-clip:text; color:transparent;'>Marcos</span> builds smart systems"
        "</h1>"
        "<p class='muted'>Neon‑accent dark mode with bold type and micro‑interactions. Great for a memorable vibe.</p>"
        "</div></div>",
        unsafe_allow_html=True
    )

    c1, c2 = st.columns([1,1])
    with c1:
        if lottie_data:
            st_lottie(lottie_data, height=240, key="hero_anim_neon")
            if lottie_used:
                st.caption(f"<span class='cap'>Animation: {os.path.basename(lottie_used)}</span>", unsafe_allow_html=True)
        st.markdown("<div class='card'><div class='section-header about'>About Me</div>", unsafe_allow_html=True)
        st.markdown(
            "<p class='muted'>From ATP courts to production code. I design intelligent systems (finance, sports analytics) and make complex things feel simple.</p>",
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='card'><b>Live widget</b><br><span class='muted'>Mini Demo Panel</span><div style='height:8px'></div>", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1: link_button_like("Run", "#")
        with b2: link_button_like("Inspect", "#")
        st.markdown("</div>", unsafe_allow_html=True)

    # Feature bullets
    f1, f2, f3 = st.columns(3)
    f1.markdown("<div class='card'><div style='font-weight:600'>Realtime</div><div class='muted'>Streaming IB / telemetry</div></div>", unsafe_allow_html=True)
    f2.markdown("<div class='card'><div style='font-weight:600'>Vision</div><div class='muted'>YOLOv11x tennis analytics</div></div>", unsafe_allow_html=True)
    f3.markdown("<div class='card'><div style='font-weight:600'>Explainable</div><div class='muted'>SHAP & dashboards</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Skills</div>", unsafe_allow_html=True)
    pills_wall(SKILLS)

# --------------------------
#     ROUTER
# --------------------------
if style == "Split‑Screen":
    render_split_screen()
elif style == "Minimal Hero":
    render_minimal()
elif style == "Card Grid":
    render_card_grid()
else:
    render_dark_neon()

# --------------------------
#     FOOTER
# --------------------------
st.markdown("<p style='text-align:center; color:#D0DAFF; margin-top:12px;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
