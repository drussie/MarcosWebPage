#!/usr/bin/env python3
import streamlit as st
import json
import os
from typing import List, Optional, Tuple, Any
from streamlit_lottie import st_lottie

# Optional auto-height helper (not required)
try:
    from streamlit_js_eval import get_page_info
    _HAS_JS_EVAL = True
except Exception:
    _HAS_JS_EVAL = False

# --------------------------
#     PAGE CONFIG
# --------------------------
st.set_page_config(page_title="Playground", page_icon="🛠️", layout="wide")

# --------------------------
#     STYLES
# --------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron&display=swap');
    .stApp {
        background: linear-gradient(to right, #0A2540, #1E90FF);
        color: white;
    }
    h1 {
        font-family: 'Orbitron', sans-serif;
        color: #FFD700;
    }
    a {
        color: #00FF7F;
        text-decoration: none;
        transition: color 0.3s;
    }
    a:hover {
        color: #FFD700;
        text-decoration: underline;
    }
    .app-link {
        display: inline-block;
        margin: 10px;
        padding: 10px 20px;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
        font-size: 1.2em;
    }
    .stExpander {
        transition: transform 0.3s;
    }
    .stExpander:hover {
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------
#     HELPERS
# --------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

def _fix_json_extension(p: str) -> List[str]:
    """Return candidate paths adjusting double/absent .json endings."""
    candidates: List[str] = []
    low = p.lower()
    if low.endswith(".json.json"):
        candidates.append(p)           # as-is
        candidates.append(p[:-5])      # strip one .json -> .json
    elif low.endswith(".json"):
        candidates.append(p)
        candidates.append(p + ".json") # try doubled, just in case
    else:
        candidates.append(p + ".json")
        candidates.append(p + ".json.json")
    return candidates

def _normalize_abs(p: str) -> str:
    """Normalize to absolute path, adding leading / if missing on macOS-like paths."""
    if not p:
        return p
    p = p.strip().strip('"').strip("'")
    p = os.path.expanduser(p)
    if p.startswith("Users/"):  # add leading slash if omitted
        p = "/" + p
    return os.path.abspath(p) if not os.path.isabs(p) else p

def load_lottie_from_candidates(candidates: List[str]) -> Tuple[Optional[Any], Optional[str]]:
    for path in candidates:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f), path
        except Exception:
            continue
    return None, None

def load_lottie(best_name_or_path: Optional[str], fallback_name: Optional[str] = None) -> Tuple[Optional[Any], Optional[str]]:
    """
    Tries, in order:
    1) Custom absolute path (with smart fixes).
    2) Local project candidates: <name>.json in SCRIPT_DIR, assets/, PROJECT_ROOT.
    """
    if best_name_or_path:
        cand = _normalize_abs(best_name_or_path)
        abs_candidates = _fix_json_extension(cand)
        data, used = load_lottie_from_candidates(abs_candidates)
        if data is not None:
            return data, used

    # Fall back to name-based search (Laptop / Tennis Ball)
    name = fallback_name or "Laptop"
    local_candidates: List[str] = []
    for base in (
        os.path.join(SCRIPT_DIR, f"{name}"),
        os.path.join(SCRIPT_DIR, "assets", f"{name}"),
        os.path.join(PROJECT_ROOT, f"{name}"),
        os.path.join(PROJECT_ROOT, "assets", f"{name}"),
    ):
        local_candidates += _fix_json_extension(base)

    data, used = load_lottie_from_candidates(local_candidates)
    return data, used

def _iframe_height(auto_margin: int = 120, fallback: int = 800) -> int:
    """
    Compute iframe height from browser viewport using streamlit-js-eval.
    Returns a sensible fallback if the module isn't available.
    """
    if not _HAS_JS_EVAL:
        return fallback
    try:
        page_info = get_page_info()  # {'innerHeight': ..., 'innerWidth': ...}
        viewport_h = int(page_info.get("innerHeight", fallback))
        return max(400, viewport_h - auto_margin)
    except Exception:
        return fallback

# --------------------------
#     SIDEBAR: CUSTOM LOTTIE PATH
# --------------------------
with st.sidebar:
    st.markdown("### Lottie Options")
    animation_choice = st.selectbox("Choose an animation", ["Laptop", "Tennis Ball"])
    custom_path = st.text_input(
        "Custom Lottie path (optional)",
        help="Paste an absolute path to a .json (handles missing leading '/' and double '.json.json')."
    )
    if _HAS_JS_EVAL and st.button("🔄 Resize to window"):
        try:
            st.rerun()
        except Exception:
            st.experimental_rerun()

# --------------------------
#     UI: EFFECTS
# --------------------------
effect = st.selectbox("Choose an effect", ["Balloons", "Snow"], key="effect_selector")
if effect == "Balloons":
    st.balloons()
else:
    st.snow()

# --------------------------
#     HEADER
# --------------------------
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h1>My App Playground 🛠️</h1>", unsafe_allow_html=True)
    st.write("Explore the apps I've built or am working on. Select an app to interact with it here!")
with col2:
    lottie_data, used_path = load_lottie(custom_path, animation_choice)
    if lottie_data:
        st_lottie(lottie_data, height=200, key="playground_anim")
        if custom_path:
            st.caption(f"Loaded Lottie from: `{used_path}`")
    else:
        st.markdown(
            "<p style='color: #FFD700;'>Animation unavailable — "
            "check the custom path or place JSON in /assets. 😎</p>",
            unsafe_allow_html=True
        )

# --------------------------
#     APPS
# --------------------------
st.markdown("### Available Apps")
apps = {
    "Round Robin Tennis": "apps/round_robin.html",  # relative to project root (one level up from pages/)
    "Mortgage Calculator": "apps/mortgage_calculator.html",
    "Car Loan Calculator": "apps/car_loan_calculator.html",
    "Tennis Score & Stats Tracker": "apps/tennis_tracker.html",
    "Asteroids": "apps/asteroids.html"
}
selected_app = st.selectbox("Select an app to run", list(apps.keys()))

# --------------------------
#     EMBEDDER: DYNAMIC WHITE BACKGROUND + CONFIRM BINDING
# --------------------------
if selected_app in apps:
    url_or_path = apps[selected_app]
    if url_or_path.startswith("http"):
        st.markdown(
            f'<a href="{url_or_path}" target="_blank" class="app-link">Launch {selected_app} in new tab</a>',
            unsafe_allow_html=True
        )
    else:
        app_path = os.path.join(PROJECT_ROOT, url_or_path)

        try:
            with open(app_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            # --- DYNAMIC WHITE CARD CONTAINER ---
            # Body becomes transparent; card (#rr-container) is white, auto-height, padded.
            injected_css = """
<style>
  /* Make page background transparent so extra iframe space isn't a big white box */
  html, body {
      background: transparent !important;
  }

  /* Our dynamic white card wrapper */
  #rr-container {
      background: #ffffff !important;
      color: #000;               /* ensure readability inside */
      display: inline-block;     /* shrink-wrap to content width */
      padding: 16px 18px;
      margin: 10px 12px;
      border-radius: 10px;
      box-shadow: 0 6px 20px rgba(0,0,0,0.10);
      max-width: 100%;
  }

  /* Keep original app pieces readable against white */
  .match, button, input, select, #initialSetup, #setup, #tournament, #final {
      background-color: transparent !important;  /* now inside white card */
  }
  button {
      display: inline-block !important;
      padding: 8px 14px; margin: 6px 6px 6px 0;
      background-color: #4CAF50 !important; color: white !important; border: none; border-radius: 4px;
      cursor: pointer;
  }
  button:hover { background-color: #45a049 !important; }
</style>
"""

            # JS: wrap all body content in #rr-container; keep your confirm binding logic
            injected_js = """
<script>
(function(){
  function log(){ try { console.log.apply(console, arguments); } catch(e){} }

  // Wrap everything in a white "card" that auto-sizes with content
  function wrapInCard(){
    if (document.getElementById('rr-container')) return;
    var card = document.createElement('div');
    card.id = 'rr-container';

    // Move all current body children into the card
    var currentScript = document.currentScript;
    var kids = Array.prototype.slice.call(document.body.childNodes);
    kids.forEach(function(node){
      if (node !== card && node !== currentScript) {
        card.appendChild(node);
      }
    });
    document.body.appendChild(card);
  }

  function ensureConfirmDefined(){
    if (typeof window.confirmPlayerCount === 'function') return true;
    window.confirmPlayerCount = function(){
      log('[Injected] confirmPlayerCount called');
      var numEl = document.getElementById('numPlayers');
      if(!numEl){ alert('numPlayers input not found'); return; }
      var num = parseInt(numEl.value);
      if (isNaN(num) || num < 2 || num > 20) {
        alert('Please enter a number of players between 2 and 20.');
        return;
      }
      var div = document.getElementById('playerNames');
      if(!div){ alert('playerNames container not found'); return; }
      div.innerHTML = '';
      for (var i=1;i<=num;i++){
        div.insertAdjacentHTML('beforeend',
          '<label>Player '+i+' Name:</label><input type="text" id="player'+i+'" placeholder="Player '+i+'"><br>');
      }
      var init = document.getElementById('initialSetup');
      var setup = document.getElementById('setup');
      if (init) init.style.display='none';
      if (setup) setup.style.display='block';
    };
    return true;
  }

  function bindConfirm(){
    var btn =
      document.querySelector('button[onclick*="confirmPlayerCount"]') ||
      document.getElementById('confirmBtn') ||
      Array.from(document.querySelectorAll('button'))
        .find(function(b){ return ((b.textContent || '').trim().toLowerCase() === 'confirm'); });

    if(!btn){ return false; }
    ensureConfirmDefined();
    btn.onclick = function(e){
      e.preventDefault();
      try {
        window.confirmPlayerCount();
      } catch(err){
        console.error('Error in confirmPlayerCount:', err);
        alert('Error: ' + (err && err.message ? err.message : err));
      }
    };
    log('[Injected] Confirm button bound');
    return true;
  }

  function tryBind(){
    wrapInCard();
    if (bindConfirm()) return;

    var mo = new MutationObserver(function(){
      wrapInCard();
      bindConfirm();
    });
    mo.observe(document.documentElement || document.body, {childList:true, subtree:true});

    [100, 300, 800, 1500].forEach(function(ms){ setTimeout(function(){
      wrapInCard();
      bindConfirm();
    }, ms); });
  }

  if (document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', tryBind);
  } else {
    tryBind();
  }
})();
</script>
"""

            # Insert before </body> if present (case-insensitive), else append
            lower = html_content.lower()
            if "</body>" in lower:
                idx = lower.rfind("</body>")
                modified_html = html_content[:idx] + injected_css + injected_js + html_content[idx:]
            else:
                modified_html = html_content + injected_css + injected_js

            # --- iframe height (tweak as you wish) ---
            iframe_height = _iframe_height(auto_margin=120, fallback=800)
            st.components.v1.html(modified_html, height=iframe_height, scrolling=True)

        except Exception as e:
            st.error(f"Failed to load {selected_app}: {e}")

# --------------------------
#     QUICK LINKS
# --------------------------
st.markdown("### Quick Links")
for app_name, url in apps.items():
    if url.startswith("http"):
        st.markdown(f'<a href="{url}" target="_blank" class="app-link">{app_name}</a>', unsafe_allow_html=True)
