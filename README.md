# AL_CROP_SYSTEM

## Project Overview

This project is a crop pest and soil condition detection system built with TensorFlow and Streamlit.
It uses a MobileNetV2-based classifier to predict one of 8 categories from uploaded crop images.

## Folder Structure

- `app.py` — Streamlit application for image upload and prediction display
- `model.py` — inference model definition and prediction helper
- `train.py` — model training pipeline
- `utils.py` — image preprocessing functions
- `recommendations.py` — prediction-based advice mapping
- `requirements.txt` — project dependencies

## Required Dataset Layout

Create the dataset folders as follows:

```
AL_CROP_SYSTEM/
  data/
    train/
      Healthy/
      Aphids/
      Whiteflies/
      Caterpillars/
      Beetles/
      Mites/
      Soil Degradation/
      Low Soil Moisture/
    valid/
      Healthy/
      Aphids/
      Whiteflies/
      Caterpillars/
      Beetles/
      Mites/
      Soil Degradation/
      Low Soil Moisture/
```

Each class folder should contain the corresponding crop images.

## How to Train

Run the training script after adding the dataset:

```bash
py train.py
```

This will generate `model_weights.h5` and `class_indices.json`.

## How to Run the App

Once training has completed, run:

```bash
streamlit run app.py
```

Then upload a crop image in the browser UI to see predictions and recommendations.

## Notes

- If `model_weights.h5` or `class_indices.json` is missing, the app will show a warning and disable inference.
- Use `requirements.txt` to install dependencies:

```bash
py -m pip install -r requirements.txt
```
