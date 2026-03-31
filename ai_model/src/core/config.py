from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SEQUENCE_LENGTH = 30
PREDICTION_THRESHOLD = 0.7
EXERCISE_SWITCH_DELAY = 5
IDLE_FRAME_THRESHOLD = 30
MOTION_THRESHOLD = 0.010

MODEL_PATH = PROJECT_ROOT / "exercise_model.pth"
POSE_TASK_PATH = PROJECT_ROOT / "models" / "pose_landmarker.task"