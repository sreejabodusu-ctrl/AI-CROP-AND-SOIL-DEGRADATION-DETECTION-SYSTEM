import streamlit as st


APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Manrope:wght@400;600;700&display=swap');

:root {
    --bg-top: #f8fff3;
    --bg-bottom: #e7f4dc;
    --card: #ffffff;
    --text-main: #11251a;
    --text-muted: #3a5b47;
    --accent: #1f8f3b;
    --accent-2: #0f5d2d;
    --line: #d3e7d2;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 12% 8%, #ffffff 0%, rgba(255, 255, 255, 0.2) 32%, transparent 48%),
        linear-gradient(160deg, var(--bg-top) 0%, var(--bg-bottom) 100%);
    color: var(--text-main);
    font-family: 'Manrope', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    right: 1rem;
}

.block-container {
    max-width: 1200px;
    padding-top: 1.6rem;
    padding-bottom: 1.6rem;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
    color: var(--text-main);
    letter-spacing: 0.3px;
}

.hero {
    background: linear-gradient(130deg, #145f2e 0%, #1f8f3b 55%, #39a658 100%);
    color: #f8fff6;
    border-radius: 20px;
    padding: 30px 26px;
    box-shadow: 0 16px 36px rgba(14, 54, 27, 0.24);
    margin-bottom: 18px;
    border: 1px solid rgba(255, 255, 255, 0.25);
}

.hero h1 {
    color: #f8fff6;
    font-size: 2.1rem;
    margin-bottom: 0.4rem;
    text-transform: uppercase;
}

.hero p {
    margin: 0;
    max-width: 780px;
    color: #ecf8e8;
    font-size: 1.03rem;
}

.result-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 16px 18px;
    box-shadow: 0 10px 24px rgba(17, 37, 26, 0.08);
    margin-bottom: 12px;
}

.chip-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 14px;
}

.chip {
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.28);
    color: #f4ffef;
    border-radius: 999px;
    font-size: 0.85rem;
    padding: 6px 12px;
}

.frontend-tag {
    margin-top: 8px;
    color: #163a24;
    font-size: 0.82rem;
    font-weight: 700;
}

[data-testid="stFileUploaderDropzone"] {
    border: 2px dashed #98cfa1;
    border-radius: 16px;
    background: #f7fff4;
}

.stButton button, .stDownloadButton button {
    border-radius: 999px;
    border: 1px solid #2a8240;
    color: #ffffff;
    background: linear-gradient(180deg, #2f9b4a 0%, var(--accent) 100%);
}

@media (max-width: 840px) {
    .hero h1 {
        font-size: 1.6rem;
    }
}
</style>
"""


def apply_app_styles() -> None:
    st.markdown(APP_CSS, unsafe_allow_html=True)
