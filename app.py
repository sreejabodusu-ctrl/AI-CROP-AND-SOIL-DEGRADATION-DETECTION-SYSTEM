import streamlit as st
from PIL import Image
from utils import preprocess_image
from model import get_model_status, predict_image
from recommendations import get_solution

# Page config (ONLY ONCE)
st.set_page_config(page_title="AI Crop Detection", layout="wide")

# =========================
# Theme Toggle
# =========================
theme = st.sidebar.selectbox("Theme", ["Dark", "Light"])

if theme == "Dark":
    background = "#0e1117"
    text_color = "white"
    box_color = "#1e1e1e"
else:
    background = "#f5f7fa"
    text_color = "black"
    box_color = "#ffffff"

# =========================
# Custom CSS
# =========================
st.markdown(f"""
<style>

/* Page */
body {{
    background-color: {background};
    color: {text_color};
}}

/* Banner */
.banner {{
    background: linear-gradient(to right, #2e7d32, #66bb6a);
    padding: 30px;
    border-radius: 15px;
    color: white;
    margin-bottom: 30px;
}}

/* Upload Box */
.upload-box {{
    background-color: {box_color};
    padding: 25px;
    border-radius: 12px;
    border: 1px solid #333;
}}

/* Output Box */
.output-box {{
    background-color: {box_color};
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #ccc;
}}

/* Section Title */
.section-title {{
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 10px;
}}

/* Hide default uploader label */
div[data-testid="stFileUploader"] > label {{
    display: none;
}}

/* Style uploader */
div[data-testid="stFileUploader"] {{
    background-color: {box_color};
    padding: 20px;
    border-radius: 10px;
    border: 1px dashed #888;
}}

/* Center uploader content */
div[data-testid="stFileUploader"] section {{
    text-align: center;
}}

</style>
""", unsafe_allow_html=True)

# =========================
# Header
# =========================
st.markdown("""
<div class="banner">
    <h1>AI Crop Pest and Soil Condition Detection</h1>
    <p>Upload a crop image to classify pest or soil issues and get practical recommendations instantly.</p>
</div>
""", unsafe_allow_html=True)

# =========================
# Model Status Check
# =========================
model_status = get_model_status()

if not model_status['ready']:
    st.warning(
        "Model is not ready for inference. "
        f"Weights loaded: {model_status['weights_loaded']} "
        f"(path: {model_status['weights_path']}), "
        f"class mapping loaded: {model_status['class_mapping_loaded']} "
        f"(path: {model_status['label_mapping_path']})."
    )
    if model_status.get('load_error'):
        st.error(model_status['load_error'])

# =========================
# Layout
# =========================
col1, col2 = st.columns(2)

# =========================
# Upload Section
# =========================
with col1:
    st.markdown('<div class="section-title">Upload Image</div>', unsafe_allow_html=True)

    st.markdown('<div class="upload-box">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Output Section
# =========================
with col2:
    st.markdown('<div class="section-title">Diagnosis Output</div>', unsafe_allow_html=True)

    st.markdown('<div class="output-box">', unsafe_allow_html=True)

    if uploaded_file and model_status['ready']:
        image = Image.open(uploaded_file)

        st.image(image, caption="Uploaded Image", use_column_width=True)

        with st.spinner("Processing image..."):
            processed_img = preprocess_image(image)
            prediction = predict_image(processed_img)
            solution = get_solution(prediction)

        st.subheader(f"Prediction: {prediction}")

        st.subheader("Control Measures")
        st.write(solution['control'])

        st.subheader("Prevention Methods")
        st.write(solution['prevention'])

    elif uploaded_file and not model_status['ready']:
        st.info("Model not ready. Please check model files.")

    else:
        st.info("Upload an image to see results")

    st.markdown('</div>', unsafe_allow_html=True)
