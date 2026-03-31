from src.dataset.builder import DatasetBuilder

MODEL_PATH = "models/pose_landmarker.task"
DATA_DIR = "data/raw_videos"

builder = DatasetBuilder()

X, y = builder.build_from_folder(DATA_DIR, MODEL_PATH)

print("Number of videos processed:", len(X))
print("Number of labels:", len(y))

if len(X) > 0:
    print("First sequence shape:", X[0].shape)
    print("First label:", y[0])