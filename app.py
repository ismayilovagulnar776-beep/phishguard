import streamlit as st
import joblib

st.set_page_config(
    page_title="PhishGuard AI | Cyber Defense Lab",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_model():
    data = joblib.load("phishing_model.joblib")
    return data["model"], data["tfidf"]

model, tfidf = load_model()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

:root {
    --bg-main: #030712;
    --bg-card: #0b1329;
    --bg-card-hover: #111e38;
    --border-color: #1e293b;
    --accent-cyan: #06b6d4;
    --accent-green: #10b981;
    --accent-purple: #8b5cf6;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
}

.stApp {
    background-color: var(--bg-main);
    background-image: 
        radial-gradient(at 0% 0%, rgba(6, 182, 212, 0.12) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.12) 0px, transparent 50%),
        radial-gradient(at 50% 100%, rgba(16, 185, 129, 0.08) 0px, transparent 50%);
    color: var(--text-main);
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.block-container {
    max-width: 1300px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

[data-testid="stSidebar"] {
    background: #050b18;
    border-right: 1px solid var(--border-color);
}

[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

.brand-box {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 8px 0;
    margin-bottom: 20px;
}

.brand-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(139, 92, 246, 0.2));
    border: 1px solid rgba(6, 182, 212, 0.4);
    box-shadow: 0 0 20px rgba(6, 182, 212, 0.15);
    font-size: 24px;
}

.brand-title {
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #ffffff;
}

.brand-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--accent-cyan);
    letter-spacing: 1.5px;
}

.system-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: var(--accent-green);
    padding: 6px 12px;
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    margin-bottom: 24px;
}

.hero-card {
    position: relative;
    padding: 36px;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(11, 19, 41, 0.8), rgba(17, 30, 56, 0.4));
    border: 1px solid var(--border-color);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(10px);
    margin-bottom: 24px;
    overflow: hidden;
}

.hero-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(to bottom, var(--accent-cyan), var(--accent-purple));
}

.hero-tag {
    font-family: 'JetBrains Mono', monospace;
    color: var(--accent-cyan);
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.hero-title {
    font-size: clamp(28px, 3.5vw, 42px);
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 12px;
    color: #ffffff;
}

.gradient-text {
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-green), var(--accent-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-desc {
    color: var(--text-muted);
    font-size: 15px;
    max-width: 700px;
    line-height: 1.6;
}

.custom-panel {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.custom-panel:hover {
    border-color: rgba(6, 182, 212, 0.3);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

div[data-testid="stTextArea"] textarea {
    background: #050b18 !important;
    color: #f1f5f9 !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    padding: 14px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    line-height: 1.6 !important;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 0 2px rgba(6, 182, 212, 0.2) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple)) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    min-height: 52px;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
    box-shadow: 0 10px 25px rgba(6, 182, 212, 0.2);
    transition: all 0.3s ease;
}

.stButton > button:hover {
    opacity: 0.9;
    transform: translateY(-2px);
    box-shadow: 0 15px 30px rgba(139, 92, 246, 0.3);
}

div[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    padding: 20px;
    border-radius: 14px;
}

div[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: var(--accent-cyan) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

div[data-testid="stProgress"] > div {
    background: var(--border-color);
    border-radius: 10px;
    height: 8px;
}

div[data-testid="stProgress"] div[role="progressbar"] {
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-green));
    border-radius: 10px;
}

[data-testid="stExpander"] {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
}

.footer {
    text-align: center;
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 1px;
    padding: 30px 0;
    border-top: 1px solid var(--border-color);
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div class="brand-box">
        <div class="brand-icon">🛡️</div>
        <div>
            <div class="brand-title">PhishGuard AI</div>
            <div class="brand-subtitle">CYBER DEFENSE</div>
        </div>
    </div>
    <div class="system-badge">● SYSTEM ONLINE</div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚙️ Scan Configuration")
    threshold = st.slider(
        "Phishing alert threshold",
        min_value=0.10,
        max_value=0.90,
        value=0.35,
        step=0.05
    )

    st.markdown("---")
    st.markdown("### 🧠 Model Intelligence")
    st.write("**Algorithm**")
    st.code("Logistic Regression")
    st.write("**Vectorization**")
    st.code("TF-IDF")
    st.write("**Test Accuracy**")
    st.markdown(
        "<span style='color:#10b981;font-size:22px;font-weight:800;font-family:JetBrains Mono'>98.39%</span>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.caption("EDUCATIONAL CYBERSECURITY PROTOTYPE")

# HERO SECTION
st.markdown("""
<div class="hero-card">
    <div class="hero-tag">⚡ Threat Intelligence & Analysis Module</div>
    <div class="hero-title">Detect threats instantly.<br><span class="gradient-text">Secure your digital perimeter.</span></div>
    <div class="hero-desc">
        Advanced machine learning email evaluation tool designed to detect phishing vectors, 
        calculate risk scores, and prevent cyber threats before they breach your inbox.
    </div>
</div>
""", unsafe_allow_html=True)

# FEATURE COLUMNS
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="custom-panel">
        <div style="color: var(--accent-cyan); font-family: 'JetBrains Mono'; font-size: 11px; letter-spacing: 1px;">MODULE 01</div>
        <div style="font-size: 16px; font-weight: 700; color: #fff; margin-top: 6px;">Email Parsing</div>
        <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">Granular text feature extraction</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="custom-panel">
        <div style="color: var(--accent-green); font-family: 'JetBrains Mono'; font-size: 11px; letter-spacing: 1px;">MODULE 02</div>
        <div style="font-size: 16px; font-weight: 700; color: #fff; margin-top: 6px;">Risk Scoring</div>
        <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">Deep probability evaluation</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="custom-panel">
        <div style="color: var(--accent-purple); font-family: 'JetBrains Mono'; font-size: 11px; letter-spacing: 1px;">MODULE 03</div>
        <div style="font-size: 16px; font-weight: 700; color: #fff; margin-top: 6px;">Alert Engine</div>
        <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">Dynamic threshold warnings</div>
    </div>
    """, unsafe_allow_html=True)

# SCANNER INPUT PANEL
st.markdown("""
<div class="custom-panel">
    <div style="font-size: 18px; font-weight: 700; color: #fff; margin-bottom: 4px;">🔍 Threat Scanner Payload</div>
    <div style="font-size: 13px; color: var(--text-muted);">Paste suspicious email contents below to initialize threat detection scan.</div>
</div>
""", unsafe_allow_html=True)

email_text = st.text_area(
    "EMAIL PAYLOAD INPUT",
    value="",
    height=180,
    placeholder="Dear user, your banking credentials require immediate verification. Click the secure link below to update..."
)

scan = st.button("⚡ INITIATE DEEP THREAT SCAN", use_container_width=True)

# ANALYSIS LOGIC & RESULTS
if scan:
    if not email_text.strip():
        st.warning("Zəhmət olmasa təhlil üçün hər hansı bir email mətni daxil edin.")
    else:
        email_vector = tfidf.transform([email_text])
        class_index = list(model.classes_).index(1)
        probability = model.predict_proba(email_vector)[0][class_index]

        st.markdown("---")
        st.markdown("### 📊 THREAT ANALYSIS REPORT")

        rep_col1, rep_col2 = st.columns(2)

        with rep_col1:
            st.metric("PHISHING PROBABILITY", f"{probability:.2%}")

        with rep_col2:
            st.metric(
                "SECURITY STATUS",
                "HIGH RISK" if probability >= threshold else "LOW RISK"
            )

        st.progress(float(probability))

        if probability >= threshold:
            st.error("🚨 HIGH RISK ALERT: POTENTIAL PHISHING DETECTED")
            st.markdown("""
            **RECOMMENDED SECURITY ACTIONS:**
            - Do not click on embedded links or download attachments.
            - Do not share sensitive personal information or credentials.
            - Report this email immediately to your cybersecurity operations center.
            """)
        else:
            st.success("✅ LOW THREAT DETECTED: Email appears safe based on current thresholds.")
            st.warning("Note: A low model score does not provide an absolute safety guarantee.")

        with st.expander("🛠️ INSPECT PIPELINE PROCESS"):
            st.write("01 / Input text tokenized and transformed via TF-IDF vectorizer.")
            st.write("02 / Logistic Regression model evaluated the feature probabilities.")
            st.write(f"03 / Calculated risk factor benchmarked against {threshold:.0%} user threshold.")
            st.caption("Educational AI prototype. Independent verification of links and sender addresses is always advised.")

# FOOTER
st.markdown("""
<div class="footer">
    PHISHGUARD AI &nbsp; // &nbsp; CYBER DEFENSE LAB<br>
    EDUCATIONAL PROTOTYPE · MODEL OUTPUT DOES NOT CONSTITUTE A FORMAL SECURITY GUARANTEE
</div>
""", unsafe_allow_html=True)
