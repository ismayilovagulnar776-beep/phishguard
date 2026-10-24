
import streamlit as st
import joblib

st.set_page_config(
    page_title="PhishGuard AI",
    page_icon="🛡️",
    layout="centered"
)

@st.cache_resource
def load_model():
    data = joblib.load("phishing_model.joblib")
    return data["model"], data["tfidf"]

model, tfidf = load_model()

st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}
.block-container {
    max-width: 850px;
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ PhishGuard AI")
st.caption("AI-Based Phishing Email Detection System")

st.info(
    "Email mətnini daxil et. Model onun phishing ola "
    "bilməsi ehtimalını qiymətləndirəcək."
)

st.markdown("### 📩 Email yoxlayıcısı")

email_text = st.text_area(
    "Email məzmunu",
    value=(
        "Your account will be suspended. "
        "Click here to verify your password immediately."
    ),
    height=180,
    placeholder="Email mətnini bura yapışdır..."
)

threshold = st.sidebar.slider(
    "Phishing xəbərdarlıq həddi",
    min_value=0.10,
    max_value=0.90,
    value=0.35,
    step=0.05
)

st.sidebar.markdown("### 🤖 Model haqqında")
st.sidebar.write("Alqoritm: Logistic Regression")
st.sidebar.write("Mətn emalı: TF-IDF")
st.sidebar.write("Qərar həddi dəyişdirilə bilər.")

if st.button("🔍 Email-i yoxla", type="primary",
             use_container_width=True):

    if not email_text.strip():
        st.warning("Zəhmət olmasa, email mətnini daxil et.")
    else:
        email_vector = tfidf.transform([email_text])

        # Modelin 1-ci sinfə (phishing) aid ehtimalı
        class_index = list(model.classes_).index(1)
        probability = model.predict_proba(email_vector)[0][class_index]

        st.markdown("---")
        st.subheader("📊 Təhlilin nəticəsi")

        st.metric(
            "Phishing ehtimalı",
            f"{probability:.2%}"
        )
        st.progress(float(probability))

        if probability >= threshold:
            st.error(
                "⚠️ Model bu email-i phishing kimi təsnif etdi."
            )
            st.write(
                "Linklərə klikləməzdən və şəxsi məlumatlarını "
                "daxil etməzdən əvvəl göndərəni müstəqil yoxla."
            )
        else:
            st.warning(
                "Model bu email-i seçilmiş həddə görə "
                "phishing kimi işarələmədi."
            )
            st.write(
                "Bu nəticə email-in təhlükəsiz olduğunu sübut etmir."
            )

        with st.expander("Bu nəticə necə hesablandı?"):
            st.write(
                "1. Email mətni TF-IDF ilə rəqəmsal xüsusiyyətlərə "
                "çevrildi."
            )
            st.write(
                "2. Logistic Regression modeli phishing ehtimalını "
                "hesabladı."
            )
            st.write(
                f"3. Ehtimal {threshold:.0%} həddi ilə müqayisə edildi."
            )

st.markdown("---")
st.caption(
    "Tədris məqsədli prototipdir. Nəticələr zəmanət deyil; "
    "bu vasitə real email təhlükəsizliyi sistemini əvəz etmir."
)
