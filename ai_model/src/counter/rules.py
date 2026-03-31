# MediaPipe indices
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW = 13
RIGHT_ELBOW = 14
LEFT_WRIST = 15
RIGHT_WRIST = 16
LEFT_HIP = 23
RIGHT_HIP = 24
LEFT_KNEE = 25
RIGHT_KNEE = 26
LEFT_ANKLE = 27
RIGHT_ANKLE = 28


EXERCISE_COUNTER_RULES = {
    "squat": {
        "label": "Squat",
        "points": (RIGHT_HIP, RIGHT_KNEE, RIGHT_ANKLE),
        "full_angle": 155,
        "contract_angle": 100,
        "mode": "up_down_up",
        "start_stage": "up",
    },
    "pushup": {
        "label": "Push-Up",
        "points": (RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST),
        "full_angle": 160,
        "contract_angle": 80,
        "mode": "up_down_up",
        "start_stage": "up",
    },
    "bicep_curl": {
        "label": "Bicep Curl",
        "points": (RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST),
        "full_angle": 150,
        "contract_angle": 50,
        "mode": "down_up",
        "start_stage": "down",
    },
    "shoulder_press": {
        "label": "Shoulder Press",
        "points": (RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST),
        "full_angle": 160,
        "contract_angle": 70,
        "mode": "down_up",
        "start_stage": "down",
    },
    "hammer_curl": {
        "label": "Hammer Curl",
        "points": (RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST),
        "full_angle": 150,
        "contract_angle": 55,
        "mode": "down_up",
        "start_stage": "down",
    },
}