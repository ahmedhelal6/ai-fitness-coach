from src.dataset.builder import DatasetBuilder
from src.dataset.preprocess import prepare_dataset

MODEL_PATH = "models/pose_landmarker.task"
DATA_DIR = "data/raw_videos"

builder = DatasetBuilder()

X, y = builder.build_from_folder(DATA_DIR, MODEL_PATH)

print("Before preprocessing:")
print("Number of samples:", len(X))

# 🔥 هنا بنجهز الداتا
X_tensor, y_tensor = prepare_dataset(X, y, target_length=100)

print("\nAfter preprocessing:")
print("X shape:", X_tensor.shape)
print("y shape:", y_tensor.shape)