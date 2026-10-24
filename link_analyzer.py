"""
link_analyzer.py - PhishGuard AI üçün link, domen və qoşma yoxlaması.

Yalnız Python standart kitabxanasından istifadə edir, ona görə
requirements.txt faylına yeni paket əlavə etmək lazım deyil.

Əsas funksiyalar:
    analyze_email(text)                 -> ətraflı təhlil nəticəsi (dict)
    combined_probability(p_model, res)  -> modelin ehtimalı + link/domen riski
    render_report(st, res)              -> Streamlit-də ətraflı hesabat
"""

import ipaddress
import re
from urllib.parse import parse_qs, urlparse

# --------------------------------------------------------------------------
# Sabitlər
# --------------------------------------------------------------------------
URL_RE = re.compile(r"""(?i)\b((?:https?://|www\.)[^\s<>"'()\[\]]+)""")
EMAIL_RE = re.compile(r"([A-Za-z0-9._%+\-]+)@([A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,})")
FROM_RE = re.compile(r"(?im)^\s*from\s*:\s*(.+)$")
FILE_RE = re.compile(
    r"(?i)(?<![\w@/.\-])([\w\-]+(?:\.[\w\-]+)*\.(?:exe|scr|bat|cmd|js|vbs|jar|msi|lnk|"
    r"docm|xlsm|pptm|iso|img|zip|rar|7z|html|htm|pdf))\b"
)

SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd", "buff.ly",
    "rebrand.ly", "cutt.ly", "shorturl.at", "tiny.cc", "rb.gy",
}
SUSPICIOUS_TLDS = {
    "zip", "mov", "xyz", "top", "click", "link", "work", "support", "country",
    "gq", "tk", "ml", "ga", "cf", "icu", "rest", "monster", "buzz", "cam",
    "loan", "men", "date",
}
FREE_MAIL = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "mail.ru",
    "yandex.ru", "icloud.com", "proton.me", "protonmail.com",
}
BRANDS = {
    "paypal": "paypal.com",
    "google": "google.com",
    "microsoft": "microsoft.com",
    "apple": "apple.com",
    "amazon": "amazon.com",
    "facebook": "facebook.com",
    "instagram": "instagram.com",
    "netflix": "netflix.com",
    "linkedin": "linkedin.com",
    "dhl": "dhl.com",
    "fedex": "fedex.com",
    "kapitalbank": "kapitalbank.az",
    "pashabank": "pashabank.az",
}
SECOND_LEVEL = {"co", "com", "org", "net", "gov", "edu", "ac"}
LEET = str.maketrans({"0": "o", "1": "l", "3": "e", "5": "s", "$": "s", "@": "a"})
SENSITIVE_WORDS = (
    "login", "signin", "verify", "secure", "account", "update", "confirm",
    "password", "billing", "wallet", "bank", "suspend", "unlock",
)
EXEC_EXT = {"exe", "scr", "bat", "cmd", "js", "vbs", "jar", "msi", "lnk"}
MACRO_EXT = {"docm", "xlsm", "pptm"}
CONTAINER_EXT = {"zip", "rar", "7z", "iso", "img"}
WEB_EXT = {"html", "htm"}
DOC_EXT = {"pdf", "doc", "docx", "xls", "xlsx", "jpg", "jpeg", "png", "txt"}

WEIGHTS = {"Yüksək": 40, "Orta": 20, "Aşağı": 8}
ICONS = {"Yüksək": "🔴", "Orta": "🟠", "Aşağı": "🟡"}


# --------------------------------------------------------------------------
# Köməkçi funksiyalar
# --------------------------------------------------------------------------
def _f(severity, title, detail):
    return {"severity": severity, "title": title, "detail": detail}


def registered_domain(host):
    """Sadə üsulla əsas domeni tapır (sub.example.com -> example.com)."""
    labels = host.split(".")
    if len(labels) <= 2:
        return host
    if len(labels[-1]) == 2 and labels[-2] in SECOND_LEVEL:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


def levenshtein(a, b):
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _score(findings):
    return min(100, sum(WEIGHTS[x["severity"]] for x in findings))


def _level(score):
    if score >= 50:
        return "Yüksək"
    if score >= 20:
        return "Orta"
    return "Aşağı"


def _host_checks(host):
    """Host (domen) üçün ümumi yoxlamalar: link və göndərən üçün istifadə olunur."""
    findings = []
    reg = registered_domain(host)
    tld = host.rsplit(".", 1)[-1]

    # IP ünvanı
    try:
        ipaddress.ip_address(host)
        findings.append(_f("Yüksək", "Domen əvəzinə IP ünvanı",
                           "Real şirkətlər linklərdə nadir hallarda çılpaq IP istifadə edir."))
        return findings, host
    except ValueError:
        pass

    # Punycode və qeyri-ASCII simvollar
    if "xn--" in host or any(ord(c) > 127 for c in host):
        findings.append(_f("Yüksək", "Oxşar simvollu (homoqraf) domen",
                           "Domendə kiril/xüsusi simvollar və ya punycode var; adi hərflərə bənzədilib."))

    # Şübhəli TLD
    if tld in SUSPICIOUS_TLDS:
        findings.append(_f("Orta", f"Şübhəli domen sonluğu (.{tld})",
                           "Bu sonluq fişinq və spam kampaniyalarında tez-tez istifadə olunur."))

    # Çox subdomen
    sub_count = len(host.split(".")) - len(reg.split("."))
    if sub_count >= 3:
        findings.append(_f("Orta", "Həddindən artıq subdomen",
                           f"{sub_count} subdomen var; əsl domen ({reg}) gizlədilə bilər."))

    # Tire sayı
    if host.count("-") >= 3:
        findings.append(_f("Aşağı", "Domendə çoxlu tire",
                           "Saxta domenlər tez-tez 'secure-login-update-xxx' formasında olur."))

    # Brend təqlidi
    tokens = re.split(r"[.\-]", host)
    sld = reg.split(".")[0]
    for brand, official in BRANDS.items():
        if reg == official:
            continue
        for tok in tokens:
            norm = tok.translate(LEET)
            if tok == brand:
                findings.append(_f("Yüksək", f"Brend təqlidi: {brand}",
                                   f"Domendə '{brand}' sözü var, amma rəsmi domen {official}-dir. Əsl domen: {reg}."))
                break
            if norm == brand:
                findings.append(_f("Yüksək", f"Simvol əvəzləməsi ilə brend təqlidi: {brand}",
                                   f"'{tok}' sözü '{brand}' sözünü rəqəm/simvol əvəzləməsi ilə təqlid edir."))
                break
        else:
            d = levenshtein(sld.translate(LEET), brand)
            if d == 1 or (d == 2 and len(brand) >= 7):
                findings.append(_f("Yüksək", f"Yazılışı dəyişdirilmiş brend: {brand}",
                                   f"'{sld}' domeni '{brand}' brendinə çox bənzəyir (typosquatting)."))
    return findings, reg


# --------------------------------------------------------------------------
# Link təhlili
# --------------------------------------------------------------------------
def analyze_url(raw_url):
    url = raw_url.rstrip(".,;:!?")
    parsed = urlparse(url if "://" in url else "http://" + url)
    host = (parsed.hostname or "").lower()
    findings = []

    if not host:
        return {"url": url, "host": "", "domain": "", "findings": [], "score": 0, "level": "Aşağı"}

    host_findings, reg = _host_checks(host)
    findings.extend(host_findings)

    if not url.lower().startswith("https://"):
        findings.append(_f("Orta", "Təhlükəsiz olmayan bağlantı (HTTPS yoxdur)",
                           "Link şifrələnməyib; həssas məlumat daxil etməyin."))

    if "@" in (parsed.netloc or ""):
        findings.append(_f("Yüksək", "Linkdə '@' işarəsi",
                           "'@'-dən əvvəlki hissə istifadəçi adı sayılır, əsl ünvan isə sonradan gəlir; aldatma üsuludur."))

    if host in SHORTENERS or reg in SHORTENERS:
        findings.append(_f("Orta", "Qısaldılmış link",
                           f"{reg} qısaldıcısı əsl təyinat ünvanını gizlədir."))

    if parsed.port and parsed.port not in (80, 443):
        findings.append(_f("Orta", f"Qeyri-standart port ({parsed.port})",
                           "Adi saytlar nadir hallarda qeyri-standart portdan istifadə edir."))

    if len(url) > 100:
        findings.append(_f("Aşağı", "Çox uzun link",
                           f"Link {len(url)} simvoldur; uzun linklər şübhəli hissələri gizlədə bilər."))

    # Yönləndirmə parametri
    query = parse_qs(parsed.query)
    for key, values in query.items():
        if any(v.lower().startswith(("http://", "https://")) for v in values):
            findings.append(_f("Orta", "Linkin içində başqa link (yönləndirmə)",
                               f"'{key}' parametri başqa ünvana yönləndirir."))
            break

    # Həssas sözlər (yalnız brend və ya digər xəbərdarlıqlarla birlikdə daha ciddi)
    path_text = (parsed.path + " " + parsed.query).lower()
    hits = [w for w in SENSITIVE_WORDS if w in path_text or w in host]
    if hits and findings:
        findings.append(_f("Aşağı", "Həssas sözlər: " + ", ".join(hits[:4]),
                           "Giriş/təsdiq/hesab kimi sözlər istifadəçini məlumat verməyə yönəldir."))

    score = _score(findings)
    return {"url": url, "host": host, "domain": reg, "findings": findings,
            "score": score, "level": _level(score)}


# --------------------------------------------------------------------------
# Göndərən təhlili
# --------------------------------------------------------------------------
def analyze_sender(text):
    m = FROM_RE.search(text)
    if not m:
        return None
    line = m.group(1).strip()
    em = EMAIL_RE.search(line)
    if not em:
        return None

    address = em.group(0)
    domain = em.group(2).lower()
    display = line[:em.start()].strip(" <\"'")
    findings, reg = _host_checks(domain)

    low = display.lower()
    for brand, official in BRANDS.items():
        if brand in low and reg != official:
            findings.append(_f("Yüksək", f"Göndərən adı '{brand}' göstərir, domen uyğun deyil",
                               f"Görünən ad '{display}', real domen isə {reg}. Rəsmi domen {official} olmalıdır."))
            break

    if reg in FREE_MAIL and display and any(w in low for w in ("bank", "support", "security", "admin", "team")):
        findings.append(_f("Orta", "Rəsmi görünən ad, pulsuz e-poçt xidməti",
                           f"Rəsmi təşkilat adı ilə {reg} ünvanından yazılıb."))

    score = _score(findings)
    return {"address": address, "display": display, "domain": reg,
            "findings": findings, "score": score, "level": _level(score)}


# --------------------------------------------------------------------------
# Qoşma təhlili (mətndə adı çəkilən fayllar)
# --------------------------------------------------------------------------
def analyze_attachments(text):
    # Linklərin içindəki fayl adları qoşma sayılmasın
    cleaned = URL_RE.sub(" ", text)
    results, seen = [], set()
    for m in FILE_RE.finditer(cleaned):
        name = m.group(1)
        if name.lower() in seen:
            continue
        seen.add(name.lower())
        parts = name.lower().split(".")
        ext = parts[-1]
        findings = []
        if len(parts) >= 3 and parts[-2] in DOC_EXT and ext in EXEC_EXT:
            findings.append(_f("Yüksək", "İkiqat uzantı",
                               f"'{name}' sənəd kimi görünür, əslində icra olunan fayldır (.{ext})."))
        elif ext in EXEC_EXT:
            findings.append(_f("Yüksək", f"İcra olunan fayl (.{ext})",
                               "Bu tip fayl açılanda kompüterdə proqram işə sala bilər."))
        elif ext in MACRO_EXT:
            findings.append(_f("Orta", f"Makro dəstəkli sənəd (.{ext})",
                               "Makrolar zərərli kod çalışdırmaq üçün istifadə olunur."))
        elif ext in CONTAINER_EXT:
            findings.append(_f("Orta", f"Arxiv/disk faylı (.{ext})",
                               "Arxivlər içindəki zərərli faylı gizlətmək üçün istifadə olunur."))
        elif ext in WEB_EXT:
            findings.append(_f("Orta", f"HTML qoşma (.{ext})",
                               "Saxta giriş səhifələri çox vaxt HTML qoşma kimi göndərilir."))
        elif ext == "pdf":
            findings.append(_f("Aşağı", "PDF qoşma",
                               "PDF-in içində zərərli link ola bilər; açmazdan əvvəl göndərəni yoxlayın."))
        score = _score(findings)
        results.append({"name": name, "ext": ext, "findings": findings,
                        "score": score, "level": _level(score)})
    return results


# --------------------------------------------------------------------------
# Əsas funksiya
# --------------------------------------------------------------------------
def analyze_email(text):
    urls, seen = [], set()
    for m in URL_RE.finditer(text):
        item = analyze_url(m.group(1))
        if item["url"] not in seen:
            seen.add(item["url"])
            urls.append(item)

    sender = analyze_sender(text)
    attachments = analyze_attachments(text)

    scores = [u["score"] for u in urls] + [a["score"] for a in attachments]
    if sender:
        scores.append(sender["score"])

    if scores:
        flagged = sum(1 for s in scores if s > 0)
        total = min(100, max(scores) + 10 * max(0, flagged - 1))
    else:
        total = 0
    level = _level(total)

    if not scores:
        summary = "Mətndə link, göndərən domeni və ya qoşma adı tapılmadı; bu hissələr üzrə risk qiymətləndirilmədi."
    elif total == 0:
        summary = "Tapılan link, domen və qoşmalarda şübhəli əlamət aşkarlanmadı."
    else:
        n_find = (sum(len(u["findings"]) for u in urls)
                  + sum(len(a["findings"]) for a in attachments)
                  + (len(sender["findings"]) if sender else 0))
        summary = f"{n_find} şübhəli əlamət tapıldı. Link/domen/qoşma risk səviyyəsi: {level} ({total}/100)."

    return {"urls": urls, "sender": sender, "attachments": attachments,
            "score": total, "level": level, "summary": summary}


def combined_probability(model_proba, result):
    """Modelin mətn ehtimalını link/domen/qoşma riski ilə birləşdirir (0..1)."""
    s = result["score"] / 100
    return 1 - (1 - model_proba) * (1 - 0.9 * s)


# --------------------------------------------------------------------------
# Streamlit hesabatı
# --------------------------------------------------------------------------
def _render_findings(st, findings):
    if not findings:
        st.markdown("✅ Şübhəli əlamət tapılmadı.")
        return
    for f in findings:
        st.markdown(f"- {ICONS[f['severity']]} **{f['title']}** ({f['severity']}): {f['detail']}")


def render_report(st, result):
    st.markdown("### 🔍 Link, domen və qoşma təhlili")

    c1, c2, c3 = st.columns(3)
    c1.metric("Tapılan linklər", len(result["urls"]))
    c2.metric("Göndərən domeni", result["sender"]["domain"] if result["sender"] else "tapılmadı")
    c3.metric("Qoşma adları", len(result["attachments"]))

    st.progress(result["score"] / 100)
    st.caption(f"{ICONS[result['level']]} {result['summary']}")

    if result["sender"]:
        s = result["sender"]
        with st.expander(f"{ICONS[s['level']]} Göndərən: {s['address']}", expanded=s["score"] > 0):
            _render_findings(st, s["findings"])

    for u in result["urls"]:
        label = u["url"] if len(u["url"]) <= 70 else u["url"][:67] + "..."
        with st.expander(f"{ICONS[u['level']]} Link: {label}", expanded=u["score"] > 0):
            st.markdown(f"**Domen:** `{u['domain']}`")
            _render_findings(st, u["findings"])

    for a in result["attachments"]:
        with st.expander(f"{ICONS[a['level']]} Qoşma: {a['name']}", expanded=a["score"] > 0):
            _render_findings(st, a["findings"])

    st.caption("Qeyd: yoxlama linkə daxil olmadan, yalnız mətndəki ünvanın quruluşuna əsaslanır. "
               "Qoşmalar yalnız mətndə adı çəkildikdə qiymətləndirilir.")


if __name__ == "__main__":
    demo = """From: PayPal Support <security@paypa1-secure.xyz>
Dear user, your account will be suspended.
Verify now: http://192.168.4.5:8080/login/verify?url=http://evil.ru
Or here: https://secure.paypal.com.account-update.top/signin
Short: https://bit.ly/3xYz
Open the invoice: invoice.pdf.exe and report.docm
"""
    import json
    print(json.dumps(analyze_email(demo), indent=2, ensure_ascii=False))
