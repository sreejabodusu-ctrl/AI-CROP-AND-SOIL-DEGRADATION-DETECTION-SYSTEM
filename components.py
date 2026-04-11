import streamlit as st


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero">
            <h1>AI Crop Pest and Soil Condition Detection</h1>
            <p>Upload a crop image to classify pest or soil issues and get practical field recommendations instantly.</p>
            <div class="chip-row">
                <span class="chip">Multi-class diagnosis</span>
                <span class="chip">Top-3 confidence scores</span>
                <span class="chip">Actionable control guidance</span>
            </div>
        </div>
        <div class="frontend-tag">Frontend Build: v2-green-panel</div>
        """,
        unsafe_allow_html=True
    )


def render_model_warnings(model_status: dict) -> None:
    if model_status["ready"]:
        return

    st.warning(
        "Inference is blocked until both model files are available. "
        f"Weights path: {model_status['weights_path']} | "
        f"Class mapping path: {model_status['label_mapping_path']}"
    )
    if model_status.get("load_error"):
        st.error(model_status["load_error"])


def render_result_placeholder() -> None:
    st.markdown(
        '<div class="result-card">Prediction details will appear here after upload.</div>',
        unsafe_allow_html=True
    )
