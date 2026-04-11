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
