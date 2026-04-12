import json
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
# Avoid Pylance path issues by using tf.keras callbacks through the tf alias
ModelCheckpoint = tf.keras.callbacks.ModelCheckpoint
EarlyStopping = tf.keras.callbacks.EarlyStopping
ReduceLROnPlateau = tf.keras.callbacks.ReduceLROnPlateau
IMG_SIZE = 128
BATCH_SIZE = 16
EPOCHS = 20
NUM_CLASSES = 8
TRAIN_DIR = 'data/train'
VALID_DIR = 'data/valid'
ALLOWED_IMAGE_EXTENSIONS = {'.bmp', '.gif', '.jpeg', '.jpg', '.png'}
def count_image_files(directory):
    total = 0
    for root_dir, _, files in os.walk(directory):
        for filename in files:
            if os.path.splitext(filename)[1].lower() in ALLOWED_IMAGE_EXTENSIONS:
                total += 1
    return total
if not os.path.isdir(TRAIN_DIR):
    raise FileNotFoundError(
        f"Training directory not found. Please create the dataset folder:\n"
        f"{TRAIN_DIR}\n"
        "Each class should be a subfolder inside this directory."
    )
train_image_count = count_image_files(TRAIN_DIR)
if train_image_count == 0:
    raise FileNotFoundError(
        f"No image files found in training directory {TRAIN_DIR}."
        " Please add images to the class subfolders before training."
    )
valid_available = False
if os.path.isdir(VALID_DIR):
    valid_image_count = count_image_files(VALID_DIR)
    if valid_image_count > 0:
        valid_available = True
    else:
        print(f"Warning: Validation directory {VALID_DIR} contains no valid image files. Training will continue without validation.")
else:
    print(f"Warning: Validation directory {VALID_DIR} not found. Training will continue without validation.")

# Data pipeline using tf.data and image_dataset_from_directory instead of ImageDataGenerator
AUTOTUNE = tf.data.AUTOTUNE
train_dataset = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    labels='inferred',
    label_mode='categorical',
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    shuffle=True
)
print('Class names:', train_dataset.class_names)
label_order = train_dataset.class_names
with open('class_indices.json', 'w', encoding='utf-8') as f:
    json.dump(label_order, f, ensure_ascii=False, indent=2)
print('Saved label mapping to class_indices.json')
rescale_layer = tf.keras.layers.Rescaling(1.0 / 255.0)
train_dataset = train_dataset.map(lambda x, y: (rescale_layer(x), y), num_parallel_calls=AUTOTUNE).prefetch(AUTOTUNE)
valid_dataset = None
if valid_available:
    valid_dataset = tf.keras.utils.image_dataset_from_directory(
        VALID_DIR,
        labels='inferred',
        label_mode='categorical',
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        shuffle=False
    )
    valid_dataset = valid_dataset.map(lambda x, y: (rescale_layer(x), y), num_parallel_calls=AUTOTUNE).prefetch(AUTOTUNE)
# Model building function (reuse same architecture)
def build_model():
    base_model = tf.keras.applications.MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(IMG_SIZE, IMG_SIZE, 3)
    )
    base_model.trainable = False
    x = base_model.output
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')(x)
    model = tf.keras.Model(inputs=base_model.input, outputs=outputs)
    return model
model = build_model()
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
print(model.summary())
os.makedirs('checkpoints', exist_ok=True)
if valid_dataset is not None:
    callbacks = [
        ModelCheckpoint('checkpoints/model_weights.h5', monitor='val_accuracy', save_best_only=True, verbose=1),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, verbose=1, min_lr=1e-7),
        EarlyStopping(monitor='val_loss', patience=6, verbose=1, restore_best_weights=True)
    ]
    history = model.fit(
        train_dataset,
        validation_data=valid_dataset,
        epochs=EPOCHS,
        callbacks=callbacks
    )
else:
    callbacks = [
        ModelCheckpoint('checkpoints/model_weights.h5', monitor='accuracy', save_best_only=True, verbose=1),
        ReduceLROnPlateau(monitor='loss', factor=0.5, patience=3, verbose=1, min_lr=1e-7),
        EarlyStopping(monitor='loss', patience=6, verbose=1, restore_best_weights=True)
    ]
    history = model.fit(
        train_dataset,
        epochs=EPOCHS,
        callbacks=callbacks
    )
model.save_weights('model_weights.h5')
model.save('model_saved')
print('Training complete. Model weights saved to model_weights.h5 and model_saved/')
