
import streamlit as st
import joblib

st.set_page_config(
    page_title="PhishGuard AI | Email Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_model():
    data = joblib.load("phishing_model.joblib")
    return data["model"], data["tfidf"]

model, tfidf = load_model()

# ---------- DESIGN ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #080D1B;
    --panel: #111A2E;
    --border: #263653;
    --cyan: #45E5FF;
    --purple: #9B7BFF;
    --text: #F0F5FF;
    --muted: #9AABC5;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #16264A 0%, transparent 40%),
        radial-gradient(ellipse at 90% 20%, #251747 0%, transparent 35%),
        #080D1B;
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #0C1426;
    border-right: 1px solid #263653;
}

[data-testid="stSidebar"] * {
    color: #E4EDFF;
}

.brand {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 25px;
}

.brand-icon {
    background: linear-gradient(135deg, #167DE8, #8455F7);
    border-radius: 15px;
    width: 54px;
    height: 54px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 29px;
    box-shadow: 0 0 28px #247CE744;
}

.brand-name {
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #FFFFFF;
}

.brand-sub {
    color: #91A6C8;
    font-size: 10px;
    letter-spacing: 2px;
}

.status {
    display: inline-block;
    border: 1px solid #245B56;
    background: #102B30;
    color: #6DF3C5;
    padding: 7px 13px;
    border-radius: 30px;
    font-size: 12px;
    margin-bottom: 22px;
}

.hero {
    padding: 30px 0 24px 0;
}

.eyebrow {
    color: #54DFFF;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.hero h1 {
    color: #F4F7FF;
    font-size: clamp(32px, 4vw, 52px);
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 1.13;
    margin: 14px 0;
}

.gradient-text {
    background: linear-gradient(90deg, #48E4FF, #A58BFF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #A7B7D0;
    font-size: 16px;
    line-height: 1.8;
    max-width: 680px;
}

.panel {
    background: linear-gradient(145deg, #131F35, #10182A);
    border: 1px solid #2A3C5A;
    border-radius: 22px;
    padding: 26px;
    margin: 10px 0 22px 0;
    box-shadow: 0 15px 45px #00000020;
}

.panel-title {
    font-size: 21px;
    font-weight: 700;
    color: #F3F6FF;
}

.panel-sub {
    font-size: 13px;
    color: #9AABC5;
    margin-top: 5px;
    margin-bottom: 20px;
}

/* Readable Model Intelligence card */
.model-info {
    background: #142238;
    border: 1px solid #344967;
    border-radius: 12px;
    padding: 16px;
    margin: 12px 0;
}

.model-info-title {
    color: #55E6FF !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    line-height: 1.5;
    margin-bottom: 18px;
}

.model-label {
    color: #D5E1F0 !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0.7px;
    margin-top: 14px;
    margin-bottom: 7px;
}

.model-value {
    color: #FFFFFF !important;
    background: #0A1424;
    border: 1px solid #304763;
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 14px !important;
    font-weight: 600 !important;
    line-height: 1.6;
    overflow-wrap: anywhere;
}

div[data-testid="stTextArea"] textarea {
    background: #0A1222 !important;
    color: #EAF2FF !important;
    border: 1px solid #344967 !important;
    border-radius: 13px !important;
    line-height: 1.7 !important;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: #4BCEFF !important;
    box-shadow: 0 0 0 1px #4BCEFF44 !important;
}

.stButton > button {
    background: linear-gradient(100deg, #087FE8, #7956F5) !important;
    color: white !important;
    border: 0 !important;
    border-radius: 12px !important;
    min-height: 49px;
    font-weight: 700 !important;
    transition: 0.2s ease;
}

.stButton > button:hover {
    box-shadow: 0 0 24px #6B63FF55;
    transform: translateY(-1px);
}

div[data-testid="stMetric"] {
    background: #111D31;
    border: 1px solid #2A3C5A;
    padding: 18px;
    border-radius: 16px;
}

div[data-testid="stMetricLabel"] {
    color: #A7B7D0 !important;
}

div[data-testid="stMetricValue"] {
    color: #53E2FF !important;
}

div[data-testid="stProgress"] > div {
    background: #25344D;
    border-radius: 20px;
}

div[data-testid="stProgress"] div[role="progressbar"] {
    background: linear-gradient(90deg, #15C8E8, #9868FF);
}

div[data-testid="stAlert"] {
    border-radius: 13px;
}

h2, h3 {
    color: #F1F5FF !important;
}

hr {
    border-color: #263653 !important;
}

.footer {
    text-align: center;
    color: #A7B7D0;
    font-size: 12px;
    padding: 22px 0;
    border-top: 1px solid #263653;
    margin-top: 30px;
}

div[data-testid="stCaptionContainer"] {
    color: #B4C3D8;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem;
    }

    .panel {
        padding: 17px;
    }

    .hero h1 {
        letter-spacing: -1px;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🛡️</div>
        <div>
            <div class="brand-name">PhishGuard AI</div>
            <div class="brand-sub">EMAIL SECURITY</div>
        </div>
    </div>
    <div class="status">● &nbsp; AI MODEL LOADED</div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚙️ Analysis settings")

    threshold = st.slider(
        "Phishing xəbərdarlıq həddi",
        min_value=0.10,
        max_value=0.90,
        value=0.35,
        step=0.05,
        help="Hədd aşağı olduqda daha çox email phishing kimi işarələnə bilər."
    )

    st.markdown("---")
    st.markdown("### 🤖 Model məlumatları")

    st.markdown("""
    <div class="model-info">
        <div class="model-info-title">
            🧠 MODEL INTELLIGENCE
        </div>

        <div class="model-label">ALGORITHM</div>
        <div class="model-value">Logistic Regression</div>

        <div class="model-label">TEXT VECTORIZATION</div>
        <div class="model-value">TF-IDF</div>

        <div class="model-label">TEST ACCURACY</div>
        <div class="model-value">98.39%</div>
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        "Tədris məqsədli prototip. "
        "Real təhlükəsizlik zəmanəti vermir."
    )

# ---------- HERO ----------
st.markdown("""
<div class="hero">
    <div class="eyebrow">NEXT-GENERATION EMAIL PROTECTION</div>
    <h1>Stay one step ahead of<br>
    <span class="gradient-text">phishing attacks.</span></h1>
    <p>
        E-poçt mətnini süni intellekt əsaslı model ilə analiz et,
        potensial phishing təhlükələrini müəyyənləşdir və
        daha məlumatlı təhlükəsizlik qərarları ver.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- SCANNER ----------
st.markdown("""
<div class="panel">
    <div class="panel-title">📩 Email Security Scanner</div>
    <div class="panel-sub">
        Şübhəli e-poçtun mətnini aşağıya daxil et və analizə başla.
    </div>
</div>
""", unsafe_allow_html=True)

email_text = st.text_area(
    "Email məzmunu",
    value="",
    height=200,
    placeholder=(
        "Dear user, your account will be suspended. "
        "Click here to verify your password immediately..."
    ),
    label_visibility="collapsed"
)

scan = st.button(
    "🔍  ANALYZE EMAIL",
    type="primary",
    use_container_width=True
)

# ---------- ANALYSIS ----------
if scan:
    if not email_text.strip():
        st.warning("Zəhmət olmasa, əvvəlcə email mətnini daxil et.")
    else:
        email_vector = tfidf.transform([email_text])
        class_index = list(model.classes_).index(1)
        probability = model.predict_proba(email_vector)[0][class_index]

        st.markdown("---")
        st.markdown("## 📊 Analysis report")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Phishing ehtimalı", f"{probability:.2%}")

        with col2:
            if probability >= threshold:
                st.metric("Risk statusu", "YÜKSƏK RİSK")
            else:
                st.metric("Risk statusu", "AŞAĞI RİSK")

        st.progress(float(probability))

        if probability >= threshold:
            st.error(
                "🚨 Potensial phishing aşkarlandı! "
                "Bu email-i şübhəli hesab et."
            )
            st.markdown("""
            **Təhlükəsizlik tövsiyələri**
            - Şübhəli linklərə klikləmə.
            - Şifrən və digər məxfi məlumatlarını daxil etmə.
            - Göndərənin kimliyini ayrıca yoxla.
            """)
        else:
            st.success(
                "✅ Email seçilmiş həddə görə phishing kimi "
                "işarələnmədi."
            )
            st.warning(
                "Bu nəticə email-in tam təhlükəsiz olduğunu "
                "sübut etmir."
            )

        with st.expander("🔬 Model qərarını necə verdi?"):
            st.write(
                "1. Email mətni TF-IDF vasitəsilə rəqəmsal "
                "xüsusiyyətlərə çevrildi."
            )
            st.write(
                "2. Logistic Regression modeli phishing "
                "ehtimalını hesabladı."
            )
            st.write(
                f"3. Nəticə {threshold:.0%} qərar həddi ilə müqayisə edildi."
            )
            st.caption(
                "Göstərilən ehtimal modelin hesablamasıdır; "
                "təhlükənin dəqiq ölçüsü və ya zəmanəti deyil."
            )

# ---------- FEATURE CARDS ----------
st.markdown("---")
st.markdown("## ✨ Platform features")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 🧠")
    st.markdown("**AI Analysis**")
    st.caption("E-poçt mətninin avtomatik təsnifatı.")

with c2:
    st.markdown("### ⚡")
    st.markdown("**Fast Detection**")
    st.caption("Daxil edilən mətnin sürətli analizi.")

with c3:
    st.markdown("### 🎚️")
    st.markdown("**Adjustable Threshold**")
    st.caption("Xəbərdarlıq həddini ehtiyaca görə dəyişmək.")

st.markdown("""
<div class="footer">
    🛡️ PhishGuard AI · Educational Cybersecurity Project<br><br>
    AI əsaslı phishing aşkarlama prototipi · Nəticələr zəmanət deyil
</div>
""", unsafe_allow_html=True)
