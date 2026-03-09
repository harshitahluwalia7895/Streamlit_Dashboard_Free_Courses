import streamlit as st
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
PLATFORM_ICONS  = {"YouTube": "▶", "Instagram": "◈", "LinkedIn": "in"}
PLATFORM_COLORS = {"YouTube": "#E53E3E", "Instagram": "#D53F8C", "LinkedIn": "#2B6CB0"}

# ── Session State Init ────────────────────────────────────────────────────────
for key, default in [
    ("promotions", {}),
    ("activity_log", []),
    ("show_form", False),
    ("form_course", None),
    ("form_platform", "YouTube"),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_promos(course_id):
    return st.session_state.promotions.get(str(course_id), {})

def open_form(course, platform):
    st.session_state.show_form     = True
    st.session_state.form_course   = course
    st.session_state.form_platform = platform

def close_form():
    st.session_state.show_form     = False
    st.session_state.form_course   = None
    st.session_state.form_platform = "YouTube"

def save_promotion(course_id, course_name, platform, promo_date, note):
    cid = str(course_id)
    if cid not in st.session_state.promotions:
        st.session_state.promotions[cid] = {}
    st.session_state.promotions[cid][platform] = {"date": str(promo_date), "note": note}
    st.session_state.activity_log.insert(0, {
        "course": course_name, "platform": platform,
        "date": str(promo_date), "note": note
    })

def undo_promotion(course_id, platform):
    cid = str(course_id)
    if cid in st.session_state.promotions:
        st.session_state.promotions[cid].pop(platform, None)
        if not st.session_state.promotions[cid]:
            del st.session_state.promotions[cid]

def compute_stats():
    total   = len(COURSES)
    done    = sum(1 for c in COURSES if len(get_promos(c["id"])) >= 1)
    pending = sum(1 for c in COURSES if len(get_promos(c["id"])) == 0)
    yt  = sum(1 for c in COURSES if "YouTube"   in get_promos(c["id"]))
    ig  = sum(1 for c in COURSES if "Instagram" in get_promos(c["id"]))
    li  = sum(1 for c in COURSES if "LinkedIn"  in get_promos(c["id"]))
    return total, done, pending, yt, ig, li

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background: #F7F8FC; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="metric-container"] {
    background: #fff; border: 1px solid #e8ecf4;
    border-radius: 14px; padding: 14px 18px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
[data-testid="metric-container"] label {
    font-size: 11px !important; font-weight: 700 !important;
    text-transform: uppercase; letter-spacing: 0.5px; color: #a0aec0 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 28px !important; font-weight: 800 !important;
}
.stButton > button {
    border-radius: 8px !important; font-weight: 600 !important;
    font-size: 12px !important; padding: 4px 14px !important;
    border: 1px solid #e8ecf4 !important; transition: all 0.15s !important;
}
.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important; }
.stTabs [data-baseweb="tab-list"] {
    background: #fff; border-radius: 10px; padding: 4px;
    border: 1px solid #e8ecf4; gap: 4px;
}
.stTabs [data-baseweb="tab"] { border-radius: 7px !important; font-weight: 600 !important; font-size: 13px !important; color: #a0aec0 !important; }
.stTabs [aria-selected="true"] { background: #667eea !important; color: #fff !important; }
.stTextInput input { border-radius: 9px !important; border: 1px solid #e8ecf4 !important; background: #fff !important; }
.stSelectbox > div > div { border-radius: 9px !important; border: 1px solid #e8ecf4 !important; background: #fff !important; }
.stProgress > div > div > div { background: linear-gradient(90deg, #667eea, #764ba2) !important; border-radius: 3px !important; }
.badge-done    { background:#ECFDF5; color:#059669; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; border:1px solid #6EE7B7; display:inline-block; }
.badge-pending { background:#FFF7ED; color:#D97706; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; border:1px solid #FCD34D; display:inline-block; }
.promo-tag { padding:3px 10px; border-radius:6px; font-size:12px; font-weight:700; display:inline-block; }
.form-card { background:#fff; border:2px solid #667eea; border-radius:16px; padding:20px 24px; margin:12px 0 20px; box-shadow:0 4px 20px rgba(102,126,234,0.15); }
hr { border-color: #e8ecf4 !important; margin: 6px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
hc1, hc2 = st.columns([3, 2])
with hc1:
    st.markdown("## 📣 Course Promo Tracker")
    st.caption("Analytics Vidhya · Free Courses")

total, done, pending, yt, ig, li = compute_stats()
pct = int((done / total) * 100) if total else 0
with hc2:
    st.markdown(f"**Overall Progress** — {done}/{total} promoted &nbsp; `{pct}%`")
    st.progress(pct / 100)

st.markdown("---")

# ── Stats ─────────────────────────────────────────────────────────────────────
s1, s2, s3, s4, s5, s6 = st.columns(6)
s1.metric("📚 Total",     total)
s2.metric("⏳ Pending",   pending)
s3.metric("✅ Done",      done)
s4.metric("▶ YouTube",   yt)
s5.metric("◈ Instagram", ig)
s6.metric("in LinkedIn",  li)

st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📋  Courses", "🕒  Activity Log"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — COURSES
# ════════════════════════════════════════════════════════════════════════════════
with tab1:

    # ── Log Form (renders at top when a + Log button was clicked) ─────────────
    if st.session_state.show_form and st.session_state.form_course:
        fc = st.session_state.form_course
        fp = st.session_state.form_platform

        st.markdown(
            f'<div class="form-card">'
            f'<h4 style="margin:0 0 4px;color:#1a202c;">📝 Log Promotion</h4>'
            f'<p style="margin:0;color:#718096;font-size:13px;">{fc["name"]}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

        fa, fb, fc_col = st.columns([2, 2, 3])
        with fa:
            sel_platform = st.selectbox("Platform", PLATFORMS,
                                        index=PLATFORMS.index(fp), key="form_sel_platform")
        with fb:
            sel_date = st.date_input("Date", value=date.today(), key="form_sel_date")
        with fc_col:
            sel_note = st.text_input("Note (optional)",
                                     placeholder="Post link, campaign name...", key="form_sel_note")

        save_col, cancel_col, _ = st.columns([1.8, 1.2, 4])
        with save_col:
            if st.button("✓ Mark as Promoted", type="primary",
                         use_container_width=True, key="form_save_btn"):
                existing = get_promos(st.session_state.form_course["id"])
                if sel_platform in existing:
                    st.warning(f"Already promoted on {sel_platform}!")
                else:
                    save_promotion(
                        st.session_state.form_course["id"],
                        st.session_state.form_course["name"],
                        sel_platform, sel_date, sel_note
                    )
                    close_form()
                    st.rerun()
        with cancel_col:
            if st.button("✕ Cancel", use_container_width=True, key="form_cancel_btn"):
                close_form()
                st.rerun()

        st.markdown("---")

    # ── Filters ───────────────────────────────────────────────────────────────
    fl1, fl2 = st.columns([2, 3])
    with fl1:
        search = st.text_input("", placeholder="🔍  Search courses...",
                               label_visibility="collapsed", key="search_box")
    with fl2:
        filter_opt = st.selectbox(
            "",
            ["All", "✅ Done (promoted on any platform)",
             "⏳ Not yet promoted", "▶ YouTube", "◈ Instagram", "in LinkedIn"],
            label_visibility="collapsed", key="filter_box"
        )

    def passes_filter(c):
        p = get_promos(c["id"])
        if search and search.lower() not in c["name"].lower():
            return False
        if "All"       in filter_opt: return True
        if "Done"      in filter_opt: return len(p) >= 1
        if "Not yet"   in filter_opt: return len(p) == 0
        if "YouTube"   in filter_opt: return "YouTube"   in p
        if "Instagram" in filter_opt: return "Instagram" in p
        if "LinkedIn"  in filter_opt: return "LinkedIn"  in p
        return True

    visible = [c for c in COURSES if passes_filter(c)]
    st.caption(f"{len(visible)} courses shown")
    st.markdown("")

    # ── Column headers ────────────────────────────────────────────────────────
    hdr = st.columns([4, 1.6, 1.6, 1.6, 1.4])
    for col, lbl in zip(hdr, ["**Course**", "**▶ YouTube**",
                               "**◈ Instagram**", "**in LinkedIn**", "**Status**"]):
        col.markdown(lbl)
    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Rows ──────────────────────────────────────────────────────────────────
    for course in visible:
        promos  = get_promos(course["id"])
        is_done = len(promos) >= 1
        row     = st.columns([4, 1.6, 1.6, 1.6, 1.4])

        with row[0]:
            st.markdown(f"**{course['name']}**")
            st.caption(f"#{course['id']}")

        for idx, plat in enumerate(PLATFORMS):
            with row[idx + 1]:
                if plat in promos:
                    info  = promos[plat]
                    color = PLATFORM_COLORS[plat]
                    st.markdown(
                        f"<span class='promo-tag' "
                        f"style='background:{color}18;color:{color};border:1px solid {color}44;'>"
                        f"✓ {info['date']}</span>",
                        unsafe_allow_html=True
                    )
                    # Key must be unique and stable across reruns
                    if st.button("✕ undo",
                                 key=f"undo__{course['id']}__{plat}"):
                        undo_promotion(course["id"], plat)
                        st.rerun()
                else:
                    if st.button("+ Log",
                                 key=f"log__{course['id']}__{plat}",
                                 use_container_width=True):
                        open_form(course, plat)
                        st.rerun()

        with row[4]:
            if is_done:
                st.markdown('<span class="badge-done">✅ Done</span>',
                            unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge-pending">⏳ Pending</span>',
                            unsafe_allow_html=True)

        st.markdown("<hr/>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — ACTIVITY LOG
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    log = st.session_state.activity_log

    if not log:
        st.markdown("""
        <div style='text-align:center;padding:60px 0;color:#a0aec0;'>
            <div style='font-size:44px'>📭</div>
            <div style='font-size:15px;margin-top:12px;font-weight:600;'>No promotions logged yet.</div>
            <div style='font-size:12px;margin-top:4px;'>Go to the Courses tab and click + Log to get started.</div>
        </div>""", unsafe_allow_html=True)
    else:
        lh = st.columns([3, 1.3, 1.3, 2])
        for col, lbl in zip(lh, ["**Course**", "**Platform**", "**Date**", "**Note**"]):
            col.markdown(lbl)
        st.markdown("<hr/>", unsafe_allow_html=True)

        for entry in log:
            plat  = entry["platform"]
            color = PLATFORM_COLORS.get(plat, "#718096")
            icon  = PLATFORM_ICONS.get(plat, "")
            lr    = st.columns([3, 1.3, 1.3, 2])
            lr[0].markdown(f"**{entry['course']}**")
            lr[1].markdown(
                f"<span style='color:{color};font-weight:700;font-size:13px;'>"
                f"{icon} {plat}</span>",
                unsafe_allow_html=True
            )
            lr[2].markdown(entry["date"])
            lr[3].markdown(entry["note"] if entry["note"] else "—")
            st.markdown("<hr/>", unsafe_allow_html=True)
