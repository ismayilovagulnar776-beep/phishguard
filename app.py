
import streamlit as st
import joblib

st.set_page_config(
    page_title="PhishGuard AI",
    page_icon="🛡️",
    layout="wide"
)

# Load trained model
data = joblib.load("phishing_model.joblib")
model = data["model"]
tfidf = data["tfidf"]

# Design
st.markdown("""
<style>
.stApp {
    background-color: #08111F;
    color: #F1F5F9;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #F8FAFC !important;
}

p, label, span, div {
    font-family: Arial, sans-serif;
}

p {
    color: #D5DEEA;
}

.hero {
    background: #101E30;
    border: 1px solid #263D54;
    border-left: 5px solid #00E5A0;
    border-radius: 12px;
    padding: 28px;
    margin-bottom: 24px;
}

.hero h1 {
    font-size: 38px;
    margin-bottom: 10px;
}

.hero p {
    font-size: 16px;
    line-height: 1.7;
    color: #D5DEEA;
}

.info-card {
    background: #101E30;
    border: 1px solid #263D54;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 12px;
}

.info-card h3 {
    color: #00E5A0 !important;
    font-size: 17px;
    margin-bottom: 12px;
}

.info-card p {
    color: #F1F5F9 !important;
    font-size: 15px;
    line-height: 1.8;
}

div[data-testid="stTextArea"] textarea {
    background-color: #0D1929 !important;
    color: #FFFFFF !important;
    border: 1px solid #3A536B !important;
    border-radius: 9px !important;
    font-size: 16px !important;
}

div[data-testid="stTextArea"] textarea::placeholder {
    color: #A8B6C8 !important;
}

.stButton > button {
    background-color: #00D995 !important;
    color: #06111D !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: bold !important;
    min-height: 45px;
    width: 100%;
}

.stButton > button:hover {
    background-color: #42F5B2 !important;
}

div[data-testid="stAlert"] {
    border-radius: 10px;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🛡️ PhishGuard AI")
    st.caption("EMAIL SECURITY SYSTEM")
    st.divider()

    st.markdown("### 🧠 Model Intelligence")

    st.markdown("""
    <div class="info-card">
        <h3>Algorithm</h3>
        <p>Logistic Regression</p>
        <h3>Text Vectorization</h3>
        <p>TF-IDF</p>
        <h3>Test Accuracy</h3>
        <p>98.39%</p>
    </div>
    """, unsafe_allow_html=True)

    threshold = st.slider(
        "Detection threshold",
        min_value=0.10,
        max_value=0.90,
        value=0.35,
        step=0.05
    )

    st.caption(
        "Lower threshold detects more potential phishing "
        "but may flag more legitimate emails."
    )

# Main page
st.markdown("""
<div class="hero">
    <h1>🛡️ PhishGuard AI</h1>
    <p>
        Detect threats. Defend your inbox.<br>
        Analyze suspicious email text using machine learning.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <h3>🔍 Threat Detection</h3>
        <p>Identify suspicious email messages with AI.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h3>🧠 Machine Learning</h3>
        <p>Text analysis powered by TF-IDF and Logistic Regression.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <h3>🔐 Email Protection</h3>
        <p>Get a risk assessment and recommended next steps.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.markdown("## 📩 Email Threat Scanner")
st.write("Paste the email text below to check for possible phishing.")

email_text = st.text_area(
    "Email content",
    height=200,
    placeholder=(
        "Example: Your account has been suspended. "
        "Click here immediately to verify your password..."
    ),
    label_visibility="collapsed"
)

if st.button("🔍 ANALYZE EMAIL"):
    if not email_text.strip():
        st.warning("Please enter an email message first.")
    else:
        email_vector = tfidf.transform([email_text])
        probabilities = model.predict_proba(email_vector)[0]

        phishing_index = list(model.classes_).index(1)
        phishing_probability = float(probabilities[phishing_index])

        st.markdown("## Analysis Result")

        st.metric(
            "Estimated phishing probability",
            f"{phishing_probability * 100:.2f}%"
        )

        if phishing_probability >= threshold:
            st.error("⚠️ Potential Phishing Detected")
            st.write(
                "This message has suspicious characteristics. "
                "Do not click links or share passwords until "
                "you verify the sender independently."
            )
        else:
            st.success("✅ Likely Legitimate Email")
            st.write(
                "The model did not flag this message as phishing. "
                "This does not guarantee that the email is safe."
            )

        st.progress(phishing_probability)

        st.caption(
            "Note: This tool analyzes email text only. "
            "It does not independently verify the sender, URLs, "
            "or attachments."
        )

st.divider()

st.markdown("""
<div style="text-align:center; padding:15px; color:#A8B6C8;">
    <p>PHISHGUARD AI · CYBERSECURITY PROJECT</p>
    <p>Machine Learning for Email Threat Detection</p>
</div>
""", unsafe_allow_html=True)
