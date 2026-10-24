import re
import ipaddress
from urllib.parse import urlparse

import joblib
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="PhishGuard AI | Cybersecurity",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# MODEL LOADING
# =========================================================
@st.cache_resource
def load_model():
    data = joblib.load("phishing_model.joblib")
    return data["model"], data["tfidf"]


try:
    model, tfidf = load_model()
    model_loaded = True
except Exception:
    model = None
    tfidf = None
    model_loaded = False


# =========================================================
# CYBERSECURITY DESIGN
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --background: #08111f;
    --surface: #101d30;
    --surface-light: #14253b;
    --border: #2a405a;
    --cyan: #55dcff;
    --green: #55e6a5;
    --white: #f4f7fc;
    --muted: #b5c3d6;
}

.stApp {
    background: var(--background);
    color: var(--white);
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #0c1728 !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: var(--white);
}

h1, h2, h3 {
    color: var(--white) !important;
    letter-spacing: -0.4px;
}

p, label, li {
    color: var(--muted);
    line-height: 1.75;
}

.brand {
    display: flex;
    align-items: center;
    gap: 13px;
    padding: 8px 0 22px 0;
}

.brand-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 49px;
    height: 49px;
    flex-shrink: 0;
    border-radius: 13px;
    background: #153750;
    border: 1px solid #34718b;
    font-size: 25px;
}

.brand-name {
    color: #ffffff;
    font-size: 23px;
    font-weight: 800;
}

.brand-caption {
    color: var(--cyan);
    font-size: 10px;
    letter-spacing: 2px;
    margin-top: 3px;
}

.status-pill {
    background: #12332f;
    border: 1px solid #286957;
    color: #8cf2c6;
    border-radius: 7px;
    padding: 9px 11px;
    font-size: 12px;
    margin: 8px 0 20px 0;
}

.hero {
    background: linear-gradient(115deg, #11243a, #10192c 72%);
    border: 1px solid #2b435e;
    border-left: 4px solid var(--cyan);
    border-radius: 16px;
    padding: 30px;
    margin: 15px 0 25px 0;
}

.eyebrow {
    color: var(--cyan);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2.4px;
}

.hero-title {
    font-size: clamp(31px, 4vw, 46px);
    font-weight: 800;
    line-height: 1.2;
    margin: 13px 0;
    color: #ffffff;
}

.hero-accent {
    color: var(--cyan);
}

.hero-description {
    max-width: 700px;
    color: #c5d2e3;
    font-size: 15px;
    line-height: 1.8;
}

.section-label {
    color: var(--cyan);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.8px;
    margin-bottom: 8px;
}

.info-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 17px;
    height: 100%;
}

.info-card-title {
    color: #ffffff;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 7px;
}

.info-card-text {
    color: #c1cfe0;
    font-size: 13px;
    line-height: 1.7;
}

.model-card {
    background: #101f32 !important;
    border: 1px solid #304760 !important;
    border-radius: 12px;
    padding: 15px;
    margin: 12px 0 18px 0;
}

.model-heading {
    color: var(--cyan) !important;
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 15px;
}

.model-label {
    color: #c5d3e5 !important;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.8px;
    margin-top: 13px;
    margin-bottom: 5px;
}

.model-value {
    color: #ffffff !important;
    background: #0a1525 !important;
    border: 1px solid #30445d !important;
    border-radius: 7px;
    padding: 9px 10px;
    font-size: 13px;
    font-weight: 600;
    overflow-wrap: anywhere;
}

.scanner-box {
    background: #101d30;
    border: 1px solid #2a405a;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 12px;
}

div[data-testid="stTextArea"] textarea {
    background: #0a1525 !important;
    color: #ffffff !important;
    border: 1px solid #3a526d !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
}

div[data-testid="stTextArea"] textarea::placeholder {
    color: #9fb0c6 !important;
    opacity: 1 !important;
}

.stButton > button {
    background: #087fa8 !important;
    color: #ffffff !important;
    border: 1px solid #39c5e8 !important;
    border-radius: 9px !important;
    min-height: 48px;
    font-weight: 800 !important;
}

.stButton > button:hover {
    background: #096a8d !important;
    border-color: #83eaff !important;
}

div[data-testid="stMetric"] {
    background: #101e31;
    border: 1px solid #304760;
    border-radius: 12px;
    padding: 17px;
}

div[data-testid="stMetricLabel"] {
    color: #c4d2e4 !important;
}

div[data-testid="stMetricValue"] {
    color: var(--cyan) !important;
}

div[data-testid="stAlert"] {
    border-radius: 10px;
}

.result-box {
    background: #101e31;
    border: 1px solid #304760;
    border-radius: 12px;
    padding: 20px;
    margin: 12px 0;
}

.result-safe {
    border-left: 4px solid #55e6a5;
}

.result-danger {
    border-left: 4px solid #ff6577;
}

.result-title {
    color: #ffffff;
    font-size: 19px;
    font-weight: 800;
    margin-bottom: 9px;
}

.result-text {
    color: #c6d3e4;
    font-size: 14px;
    line-height: 1.8;
}

.url-card {
    background: #0c192a;
    border: 1px solid #304760;
    border-radius: 9px;
    padding: 13px;
    margin: 9px 0;
    overflow-wrap: anywhere;
}

.url-address {
    color: #ffffff;
    font-size: 13px;
    font-weight: 600;
    overflow-wrap: anywhere;
}

.url-note {
    color: #c2d0e1;
    font-size: 12px;
    margin-top: 7px;
}

.footer {
    border-top: 1px solid #2a405a;
    margin-top: 35px;
    padding: 22px 0;
    text-align: center;
    color: #aebdd0;
    font-size: 12px;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem;
    }

    .hero {
        padding: 20px;
    }

    .hero-title {
        font-size: 30px;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# URL EXTRACTION AND HEURISTIC ANALYSIS
# =========================================================
URL_PATTERN = re.compile(
    r"""(?i)\b(?:(?:https?://)|(?:www\.))[^\s<>"']+"""
)

SHORTENER_DOMAINS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "is.gd",
    "cutt.ly",
    "rb.gy",
    "ow.ly",
    "buff.ly",
}

SUSPICIOUS_WORDS = {
    "login",
    "verify",
    "password",
    "secure",
    "account",
    "update",
    "wallet",
    "signin",
    "confirm",
    "suspended",
}


def extract_urls(text):
    """Extract URLs without opening or visiting them."""
    found = URL_PATTERN.findall(text)
    cleaned = []

    for item in found:
        url = item.rstrip(".,!?;:)]}")
        if url and url not in cleaned:
            cleaned.append(url)

    return cleaned


def inspect_url(raw_url):
    """Check URL structure using local heuristics only."""
    url = raw_url

    if url.lower().startswith("www."):
        url = "http://" + url

    try:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower().rstrip(".")
        reasons = []

        if not host:
            return {
                "suspicious": True,
                "reasons": ["Domen adı düzgün müəyyən edilmədi."],
            }

        try:
            ipaddress.ip_address(host)
            reasons.append("Domen əvəzinə birbaşa IP ünvanı istifadə olunur.")
        except ValueError:
            pass

        if "@" in parsed.netloc:
            reasons.append("URL daxilində istifadəçini çaşdıra bilən '@' işarəsi var.")

        if host.startswith("xn--") or ".xn--" in host:
            reasons.append("Domen Punycode formatından istifadə edir.")

        if host in SHORTENER_DOMAINS:
            reasons.append("Link qısaldıcı xidmətə aiddir; son ünvan gizli qala bilər.")

        if len(host) > 55:
            reasons.append("Domen adı qeyri-adi dərəcədə uzundur.")

        if host.count(".") >= 4:
            reasons.append("Domen çoxsaylı alt domenlərdən ibarətdir.")

        if parsed.port is not None and parsed.port not in (80, 443):
            reasons.append("URL standart olmayan portdan istifadə edir.")

        searchable = (host + " " + parsed.path + " " + parsed.query).lower()
        matched_words = sorted(
            word for word in SUSPICIOUS_WORDS if word in searchable
        )

        if len(matched_words) >= 2:
            reasons.append(
                "Giriş və ya hesab yoxlaması ilə bağlı sözlər var: "
                + ", ".join(matched_words)
                + "."
            )

        if parsed.scheme.lower() != "https":
            reasons.append("Link HTTPS istifadə etmir.")

        return {
            "suspicious": bool(reasons),
            "reasons": reasons,
        }

    except (ValueError, TypeError):
        return {
            "suspicious": True,
            "reasons": ["URL təhlil edilə bilmədi."],
        }


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🛡️</div>
        <div>
            <div class="brand-name">PhishGuard AI</div>
            <div class="brand-caption">EMAIL SECURITY SYSTEM</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if model_loaded:
        st.markdown(
            '<div class="status-pill">● MODEL LOADED</div>',
            unsafe_allow_html=True,
        )
    else:
        st.error("Model yüklənmədi. Model faylını yoxla.")

    st.markdown("### ⚙️ Analysis settings")

    threshold = st.slider(
        "Phishing xəbərdarlıq həddi",
        min_value=0.10,
        max_value=0.90,
        value=0.35,
        step=0.05,
        help="Aşağı hədd daha çox email-i şübhəli işarələyə bilər.",
    )

    st.markdown("---")

    st.markdown("""
    <div class="model-card">
        <div class="model-heading">🧠 MODEL INTELLIGENCE</div>

        <div class="model-label">ALGORITHM</div>
        <div class="model-value">Logistic Regression</div>

        <div class="model-label">TEXT VECTORIZATION</div>
        <div class="model-value">TF-IDF</div>

        <div class="model-label">TEST ACCURACY</div>
        <div class="model-value">98.39%</div>
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        "Tədris layihəsidir. Model nəticələri təhlükəsizlik zəmanəti deyil."
    )


# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero">
    <div class="eyebrow">CYBER DEFENSE • EMAIL PROTECTION</div>
    <div class="hero-title">
        Protect your inbox.<br>
        <span class="hero-accent">Detect phishing.</span>
    </div>
    <div class="hero-description">
        E-poçt mətnini analiz et, linklərdəki şübhəli əlamətləri yoxla
        və potensial phishing hücumlarına qarşı daha məlumatlı qərar ver.
    </div>
</div>
""", unsafe_allow_html=True)

# Feature cards
f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">🧠 AI Text Analysis</div>
        <div class="info-card-text">
            Machine learning vasitəsilə email mətninin təsnifatı.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">🔗 URL Inspection</div>
        <div class="info-card-text">
            Linklərin strukturunda potensial risk əlamətlərinin axtarışı.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">🛡️ Risk Awareness</div>
        <div class="info-card-text">
            Təhlükəsizlik xəbərdarlıqları və qorunma tövsiyələri.
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# EMAIL SCANNER
# =========================================================
st.markdown("")
st.markdown('<div class="section-label">THREAT ANALYSIS MODULE</div>',
            unsafe_allow_html=True)
st.markdown("## 📩 Email Security Scanner")
st.write(
    "Email mətnini aşağıya əlavə et. Sistem mətni və içindəki "
    "linkləri ayrı-ayrılıqda analiz edəcək."
)

email_text = st.text_area(
    "Email məzmunu",
    height=210,
    placeholder=(
        "Dear user, your account will be suspended. "
        "Click https://example.com to verify your password..."
    ),
    label_visibility="collapsed",
    key="email_input",
)

scan = st.button(
    "🔍  ANALYZE EMAIL",
    type="primary",
    use_container_width=True,
)


# =========================================================
# ANALYSIS RESULTS
# =========================================================
if scan:
    if not email_text.strip():
        st.warning("Zəhmət olmasa, analiz üçün email mətnini daxil et.")

    elif not model_loaded:
        st.error(
            "Model yüklənməyib. "
            "'phishing_model.joblib' faylının mövcudluğunu yoxla."
        )

    else:
        email_vector = tfidf.transform([email_text])
        classes = list(model.classes_)
        phishing_index = classes.index(1)
        probability = float(
            model.predict_proba(email_vector)[0][phishing_index]
        )

        urls = extract_urls(email_text)
        url_results = [
            {"url": url, **inspect_url(url)}
            for url in urls
        ]

        suspicious_urls = [
            item for item in url_results if item["suspicious"]
        ]

        high_risk = (
            probability >= threshold
            or len(suspicious_urls) > 0
        )

        st.markdown("---")
        st.markdown('<div class="section-label">SCAN RESULTS</div>',
                    unsafe_allow_html=True)
        st.markdown("## 📊 Analysis Report")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Model phishing score",
                f"{probability:.1%}",
            )

        with col2:
            st.metric(
                "Links found",
                len(urls),
            )

        with col3:
            st.metric(
                "Suspicious links",
                len(suspicious_urls),
            )

        st.progress(probability)

        if high_risk:
            st.markdown("""
            <div class="result-box result-danger">
                <div class="result-title">🚨 Potential Threat Detected</div>
                <div class="result-text">
                    Email model tərəfindən phishing kimi qiymətləndirilib
                    və ya ən azı bir linkdə şübhəli struktur əlaməti tapılıb.
                    Linki açmazdan əvvəl göndərəni ayrıca yoxla.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### 🛡️ Recommended actions")
            st.markdown("""
            - Şübhəli linkə klikləmə.
            - Link açıq olsa belə, parol və digər məxfi məlumatları daxil etmə.
            - Göndərəni əvvəlcədən məlum olan rəsmi əlaqə kanalı ilə yoxla.
            - Hesabın təhlükədə olduğu deyilirsə, saytı özün ayrıca açaraq yoxla.
            """)

        else:
            st.markdown("""
            <div class="result-box result-safe">
                <div class="result-title">✓ No Immediate Warning</div>
                <div class="result-text">
                    Modelin seçilmiş həddinə görə phishing xəbərdarlığı yaranmadı
                    və URL yoxlamasında məlum struktur əlamətləri tapılmadı.
                    Bu, email-in təhlükəsiz olduğunu sübut etmir.
                </div>
            </div>
            """, unsafe_allow_html=True)

        # URL report
        st.markdown("### 🔗 Link inspection")

        if not urls:
            st.info(
                "Email mətnində tanınan HTTP/HTTPS və ya www linki tapılmadı."
            )
        else:
            for item in url_results:
                if item["suspicious"]:
                    st.markdown(
                        f"""
                        <div class="url-card">
                            <div class="url-address">⚠️ {item["url"]}</div>
                            <div class="url-note">
                                Status: Şübhəli əlamətlər aşkarlandı
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    for reason in item["reasons"]:
                        st.markdown(f"- {reason}")

                else:
                    st.markdown(
                        f"""
                        <div class="url-card">
                            <div class="url-address">✓ {item["url"]}</div>
                            <div class="url-note">
                                Status: Bu yoxlamada məlum şübhəli struktur
                                əlaməti tapılmadı.
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        with st.expander("🔬 How was the decision made?"):
            st.write(
                f"**Model phishing score:** {probability:.2%}"
            )
            st.write(
                f"**Configured threshold:** {threshold:.0%}"
            )
            st.write(
                f"**Extracted links:** {len(urls)}"
            )
            st.write(
                f"**Links with heuristic warnings:** {len(suspicious_urls)}"
            )
            st.caption(
                "URL yoxlaması lokal qaydalara əsaslanır. Linklər açılmır, "
                "saytların reputasiyası və real vaxt təhlükəsizliyi yoxlanmır. "
                "Bu analiz bütün phishing hücumlarını müəyyən edə bilməz."
            )


# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
    🛡️ PHISHGUARD AI<br><br>
    Machine Learning • URL Heuristics • Cybersecurity Awareness<br><br>
    Educational prototype — not a replacement for a security gateway
</div>
""", unsafe_allow_html=True)
