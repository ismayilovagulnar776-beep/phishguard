
import streamlit as st
import joblib

st.set_page_config(
    page_title="PhishGuard AI | Cyber Defense",
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Share+Tech+Mono&display=swap');

:root {
    --bg: #050914;
    --panel: #0B1424;
    --panel2: #101D31;
    --border: #1D3850;
    --cyan: #00E5FF;
    --green: #00FFA3;
    --purple: #8B5CF6;
    --text: #E5F1FF;
    --muted: #8BA3BF;
}

.stApp {
    background:
        radial-gradient(ellipse at 15% 0%, #07304455, transparent 38%),
        radial-gradient(ellipse at 90% 10%, #30145A35, transparent 32%),
        #050914;
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}

[data-testid="stHeader"] {
    background: #050914;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #091321, #060B16);
    border-right: 1px solid #17334A;
}

[data-testid="stSidebar"] * {
    color: #D5E7F7;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
}

.brand-icon {
    width: 51px;
    height: 51px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 14px;
    background: linear-gradient(135deg, #003F59, #143B76);
    border: 1px solid #00D9FF80;
    box-shadow: 0 0 24px #00D9FF25;
    font-size: 27px;
}

.brand-name {
    color: #F0FAFF;
    font-size: 23px;
    font-weight: 800;
    letter-spacing: -1px;
}

.brand-sub {
    color: #00D9FF;
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
}

.status {
    display: inline-block;
    color: #00FFA3;
    background: #00FFA30D;
    border: 1px solid #00FFA344;
    border-radius: 5px;
    padding: 8px 11px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    letter-spacing: 1px;
    margin-bottom: 20px;
}

.hero {
    position: relative;
    padding: 26px 28px 30px;
    margin: 10px 0 24px;
    border: 1px solid #15364C;
    border-radius: 17px;
    background: linear-gradient(110deg, #0B1728, #0B1424DD);
    box-shadow: 0 0 35px #00D9FF08;
    overflow: hidden;
}

.hero:after {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    height: 3px;
    width: 45%;
    background: linear-gradient(90deg, transparent, #00E5FF, #8B5CF6);
}

.eyebrow {
    color: #00E5FF;
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    letter-spacing: 3px;
}

.hero h1 {
    color: #F0F8FF;
    font-size: clamp(31px, 4vw, 49px);
    font-weight: 800;
    letter-spacing: -1.8px;
    line-height: 1.15;
    margin: 15px 0;
}

.gradient-text {
    background: linear-gradient(90deg, #00E5FF, #00FFA3, #9D83FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #9BB1CB;
    font-size: 15px;
    line-height: 1.8;
    max-width: 730px;
}

.panel {
    background: linear-gradient(145deg, #0D192B, #091321);
    border: 1px solid #1A354D;
    border-radius: 15px;
    padding: 24px;
    margin: 10px 0 20px;
    box-shadow: inset 0 1px #FFFFFF05, 0 12px 35px #00000020;
}

.panel-title {
    color: #E8F6FF;
    font-size: 21px;
    font-weight: 700;
}

.panel-sub {
    color: #8BA3BF;
    font-size: 13px;
    margin-top: 7px;
}

div[data-testid="stTextArea"] label {
    color: #00DFFF !important;
    font-weight: 600;
}

div[data-testid="stTextArea"] textarea {
    background: #060D19 !important;
    color: #D9F5FF !important;
    border: 1px solid #1D435A !important;
    border-radius: 10px !important;
    line-height: 1.7 !important;
    caret-color: #00FFA3;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: #00E5FF !important;
    box-shadow: 0 0 0 1px #00E5FF44, 0 0 18px #00E5FF12 !important;
}

.stButton > button {
    background: linear-gradient(100deg, #007EAD, #5142B8) !important;
    color: #FFFFFF !important;
    border: 1px solid #00DFFF70 !important;
    border-radius: 9px !important;
    min-height: 50px;
    font-weight: 700 !important;
    letter-spacing: 1px;
    box-shadow: 0 0 20px #00CFFF15;
    transition: all .2s ease;
}

.stButton > button:hover {
    border-color: #00FFA3 !important;
    box-shadow: 0 0 24px #00E5FF35;
    transform: translateY(-1px);
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #0E1D31, #091321);
    border: 1px solid #1D3A53;
    padding: 18px;
    border-radius: 12px;
}

div[data-testid="stMetricLabel"] {
    color: #8BA3BF !important;
}

div[data-testid="stMetricValue"] {
    color: #00E5FF !important;
    font-family: 'Share Tech Mono', monospace;
}

div[data-testid="stProgress"] > div {
    background: #14283B;
    border-radius: 20px;
}

div[data-testid="stProgress"] div[role="progressbar"] {
    background: linear-gradient(90deg, #00E5FF, #00FFA3);
    box-shadow: 0 0 12px #00E5FF50;
}

div[data-testid="stAlert"] {
    border-radius: 10px;
}

h2, h3 {
    color: #E5F1FF !important;
}

hr {
    border-color: #1B3048 !important;
}

div[data-testid="stCaptionContainer"] {
    color: #8199B5;
}

[data-testid="stExpander"] {
    background: #0B1525;
    border: 1px solid #1C354E;
    border-radius: 10px;
}

div[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: #00E5FF;
}

.footer {
    text-align: center;
    color: #68829E;
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    letter-spacing: 1px;
    padding: 24px 0;
    border-top: 1px solid #1B3048;
    margin-top: 30px;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem;
    }
    .hero {
        padding: 20px;
    }
    .panel {
        padding: 17px;
    }
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🛡️</div>
        <div>
            <div class="brand-name">PhishGuard AI</div>
            <div class="brand-sub">CYBER DEFENSE SYSTEM</div>
        </div>
    </div>
    <div class="status">● SYSTEM INITIALIZED</div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚙️ Scan configuration")

    threshold = st.slider(
        "Phishing alert threshold",
        min_value=0.10,
        max_value=0.90,
        value=0.35,
        step=0.05
    )

    st.markdown("---")
    st.markdown("### 🧠 MODEL INTELLIGENCE")
    st.write("**Algorithm**")
    st.code("Logistic Regression")
    st.write("**Text vectorization**")
    st.code("TF-IDF")
    st.write("**Test accuracy**")
    st.markdown(
        "<span style='color:#00FFA3;font-size:23px;"
        "font-weight:800'>98.39%</span>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.caption("EDUCATIONAL CYBERSECURITY PROTOTYPE")

# HERO
st.markdown("""
<div class="hero">
    <div class="eyebrow">◈ CYBER THREAT ANALYSIS / MODULE 01</div>
    <h1>Detect threats.<br>
    <span class="gradient-text">Defend your inbox.</span></h1>
    <p>
        AI-powered phishing email analysis. Scan suspicious messages,
        evaluate their predicted risk, and make safer security decisions.
    </p>
</div>
""", unsafe_allow_html=True)

# FEATURE STRIP
a, b, c = st.columns(3)

with a:
    st.markdown("""
    <div class="panel">
        <div style="color:#00E5FF;font-size:11px;letter-spacing:2px">
        MODULE 01
        </div>
        <div style="font-size:17px;font-weight:700;color:#E5F1FF;
        margin-top:8px">EMAIL ANALYSIS</div>
        <div style="font-size:12px;color:#8BA3BF;margin-top:6px">
        Text-based threat classification
        </div>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown("""
    <div class="panel">
        <div style="color:#00FFA3;font-size:11px;letter-spacing:2px">
        MODULE 02
        </div>
        <div style="font-size:17px;font-weight:700;color:#E5F1FF;
        margin-top:8px">RISK SCORING</div>
        <div style="font-size:12px;color:#8BA3BF;margin-top:6px">
        Model probability evaluation
        </div>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown("""
    <div class="panel">
        <div style="color:#A58BFF;font-size:11px;letter-spacing:2px">
        MODULE 03
        </div>
        <div style="font-size:17px;font-weight:700;color:#E5F1FF;
        margin-top:8px">THREAT ALERT</div>
        <div style="font-size:12px;color:#8BA3BF;margin-top:6px">
        Threshold-based warning
        </div>
    </div>
    """, unsafe_allow_html=True)

# SCANNER
st.markdown("""
<div class="panel">
    <div class="panel-title">⌁ &nbsp; Email Threat Scanner</div>
    <div class="panel-sub">
        Paste a suspicious email below to run a model-based analysis.
    </div>
</div>
""", unsafe_allow_html=True)

email_text = st.text_area(
    "EMAIL PAYLOAD",
    value="",
    height=200,
    placeholder=(
        "Dear user, your account will be suspended. "
        "Click here to verify your password immediately..."
    )
)

scan = st.button(
    "⌁   INITIATE THREAT SCAN",
    type="primary",
    use_container_width=True
)

# ANALYSIS
if scan:
    if not email_text.strip():
        st.warning("Email mətnini daxil et və yenidən yoxla.")
    else:
        email_vector = tfidf.transform([email_text])
        class_index = list(model.classes_).index(1)
        probability = model.predict_proba(email_vector)[0][class_index]

        st.markdown("---")
        st.markdown("## ◈ THREAT ANALYSIS REPORT")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("PHISHING PROBABILITY", f"{probability:.2%}")

        with col2:
            st.metric(
                "DETECTION STATUS",
                "HIGH RISK" if probability >= threshold
                else "LOW RISK"
            )

        st.progress(float(probability))

        if probability >= threshold:
            st.error("⚠️ POTENTIAL PHISHING DETECTED")
            st.markdown("""
            **DEFENSE RECOMMENDATIONS**
            - Do not click suspicious links.
            - Do not provide passwords or personal information.
            - Verify the sender through a trusted channel.
            """)
        else:
            st.success("✓ No phishing classification at the selected threshold.")
            st.warning(
                "A low model score does not guarantee that the email is safe."
            )

        with st.expander("⌘ INSPECT ANALYSIS PROCESS"):
            st.write("01 / Email text converted into TF-IDF features.")
            st.write("02 / Logistic Regression calculated the phishing probability.")
            st.write(f"03 / Probability compared against the {threshold:.0%} threshold.")
            st.caption(
                "This prototype analyzes email text only. "
                "It does not independently verify URLs, attachments, or sender identity."
            )

# FOOTER
st.markdown("""
<div class="footer">
    PHISHGUARD AI &nbsp; // &nbsp; CYBER DEFENSE LAB<br><br>
    EDUCATIONAL PROTOTYPE · MODEL OUTPUT IS NOT A SECURITY GUARANTEE
</div>
""", unsafe_allow_html=True)
