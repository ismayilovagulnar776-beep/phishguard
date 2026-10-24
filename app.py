
import streamlit as st
import joblib

st.set_page_config(
    page_title="PhishGuard AI",
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at top left, #E1F2FF 0%, transparent 40%),
        radial-gradient(ellipse at top right, #F0E9FF 0%, transparent 35%),
        #F6F8FD;
    color: #192A48;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E1E8F3;
}

[data-testid="stSidebar"] * {
    color: #243756;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
}

.brand-icon {
    background: linear-gradient(135deg, #168BDE, #8660ED);
    border-radius: 15px;
    width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    box-shadow: 0 7px 18px #6C80E533;
}

.brand-name {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #192A48;
}

.brand-sub {
    color: #71829D;
    font-size: 10px;
    letter-spacing: 2px;
}

.status {
    display: inline-block;
    border: 1px solid #BCEBD8;
    background: #EAFBF3;
    color: #12815D;
    padding: 8px 12px;
    border-radius: 30px;
    font-size: 12px;
    margin-bottom: 22px;
}

.hero {
    padding: 28px 0 25px;
}

.eyebrow {
    color: #397DE0;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 3px;
}

.hero h1 {
    color: #192A48;
    font-size: clamp(34px, 4vw, 53px);
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 1.16;
    margin: 15px 0;
}

.gradient-text {
    background: linear-gradient(90deg, #168BDE, #8256E8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #64748B;
    font-size: 16px;
    line-height: 1.8;
    max-width: 720px;
}

.panel {
    background: linear-gradient(135deg, #FFFFFF, #FAFBFF);
    border: 1px solid #DCE6F5;
    border-radius: 22px;
    padding: 25px;
    margin: 10px 0 20px;
    box-shadow: 0 12px 35px #294A7610;
}

.panel-title {
    font-size: 22px;
    font-weight: 800;
    color: #192A48;
}

.panel-sub {
    font-size: 14px;
    color: #71819A;
    margin-top: 7px;
}

div[data-testid="stTextArea"] textarea {
    background: #FFFFFF !important;
    color: #192A48 !important;
    border: 1px solid #D4DFEF !important;
    border-radius: 14px !important;
    line-height: 1.7 !important;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: #438CEB !important;
    box-shadow: 0 0 0 2px #438CEB22 !important;
}

.stButton > button {
    background: linear-gradient(100deg, #168BDE, #7958E9) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 13px !important;
    min-height: 50px;
    font-weight: 700 !important;
    box-shadow: 0 7px 18px #627BE52B;
    transition: 0.2s ease;
}

.stButton > button:hover {
    box-shadow: 0 10px 25px #627BE54A;
    transform: translateY(-1px);
}

div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #DCE6F5;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 8px 24px #294A760B;
}

div[data-testid="stMetricLabel"] {
    color: #71819A !important;
}

div[data-testid="stMetricValue"] {
    color: #2869D7 !important;
}

div[data-testid="stProgress"] > div {
    background: #E3EAF5;
    border-radius: 20px;
}

div[data-testid="stProgress"] div[role="progressbar"] {
    background: linear-gradient(90deg, #168BDE, #9561EF);
}

div[data-testid="stAlert"] {
    border-radius: 13px;
}

h2, h3 {
    color: #192A48 !important;
}

hr {
    border-color: #DFE7F2 !important;
}

div[data-testid="stCaptionContainer"] {
    color: #71819A;
}

.footer {
    text-align: center;
    color: #8290A5;
    font-size: 12px;
    padding: 24px 0;
    border-top: 1px solid #DFE7F2;
    margin-top: 32px;
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

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🛡️</div>
        <div>
            <div class="brand-name">PhishGuard AI</div>
            <div class="brand-sub">EMAIL SECURITY</div>
        </div>
    </div>
    <div class="status">● &nbsp; AI MODEL READY</div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚙️ Analiz parametrləri")

    threshold = st.slider(
        "Phishing xəbərdarlıq həddi",
        min_value=0.10,
        max_value=0.90,
        value=0.35,
        step=0.05
    )

    st.markdown("---")
    st.markdown("### 🤖 Model məlumatları")
    st.write("**Alqoritm:** Logistic Regression")
    st.write("**Mətn emalı:** TF-IDF")
    st.write("**Test accuracy:** 98.39%")

    st.info(
        "Hədd aşağı olduqda daha çox email phishing "
        "kimi işarələnə bilər."
    )

# HERO
st.markdown("""
<div class="hero">
    <div class="eyebrow">AI-POWERED EMAIL SECURITY</div>
    <h1>Stay one step ahead of<br>
    <span class="gradient-text">phishing attacks.</span></h1>
    <p>
        E-poçt mətnini süni intellekt əsaslı model ilə analiz et,
        potensial phishing təhlükələrini müəyyənləşdir və
        onlayn təhlükəsizliyin üçün daha məlumatlı qərarlar ver.
    </p>
</div>
""", unsafe_allow_html=True)

# SCANNER PANEL
st.markdown("""
<div class="panel">
    <div class="panel-title">📩 Email Security Scanner</div>
    <div class="panel-sub">
        Şübhəli e-poçtun mətnini daxil et və təhlükə analizinə başla.
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
    "🔍  EMAIL-I ANALİZ ET",
    type="primary",
    use_container_width=True
)

# ANALYSIS
if scan:
    if not email_text.strip():
        st.warning("Zəhmət olmasa, əvvəlcə email mətnini daxil et.")
    else:
        email_vector = tfidf.transform([email_text])
        class_index = list(model.classes_).index(1)
        probability = model.predict_proba(email_vector)[0][class_index]

        st.markdown("---")
        st.markdown("## 📊 Analiz nəticəsi")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Phishing ehtimalı", f"{probability:.2%}")

        with col2:
            st.metric(
                "Risk statusu",
                "YÜKSƏK RİSK" if probability >= threshold
                else "AŞAĞI RİSK"
            )

        st.progress(float(probability))

        if probability >= threshold:
            st.error(
                "🚨 Potensial phishing aşkarlandı!"
            )
            st.markdown("""
            **🛡️ Təhlükəsizlik tövsiyələri**
            - Şübhəli linklərə klikləmə.
            - Şifrə və şəxsi məlumatlarını daxil etmə.
            - Göndərənin kimliyini ayrıca yoxla.
            """)
        else:
            st.success(
                "✅ Email seçilmiş həddə görə phishing "
                "kimi işarələnmədi."
            )
            st.warning(
                "Bu nəticə email-in tam təhlükəsiz olduğunu sübut etmir."
            )

        with st.expander("🔬 Analiz necə aparıldı?"):
            st.write(
                "1. Email mətni TF-IDF ilə rəqəmsal "
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
                "Ehtimal modelin qiymətləndirməsidir; "
                "tam təhlükəsizlik zəmanəti deyil."
            )

# FEATURES
st.markdown("---")
st.markdown("## ✨ Platformanın imkanları")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 🧠 AI Analysis")
    st.caption("E-poçt mətninin avtomatik təsnifatı.")

with c2:
    st.markdown("### ⚡ Fast Detection")
    st.caption("Daxil edilən mətnin sürətli analizi.")

with c3:
    st.markdown("### 🎚️ Flexible Settings")
    st.caption("Xəbərdarlıq həddini dəyişmək imkanı.")

st.markdown("""
<div class="footer">
    🛡️ PhishGuard AI · Educational Cybersecurity Project<br><br>
    AI əsaslı phishing aşkarlama prototipi · Nəticələr zəmanət deyil
</div>
""", unsafe_allow_html=True)
