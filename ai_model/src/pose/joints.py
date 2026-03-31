EXERCISE_CLASSES = [
    "squat",
    "pushup",
    "bicep_curl",
    "shoulder_press",
    "hammer_curl",
]

CLASS_TO_IDX = {name: idx for idx, name in enumerate(EXERCISE_CLASSES)}
IDX_TO_CLASS = {idx: name for name, idx in CLASS_TO_IDX.items()}

MEDIAPIPE_LANDMARKS = {
    "nose": 0,
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_elbow": 13,
    "right_elbow": 14,
    "left_wrist": 15,
    "right_wrist": 16,
    "left_hip": 23,
    "right_hip": 24,
    "left_knee": 25,
    "right_knee": 26,
    "left_ankle": 27,
    "right_ankle": 28,
}

SELECTED_JOINTS = [
    "nose",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle",
]

SELECTED_INDICES = [MEDIAPIPE_LANDMARKS[joint] for joint in SELECTED_JOINTS]

SKELETON_EDGES = [
    (0, 1),
    (0, 2),
    (1, 3),
    (3, 5),
    (2, 4),
    (4, 6),
    (1, 7),
    (2, 8),
    (7, 8),
    (7, 9),
    (9, 11),
    (8, 10),
    (10, 12),
]