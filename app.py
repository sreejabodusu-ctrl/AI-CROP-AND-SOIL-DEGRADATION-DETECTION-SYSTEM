import streamlit as st
from PIL import Image
from utils import preprocess_image
from model import get_model_status, predict_image
from recommendations import get_solution
st.set_page_config(page_title="Crop AI System")

st.header("AI CROP PEST & SOIL DEGRADATION DETECTION SYSTEM")

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

uploaded_file = st.file_uploader("Upload Crop Image", type=["jpg", "png", "jpeg"])

if uploaded_file and model_status['ready']:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=700)

    processed_img = preprocess_image(image)
    prediction = predict_image(processed_img)
    solution = get_solution(prediction)

    st.subheader(f"Prediction: {prediction}")

    st.subheader("Control Measures")
    st.write(solution['control'])

    st.subheader("Prevention Methods")
    st.write(solution['prevention'])
elif uploaded_file and not model_status['ready']:
    st.info("Upload received, but prediction is blocked until model files are loaded successfully.")
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="AI Crop Detection",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>

/* Main background */
body {
    background-color: #f5f7fa;
}

/* Header banner */
.banner {
    background: linear-gradient(to right, #2e7d32, #66bb6a);
    padding: 30px;
    border-radius: 15px;
    color: white;
    margin-bottom: 30px;
}

/* Upload box */
.upload-box {
    background-color: #1e1e1e;
    padding: 20px;
    border-radius: 10px;
    color: white;
}

/* Output box */
.output-box {
    background-color: #f1f3f6;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #ddd;
}

/* Section titles */
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="banner">
    <h1>AI Crop Pest and Soil Condition Detection</h1>
    <p>Upload a crop image to classify pest or soil issues and get practical recommendations instantly.</p>
</div>
""", unsafe_allow_html=True)

# Layout
col1, col2 = st.columns(2)

# Upload Section
with col1:
    st.markdown('<div class="section-title">Upload Image</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Drag and drop or browse image",
        type=["jpg", "jpeg", "png"]
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-title">Diagnosis Output</div>', unsafe_allow_html=True)
    st.markdown('<div class="output-box">', unsafe_allow_html=True)
    
    if uploaded_file:
        st.success("Image uploaded successfully")
        
        # Display image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        # Replace this with your model output
        st.write("Prediction: Healthy Leaf")
        st.write("Confidence: 95%")
        st.write("Recommendation: No action needed")
    else:
        st.info("Upload an image to see results")
    
    st.markdown('</div>', unsafe_allow_html=True)
