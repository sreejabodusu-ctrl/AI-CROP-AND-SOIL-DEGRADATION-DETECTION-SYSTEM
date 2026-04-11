import json
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import tensorflow as tf

# Use tf.keras for better compatibility with static analyzers
base_model = tf.keras.applications.MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(128, 128, 3)
)

x = base_model.output
x = tf.keras.layers.GlobalAveragePooling2D()(x)

predictions = tf.keras.layers.Dense(8, activation='softmax')(x)

model = tf.keras.Model(inputs=base_model.input, outputs=predictions)

# Compile the model (optional for inference, but good practice)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEIGHTS_CANDIDATES = [
    os.path.join(BASE_DIR, 'model_weights.h5'),
    os.path.join(BASE_DIR, 'checkpoints', 'model_weights.h5')
]
LABEL_MAPPING_CANDIDATES = [
    os.path.join(BASE_DIR, 'class_indices.json')
]

DEFAULT_CLASSES = [
    "Healthy",
    "Aphids",
    "Whiteflies",
    "Caterpillars",
    "Beetles",
    "Mites",
    "Soil Degradation",
    "Low Soil Moisture"
]

weights_loaded = False
class_mapping_loaded = False
classes = DEFAULT_CLASSES.copy()
weights_path = WEIGHTS_CANDIDATES[0]
label_mapping_path = LABEL_MAPPING_CANDIDATES[0]
load_error = None

for candidate in WEIGHTS_CANDIDATES:
    if os.path.exists(candidate):
        weights_path = candidate
        break

for candidate in LABEL_MAPPING_CANDIDATES:
    if os.path.exists(candidate):
        label_mapping_path = candidate
        break

if os.path.exists(weights_path):
    try:
        model.load_weights(weights_path)
        weights_loaded = True
    except Exception as exc:  # pragma: no cover - defensive path for startup diagnostics
        load_error = f'Failed to load weights from {weights_path}: {exc}'

if os.path.exists(label_mapping_path):
    try:
        with open(label_mapping_path, 'r', encoding='utf-8') as f:
            loaded_classes = json.load(f)

        # Backward compatibility in case mapping is stored as class->index dict.
        if isinstance(loaded_classes, dict):
            classes = [name for name, _ in sorted(loaded_classes.items(), key=lambda item: item[1])]
        elif isinstance(loaded_classes, list):
            classes = loaded_classes
        class_mapping_loaded = True
    except Exception as exc:  # pragma: no cover - defensive path for startup diagnostics
        load_error = f'Failed to load class mapping from {label_mapping_path}: {exc}'


def is_model_ready():
    return weights_loaded and class_mapping_loaded


def get_model_status():
    return {
        'ready': is_model_ready(),
        'weights_loaded': weights_loaded,
        'class_mapping_loaded': class_mapping_loaded,
        'weights_path': weights_path,
        'label_mapping_path': label_mapping_path,
        'load_error': load_error
    }


def predict_image(img):
    if not is_model_ready():
        raise RuntimeError(
            'Model is not fully ready. Ensure model_weights.h5 and class_indices.json are available.'
        )

    pred = model.predict(img)
    return classes[np.argmax(pred)]
