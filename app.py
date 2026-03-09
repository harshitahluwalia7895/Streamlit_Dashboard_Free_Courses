import streamlit as st
import json
from datetime import date

st.set_page_config(page_title="Course Promo Tracker", page_icon="📣", layout="wide")

# ── Data ──────────────────────────────────────────────────────────────────────
COURSES = [
    {"id": 3252657,  "name": "RIP Data Scientists"},
    {"id": 2908028,  "name": "GenAI Applied to Quantitative Finance: For Control Implementation"},
    {"id": 3017998,  "name": "OpenEngage: Build a complete AI Driven Marketing Engine"},
    {"id": 2993107,  "name": "End to end RAG Application development with Langchain and Streamlit"},
    {"id": 3302717,  "name": "Claude 4.5: Smarter, Faster & More Human AI"},
    {"id": 2933164,  "name": "Reimagining GenAI: Common Mistakes and Best Practices for Success"},
    {"id": 3291893,  "name": "Foundations of Vector Database"},
    {"id": 3307823,  "name": "Building AI agents with Amazon Bedrock AgentCore"},
    {"id": 3226993,  "name": "GenAI to Build Exciting Games"},
    {"id": 3317410,  "name": "Modeling Time-series Data with Deep Learning"},
    {"id": 2809503,  "name": "Data Preprocessing on a Real-World Problem Statement"},
    {"id": 3089573,  "name": "Exploring OpenAI o3 and o4-mini"},
    {"id": 3337167,  "name": "Getting Started With AWS For Data Science"},
    {"id": 3273365,  "name": "Gemini 3: The AI That Thinks, Sees and Creates"},
    {"id": 3240527,  "name": "Vibe Coding with Cursor"},
    {"id": 3202101,  "name": "Docker for Absolute Beginners"},
    {"id": 3086605,  "name": "Data Analysis with Apache Hive"},
    {"id": 1515017,  "name": "Introduction to Cloud"},
    {"id": 3371995,  "name": "Deploy ML Models Using AWS | AWS for Data Science Course"},
    {"id": 3366030,  "name": "AWS for Data Science: EC2 vs SageMaker vs Lambda"},
    {"id": 3360581,  "name": "AWS Storage & Querying for Data Science with S3 and Athena"},
    {"id": 3349361,  "name": "Foundations of LangGraph for Agentic AI Workflows"},
]

PLATFORMS = ["YouTube", "Instagram", "LinkedIn"]
PLATFORM_ICONS = {"YouTube": "▶", "Instagram": "◈", "LinkedIn": "in"}
PLATFORM_COLORS = {"YouTube": "#E53E3E", "Instagram": "#D53F8C", "LinkedIn": "#2B6CB0"}

# ── Session State ─────────────────────────────────────────────────────────────
if "promotions" not in st.session_state:
    # promotions: { course_id: { platform: { date, note } } }
    st.session_state.promotions = {}

if "log" not in st.session_state:
    st.session_state.log = []  # list of { course_name, platform, date, note }

def get_promos(course_id):
    return st.session_state.promotions.get(str(course_id), {})

def mark_promoted(course_id, course_name, platform, promo_date, note):
    cid = str(course_id)
    if cid not in st.session_state.promotions:
        st.session_state.promotions[cid] = {}
    st.session_state.promotions[cid][platform] = {"date": str(promo_date), "note": note}
    st.session_state.log.insert(0, {
        "course": course_name, "platform": platform,
        "date": str(promo_date), "note": note
    })

def remove_promo(course_id, platform):
    cid = str(course_id)
    if cid in st.session_state.promotions:
        st.session_state.promotions[cid].pop(platform, None)

# ── Stats ─────────────────────────────────────────────────────────────────────
def compute_stats():
    total = len(COURSES)
    done = sum(1 for c in COURSES if len(get_promos(c["id"])) >= 1)   # ≥1 platform = Done
    pending = sum(1 for c in COURSES if len(get_promos(c["id"])) == 0)
    yt = sum(1 for c in COURSES if "YouTube"  in get_promos(c["id"]))
    ig = sum(1 for c in COURSES if "Instagram" in get_promos(c["id"]))
    li = sum(1 for c in COURSES if "LinkedIn"  in get_promos(c["id"]))
    return total, done, pending, yt, ig, li

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Page background */
.stApp { background: #F7F8FC; }

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Metric cards */
[data-testid="metric-container"] {
    background: #fff;
    border: 1px solid #e8ecf4;
    border-radius: 14px;
    padding: 14px 18px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
[data-testid="metric-container"] label {
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #a0aec0 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 800 !important;
}

/* Buttons */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    padding: 4px 14px !important;
    transition: all 0.15s !important;
}
.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #fff;
    border-radius: 10px;
    padding: 4px;
    border: 1px solid #e8ecf4;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    color: #a0aec0 !important;
}
.stTabs [aria-selected="true"] {
    background: #667eea !important;
    color: #fff !important;
}

/* Search input */
.stTextInput input {
    border-radius: 9px !important;
    border: 1px solid #e8ecf4 !important;
    background: #fff !important;
    font-size: 13px !important;
}

/* Selectbox */
.stSelectbox > div > div {
    border-radius: 9px !important;
    border: 1px solid #e8ecf4 !important;
    background: #fff !important;
}

/* Expander (course rows) */
.streamlit-expanderHeader {
    background: #fff !important;
    border: 1px solid #e8ecf4 !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #2d3748 !important;
}
.streamlit-expanderContent {
    background: #fafbfe !important;
    border: 1px solid #e8ecf4 !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    padding: 12px 16px !important;
}

/* Progress bar */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #667eea, #764ba2) !important;
    border-radius: 3px !important;
}

/* Form */
.stForm { background: #fff; border-radius: 14px; border: 1px solid #e8ecf4; padding: 16px; }

/* Hide form border */
[data-testid="stForm"] { border: none !important; background: transparent !important; }

/* Divider */
hr { border-color: #e8ecf4 !important; margin: 8px 0 !important; }

/* Badge styling via markdown */
.badge-done    { background:#ECFDF5; color:#059669; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; border:1px solid #6EE7B7; }
.badge-pending { background:#FFF7ED; color:#D97706; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; border:1px solid #FCD34D; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
col_title, col_prog = st.columns([3, 2])
with col_title:
    st.markdown("## 📣 Course Promo Tracker")
    st.caption("Analytics Vidhya · Free Courses")

total, done, pending, yt, ig, li = compute_stats()
pct = int((done / total) * 100) if total else 0

with col_prog:
    st.markdown(f"**Overall Progress** — {done}/{total} promoted &nbsp; `{pct}%`")
    st.progress(pct / 100)

st.markdown("---")

# ── Stats Row ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("📚 Total",     total)
c2.metric("⏳ Pending",   pending)
c3.metric("✅ Done",      done)
c4.metric("▶ YouTube",   yt)
c5.metric("◈ Instagram", ig)
c6.metric("in LinkedIn",  li)

st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📋  Courses", "🕒  Activity Log"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 – COURSES
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    # Filter bar
    fcol1, fcol2 = st.columns([2, 3])
    with fcol1:
        search = st.text_input("", placeholder="🔍  Search courses...", label_visibility="collapsed")
    with fcol2:
        filter_opt = st.selectbox(
            "", ["All", "✅ Done (≥1 platform)", "⏳ Pending", "▶ YouTube", "◈ Instagram", "in LinkedIn"],
            label_visibility="collapsed"
        )

    # Apply filters
    def passes_filter(c):
        promos = get_promos(c["id"])
        if search and search.lower() not in c["name"].lower():
            return False
        if filter_opt == "All":
            return True
        if "Done" in filter_opt:
            return len(promos) >= 1
        if "Pending" in filter_opt:
            return len(promos) == 0
        if "YouTube" in filter_opt:
            return "YouTube" in promos
        if "Instagram" in filter_opt:
            return "Instagram" in promos
        if "LinkedIn" in filter_opt:
            return "LinkedIn" in promos
        return True

    visible = [c for c in COURSES if passes_filter(c)]
    st.caption(f"{len(visible)} courses shown")

    # Table header
    hc = st.columns([4, 1.5, 1.5, 1.5, 1.2])
    hc[0].markdown("**Course**")
    hc[1].markdown("**▶ YouTube**")
    hc[2].markdown("**◈ Instagram**")
    hc[3].markdown("**in LinkedIn**")
    hc[4].markdown("**Status**")
    st.markdown("<hr style='margin:4px 0 8px'/>", unsafe_allow_html=True)

    for course in visible:
        promos = get_promos(course["id"])
        is_done = len(promos) >= 1
        status_badge = (
            '<span class="badge-done">✅ Done</span>'
            if is_done else
            '<span class="badge-pending">⏳ Pending</span>'
        )

        row = st.columns([4, 1.5, 1.5, 1.5, 1.2])

        # Course name
        with row[0]:
            st.markdown(f"**{course['name']}**")
            st.caption(f"#{course['id']}")

        # Platform columns
        for i, plat in enumerate(PLATFORMS):
            with row[i + 1]:
                if plat in promos:
                    info = promos[plat]
                    st.markdown(
                        f"<span style='color:{PLATFORM_COLORS[plat]};font-weight:700;font-size:12px;'>✓ {info['date']}</span>",
                        unsafe_allow_html=True
                    )
                    if st.button("✕ undo", key=f"undo_{course['id']}_{plat}", use_container_width=True):
                        remove_promo(course["id"], plat)
                        st.rerun()
                else:
                    if st.button(f"+ Log", key=f"log_{course['id']}_{plat}", use_container_width=True):
                        st.session_state["modal_course"] = course
                        st.session_state["modal_platform"] = plat
                        st.rerun()

        # Status
        with row[4]:
            st.markdown(status_badge, unsafe_allow_html=True)

        st.markdown("<hr style='margin:4px 0'/>", unsafe_allow_html=True)

    # ── Log Modal (shown below table when triggered) ──────────────────────────
    if "modal_course" in st.session_state and st.session_state.modal_course:
        mc = st.session_state.modal_course
        mp = st.session_state.get("modal_platform", PLATFORMS[0])

        st.markdown("---")
        st.markdown(f"### 📝 Log Promotion — *{mc['name']}*")

        with st.form(key="promo_form"):
            fc1, fc2 = st.columns(2)
            with fc1:
                sel_platform = st.selectbox("Platform", PLATFORMS, index=PLATFORMS.index(mp))
            with fc2:
                sel_date = st.date_input("Date", value=date.today())
            sel_note = st.text_input("Note (optional)", placeholder="Post link, campaign tag...")

            sub_col, cancel_col = st.columns([2, 1])
            with sub_col:
                submitted = st.form_submit_button("✓ Mark as Promoted", use_container_width=True, type="primary")
            with cancel_col:
                cancelled = st.form_submit_button("Cancel", use_container_width=True)

        if submitted:
            existing = get_promos(mc["id"])
            if sel_platform in existing:
                st.warning(f"Already promoted on {sel_platform}!")
            else:
                mark_promoted(mc["id"], mc["name"], sel_platform, sel_date, sel_note)
                st.session_state.pop("modal_course", None)
                st.session_state.pop("modal_platform", None)
                st.success(f"Marked as promoted on {sel_platform} ✓")
                st.rerun()

        if cancelled:
            st.session_state.pop("modal_course", None)
            st.session_state.pop("modal_platform", None)
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 – ACTIVITY LOG
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    log = st.session_state.log
    if not log:
        st.markdown(
            "<div style='text-align:center;padding:60px 0;color:#a0aec0;'>"
            "<div style='font-size:40px'>📭</div>"
            "<div style='font-size:15px;margin-top:10px;'>No promotions logged yet.</div>"
            "<div style='font-size:12px;margin-top:4px;'>Go to the Courses tab and click + Log to get started.</div>"
            "</div>",
            unsafe_allow_html=True
        )
    else:
        lh = st.columns([3, 1.2, 1.2, 2])
        lh[0].markdown("**Course**")
        lh[1].markdown("**Platform**")
        lh[2].markdown("**Date**")
        lh[3].markdown("**Note**")
        st.markdown("<hr style='margin:4px 0 8px'/>", unsafe_allow_html=True)

        for entry in log:
            plat = entry["platform"]
            color = PLATFORM_COLORS.get(plat, "#718096")
            icon = PLATFORM_ICONS.get(plat, "")
            lrow = st.columns([3, 1.2, 1.2, 2])
            lrow[0].markdown(f"**{entry['course']}**")
            lrow[1].markdown(f"<span style='color:{color};font-weight:700'>{icon} {plat}</span>", unsafe_allow_html=True)
            lrow[2].markdown(entry["date"])
            lrow[3].markdown(entry["note"] if entry["note"] else "—")
            st.markdown("<hr style='margin:4px 0'/>", unsafe_allow_html=True)
