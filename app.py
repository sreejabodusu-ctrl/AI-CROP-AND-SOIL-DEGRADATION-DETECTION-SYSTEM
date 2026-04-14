import streamlit as st
from PIL import Image
from model import get_model_status, predict_with_scores
from recommendations import get_solution
from utils import preprocess_image
st.set_page_config(
    page_title="AL Crop AI Console",
    page_icon="🌾",
    layout="wide"
)
apply_app_styles()
model_status = get_model_status()
render_hero()
render_model_warnings(model_status)
left_col, right_col = st.columns([1.1, 1.3], gap="large")
with left_col:
    st.subheader("Upload Image")
    uploaded_file = st.file_uploader(
        "Accepted formats: JPG, JPEG, PNG",
        type=["jpg", "jpeg", "png"]
    )
    if uploaded_file is not None:
        preview_image = Image.open(uploaded_file).convert("RGB")
        st.image(preview_image, caption="Image Preview", use_container_width=True)
    else:
        st.info("Choose an image to start diagnosis.")
with right_col:
    st.subheader("Diagnosis Output")
    if uploaded_file is None:
        render_result_placeholder()
    elif not model_status["ready"]:
        st.info("Image uploaded. Prediction will run once model files load successfully.")
    else:
        try:
            with st.spinner("Analyzing crop condition..."):
                img = Image.open(uploaded_file).convert("RGB")
                processed_img = preprocess_image(img)
                result = predict_with_scores(processed_img, top_k=3)
            prediction = result["label"]
            confidence = result["confidence"] * 100
            solution = get_solution(prediction)
            st.success(f"Detected: {prediction}")
            st.progress(min(max(result["confidence"], 0.0), 1.0))
            st.caption(f"Confidence: {confidence:.2f}%")
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("### Top Predictions")
            for idx, item in enumerate(result["top_predictions"], start=1):
                st.write(f"{idx}. {item['label']} - {item['confidence'] * 100:.2f}%")
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("### Control Measures")
            st.write(solution["control"])
            st.markdown("### Prevention Methods")
            st.write(solution["prevention"])
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as exc:
            st.error(f"Unable to process this image: {exc}")
