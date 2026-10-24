    st.markdown("""
    <style>
    .model-info {
        background: #142238;
        border: 1px solid #344967;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
    }

    .model-info-title {
        color: #55E6FF !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        margin-bottom: 18px;
    }

    .model-label {
        color: #C5D4E8 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
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
    }
    </style>

    <div class="model-info">
        <div class="model-info-title">
            🤖 MODEL INTELLIGENCE
        </div>

        <div class="model-label">ALGORITHM</div>
        <div class="model-value">Logistic Regression</div>

        <div class="model-label">TEXT VECTORIZATION</div>
        <div class="model-value">TF-IDF</div>

        <div class="model-label">TEST ACCURACY</div>
        <div class="model-value">98.39%</div>
    </div>
    """, unsafe_allow_html=True)
