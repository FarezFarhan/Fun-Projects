import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VolleyRank – Player Level Evaluator",
    page_icon="🏐",
    layout="centered",
)

# ── Grade / GPA system ───────────────────────────────────────────────────────
GRADE_POINTS = {
    "A":  4.0,
    "A-": 3.75,
    "B+": 3.5,
    "B":  3.0,
    "C+": 2.5,
    "C":  2.0,
    "D+": 1.5,
    "D":  1.0,
    "E":  0.5,
    "F":  0.0,
}

# ── Class tier system (12 tiers, GPA thresholds) ─────────────────────────────
#  Classes: Professional, Advanced, Intermediate, Beginner
#  Each has pre-X, X, X+  →  12 total
TIERS = [
    {"label": "Professional+",    "min": 4.15, "color": "#FFD700", "badge": "🏆"},
    {"label": "Professional",     "min": 3.85, "color": "#FFC200", "badge": "🥇"},
    {"label": "Pre-Professional", "min": 3.50, "color": "#E6A800", "badge": "⭐"},
    {"label": "Advanced+",        "min": 3.15, "color": "#1E90FF", "badge": "🔵"},
    {"label": "Advanced",         "min": 2.85, "color": "#1677CC", "badge": "💙"},
    {"label": "Pre-Advanced",     "min": 2.50, "color": "#0F5EA6", "badge": "🔷"},
    {"label": "Intermediate+",    "min": 2.15, "color": "#34C68A", "badge": "🟢"},
    {"label": "Intermediate",     "min": 1.85, "color": "#27A570", "badge": "💚"},
    {"label": "Pre-Intermediate", "min": 1.50, "color": "#1A8056", "badge": "🌿"},
    {"label": "Beginner+",        "min": 1.15, "color": "#FF6B35", "badge": "🟠"},
    {"label": "Beginner",         "min": 0.80, "color": "#CC4E1A", "badge": "🔸"},
    {"label": "Pre-Beginner",     "min": 0.00, "color": "#8B2500", "badge": "🔴"},
]

# ── Skill categories & their descriptions ────────────────────────────────────
SKILLS = {
    "Serving":    "Accuracy, power, and variety (float, jump, topspin).",
    "Passing":    "Ball control, platform stability, and first-touch accuracy.",
    "Setting":    "Hand technique, decision-making, and ball placement.",
    "Attacking":  "Approach footwork, arm swing, and shot selection.",
    "Blocking":   "Timing, positioning, and reading the setter.",
    "Defence":    "Court reading, digging technique, and agility.",
    "Game IQ":    "Tactical awareness, communication, and adaptability.",
    "Fitness":    "Stamina, explosiveness, and injury resilience.",
}

GRADES = list(GRADE_POINTS.keys())


def gpa_to_tier(gpa: float) -> dict:
    for tier in TIERS:
        if gpa >= tier["min"]:
            return tier
    return TIERS[-1]


def gpa_to_letter(gpa: float) -> str:
    """Return the closest grade letter for a GPA value."""
    closest = min(GRADE_POINTS, key=lambda g: abs(GRADE_POINTS[g] - gpa))
    return closest


# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;900&family=Inter:wght@400;500;600&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0D1B2A !important;
    color: #E8EDF2 !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; }

/* Hero */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    border-bottom: 1px solid #1E3450;
    margin-bottom: 2rem;
}
.hero-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 3.6rem;
    font-weight: 900;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    background: linear-gradient(135deg, #1E90FF 0%, #FFD700 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.05;
}
.hero-sub {
    font-size: 1rem;
    color: #8FA8C0;
    margin-top: 0.5rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* Section header */
.section-label {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #1E90FF;
    border-left: 3px solid #1E90FF;
    padding-left: 0.6rem;
    margin-bottom: 1rem;
    margin-top: 1.8rem;
}

/* Skill row card */
.skill-card {
    background: #132236;
    border: 1px solid #1E3450;
    border-radius: 10px;
    padding: 1rem 1.2rem 0.6rem;
    margin-bottom: 0.8rem;
}
.skill-name {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #C8D8E8;
}
.skill-desc {
    font-size: 0.78rem;
    color: #607080;
    margin-bottom: 0.5rem;
}

/* Result card */
.result-card {
    border-radius: 16px;
    padding: 2rem 2.5rem;
    text-align: center;
    margin-top: 2rem;
    border: 2px solid;
    position: relative;
    overflow: hidden;
}
.result-badge {
    font-size: 3.5rem;
    line-height: 1;
}
.result-tier {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.6rem;
    font-weight: 900;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-top: 0.2rem;
}
.result-gpa {
    font-size: 1rem;
    color: #8FA8C0;
    margin-top: 0.2rem;
}
.result-grade {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 4.5rem;
    font-weight: 900;
    opacity: 0.12;
    position: absolute;
    right: 1rem;
    top: 0.5rem;
    line-height: 1;
    pointer-events: none;
}

/* Skill breakdown table */
.breakdown-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
    font-size: 0.88rem;
}
.breakdown-table th {
    font-family: 'Barlow Condensed', sans-serif;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-size: 0.75rem;
    color: #4A6A88;
    border-bottom: 1px solid #1E3450;
    padding: 0.4rem 0.6rem;
    text-align: left;
}
.breakdown-table td {
    padding: 0.45rem 0.6rem;
    border-bottom: 1px solid #0F2438;
    color: #C0D0E0;
}
.grade-pill {
    display: inline-block;
    padding: 0.15rem 0.55rem;
    border-radius: 4px;
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 0.04em;
}

/* Court divider */
.court-line {
    border: none;
    border-top: 1px solid #1E3450;
    margin: 2rem 0;
    position: relative;
}

/* Tier reference table */
.tier-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.tier-table td { padding: 0.35rem 0.7rem; border-bottom: 1px solid #0F2438; }
.tier-dot {
    width: 10px; height: 10px; border-radius: 50%;
    display: inline-block; margin-right: 6px; vertical-align: middle;
}

/* Streamlit widget overrides */
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label { color: #8FA8C0 !important; font-size: 0.8rem; }
div[data-testid="stSelectbox"] > div > div {
    background: #0F2438 !important;
    border: 1px solid #1E3450 !important;
    color: #E8EDF2 !important;
}
.stButton > button {
    background: linear-gradient(135deg, #1E90FF, #0060CC) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.6rem 2rem !important;
    width: 100%;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.85 !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">🏐 SEE YOUR RANK 🏐</div>
  <div class="hero-sub">Evaluate your level based on your skills grade</div>
</div>
""", unsafe_allow_html=True)

# ── Player info ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Player Info</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    player_name = st.text_input("Player Name", placeholder="e.g. Alex Rivera")
with col2:
    position = st.selectbox("Primary Position", [
        "Libero", "Setter", "Outside Hitter", "Opposite Hitter",
        "Middle Blocker", "Defensive Specialist", "All-Around"
    ])

# ── Skill grades ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Rate Each Skill</div>', unsafe_allow_html=True)
st.markdown(
    '<p style="color:#607080;font-size:0.82rem;margin-bottom:1rem;">'
    'Assign a grade to each skill area. Grades follow a GPA-style scale (A+ = 4.3 … F = 0.0).</p>',
    unsafe_allow_html=True
)

selected_grades = {}
for skill, desc in SKILLS.items():
    st.markdown(f"""
    <div class="skill-card">
      <div class="skill-name">{skill}</div>
      <div class="skill-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)
    selected_grades[skill] = st.selectbox(
        f"Grade for {skill}",
        GRADES,
        index=4,          # default "B"
        key=f"grade_{skill}",
        label_visibility="collapsed",
    )

# ── Grade reference ───────────────────────────────────────────────────────────
with st.expander("📊 Grade Point Reference"):
    cols = st.columns(4)
    items = list(GRADE_POINTS.items())
    chunk = len(items) // 4 + 1
    for i, col in enumerate(cols):
        with col:
            for g, pts in items[i*chunk:(i+1)*chunk]:
                st.markdown(f"**{g}** — {pts:.1f}")

# ── Tier reference ────────────────────────────────────────────────────────────
with st.expander("🏅 Tier / Class Reference"):
    rows = ""
    for t in TIERS:
        rows += (
            f'<tr><td><span class="tier-dot" style="background:{t["color"]}"></span>'
            f'{t["badge"]} {t["label"]}</td>'
            f'<td style="color:#8FA8C0">≥ {t["min"]:.2f} GPA</td></tr>'
        )
    st.markdown(
        f'<table class="tier-table">'
        f'<thead><tr><th>Class</th><th>Min GPA</th></tr></thead>'
        f'<tbody>{rows}</tbody></table>',
        unsafe_allow_html=True,
    )

# ── Evaluate button ───────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
evaluate = st.button("⚡ Evaluate Player Level")

if evaluate:
    # Compute weighted GPA (all skills equal weight here)
    gpa_scores = {skill: GRADE_POINTS[grade] for skill, grade in selected_grades.items()}
    avg_gpa = sum(gpa_scores.values()) / len(gpa_scores)
    tier = gpa_to_tier(avg_gpa)
    overall_letter = gpa_to_letter(avg_gpa)

    name_display = player_name.strip() if player_name.strip() else "Player"

    # ── Result card ──────────────────────────────────────────────────────────
    st.markdown('<hr class="court-line">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="result-card" style="background: linear-gradient(135deg, #0D1B2A 60%, {tier['color']}22);
             border-color: {tier['color']};">
          <div class="result-grade">{overall_letter}</div>
          <div class="result-badge">{tier['badge']}</div>
          <div class="result-tier" style="color:{tier['color']}">{tier['label']}</div>
          <div style="color:#C8D8E8;font-size:1.1rem;margin-top:0.3rem;">{name_display}</div>
          <div class="result-gpa">Overall GPA: <strong>{avg_gpa:.2f}</strong> &nbsp;|&nbsp; Grade: <strong>{overall_letter}</strong> &nbsp;|&nbsp; Position: <strong>{position}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Skill breakdown ──────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Skill Breakdown</div>', unsafe_allow_html=True)

    def grade_color(g):
        gp = GRADE_POINTS[g]
        if gp >= 3.7:   return "#FFD700"
        elif gp >= 3.0: return "#1E90FF"
        elif gp >= 2.0: return "#34C68A"
        elif gp >= 1.0: return "#FF6B35"
        else:           return "#CC2222"

    rows_html = ""
    sorted_skills = sorted(gpa_scores.items(), key=lambda x: x[1], reverse=True)
    for skill, pts in sorted_skills:
        grade = selected_grades[skill]
        color = grade_color(grade)
        bar_width = int((pts / 4.3) * 100)
        rows_html += f"""
        <tr>
          <td><strong>{skill}</strong></td>
          <td><span class="grade-pill" style="background:{color}22;color:{color};border:1px solid {color}66">{grade}</span></td>
          <td style="color:#8FA8C0">{pts:.1f}</td>
          <td style="width:40%">
            <div style="background:#0F2438;border-radius:4px;height:8px;overflow:hidden;">
              <div style="background:{color};width:{bar_width}%;height:100%;border-radius:4px;
                   transition:width 0.5s ease;"></div>
            </div>
          </td>
        </tr>"""

    st.markdown(
        f"""<table class="breakdown-table">
          <thead><tr><th>Skill</th><th>Grade</th><th>Points</th><th>Bar</th></tr></thead>
          <tbody>{rows_html}</tbody>
        </table>""",
        unsafe_allow_html=True,
    )

    # ── Strengths / Weaknesses ───────────────────────────────────────────────
    st.markdown('<hr class="court-line">', unsafe_allow_html=True)
    top3 = sorted_skills[:3]
    bot3 = sorted_skills[-3:]

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**💪 Top Strengths**")
        for s, p in top3:
            g = selected_grades[s]
            st.markdown(f"- **{s}** — {g} ({p:.1f})")
    with c2:
        st.markdown("**📈 Areas to Improve**")
        for s, p in bot3:
            g = selected_grades[s]
            st.markdown(f"- **{s}** — {g} ({p:.1f})")

    # ── Next tier goal ────────────────────────────────────────────────────────
    current_idx = next(i for i, t in enumerate(TIERS) if t["label"] == tier["label"])
    if current_idx > 0:
        next_tier = TIERS[current_idx - 1]
        gap = next_tier["min"] - avg_gpa
        st.info(
            f"🎯 **Next goal: {next_tier['badge']} {next_tier['label']}** — "
            f"You need **+{gap:.2f} GPA** on average to reach the next tier."
        )
    else:
        st.success("🏆 **You're at the top tier! Professional+ is the peak of volleyball excellence.**")

    # ── Motivational tagline ─────────────────────────────────────────────────
    taglines = {
        "Professional+":    "Elite performer. Your court vision and execution are world-class.",
        "Professional":     "Top-tier player. Consistency and leadership set you apart.",
        "Pre-Professional": "Tournament-ready. One more push to join the elite.",
        "Advanced+":        "Highly competitive. Your skills shine under pressure.",
        "Advanced":         "Strong all-around player with a clear tactical game.",
        "Pre-Advanced":     "Solid fundamentals with advanced potential emerging.",
        "Intermediate+":    "Growing rapidly. Your effort is paying off.",
        "Intermediate":     "Steady foundation. Keep drilling the fundamentals.",
        "Pre-Intermediate": "Making real progress. Consistency is key.",
        "Beginner+":        "Learning fast. Focus on footwork and serve receive.",
        "Beginner":         "Early stages — every session builds the base.",
        "Pre-Beginner":     "Just starting out. Welcome to the game! 🏐",
    }
    st.markdown(
        f'<p style="text-align:center;color:#607080;font-size:0.9rem;margin-top:1.5rem;">'
        f'"{taglines.get(tier["label"], "")}"</p>',
        unsafe_allow_html=True,
    )