import torch

from src.pose.extractor import PoseExtractor
from src.dataset.preprocess import pad_or_truncate_sequence, sequence_to_model_input
from src.model.stgcn import SimpleSTGCN
from src.pose.joints import IDX_TO_CLASS

MODEL_PATH = "models/pose_landmarker.task"
VIDEO_PATH = "data/raw_videos/shoulder_press/shoulder press_1.mp4"

NUM_CLASSES = 5
TARGET_LENGTH = 100
NUM_JOINTS = 13


def main():
    model = SimpleSTGCN(num_joints=NUM_JOINTS, num_classes=NUM_CLASSES)
    model.load_state_dict(torch.load("exercise_model.pth", map_location="cpu"))
    model.eval()

    extractor = PoseExtractor(MODEL_PATH)
    _, normalized_seq, metadata = extractor.extract_from_video(VIDEO_PATH)
    extractor.close()

    fixed_seq = pad_or_truncate_sequence(normalized_seq, TARGET_LENGTH)
    model_input = sequence_to_model_input(fixed_seq)
    model_input = torch.tensor(model_input, dtype=torch.float32).unsqueeze(0)

    with torch.no_grad():
        output = model(model_input)
        predicted_label = torch.argmax(output, dim=1).item()

    predicted_class = IDX_TO_CLASS[predicted_label]

    print("Predicted label:", predicted_label)
    print("Predicted class:", predicted_class)
    print("Frames:", len(metadata))


if __name__ == "__main__":
    main()