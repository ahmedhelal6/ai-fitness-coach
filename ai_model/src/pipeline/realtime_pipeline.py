import time
import cv2
import torch
import numpy as np

from src.core.config import (
    POSE_TASK_PATH,
    MODEL_PATH,
    SEQUENCE_LENGTH,
    PREDICTION_THRESHOLD,
    EXERCISE_SWITCH_DELAY,
    IDLE_FRAME_THRESHOLD,
    MOTION_THRESHOLD,
)

from src.pose.extractor import PoseExtractor
from src.dataset.preprocess import sequence_to_model_input
from src.model.stgcn import SimpleSTGCN
from src.pose.joints import IDX_TO_CLASS, SELECTED_INDICES, SKELETON_EDGES

from src.counter.angles import calculate_angle
from src.counter.rules import EXERCISE_COUNTER_RULES
from src.counter.rep_counter import RepCounter


NUM_CLASSES = len(IDX_TO_CLASS)
NUM_JOINTS = 13


class RealtimePipeline:
    def __init__(self):
        self.model = SimpleSTGCN(num_joints=NUM_JOINTS, num_classes=NUM_CLASSES)
        self.model.load_state_dict(torch.load(str(MODEL_PATH), map_location="cpu"))
        self.model.eval()

        self.extractor = PoseExtractor(str(POSE_TASK_PATH))

        self.sequence_buffer = []
        self.prev_keypoints = None
        self.idle_frames = 0

        self.current_exercise = None
        self.pending_exercise = None
        self.pending_count = 0

        self.exercise_counters = {}
        self.current_counter = None

        self.current_state = {
            "reps": 0,
            "stage": None,
            "angle": None,
        }

        self.start_time = time.time()

    def _compute_motion(self, keypoints: np.ndarray) -> float:
        if self.prev_keypoints is None:
            return 1.0

        diff = np.abs(keypoints[:, :3] - self.prev_keypoints[:, :3])
        return float(np.mean(diff))

    def _get_or_create_counter(self, exercise_name: str):
        if exercise_name not in self.exercise_counters:
            self.exercise_counters[exercise_name] = RepCounter(
                EXERCISE_COUNTER_RULES[exercise_name]
            )
        return self.exercise_counters[exercise_name]

    def _reset_state(self):
        self.current_exercise = None
        self.pending_exercise = None
        self.pending_count = 0
        self.current_counter = None
        self.sequence_buffer.clear()
        self.prev_keypoints = None
        self.idle_frames = 0
        self.current_state = {
            "reps": 0,
            "stage": None,
            "angle": None,
        }

    def _update_prediction_state(self, predicted_class: str, confidence: float):
        if confidence < PREDICTION_THRESHOLD:
            self.pending_exercise = None
            self.pending_count = 0
            return

        if predicted_class not in EXERCISE_COUNTER_RULES:
            self.pending_exercise = None
            self.pending_count = 0
            return

        if self.pending_exercise == predicted_class:
            self.pending_count += 1
        else:
            self.pending_exercise = predicted_class
            self.pending_count = 1

        if self.pending_count >= EXERCISE_SWITCH_DELAY:
            if self.current_exercise != self.pending_exercise:
                self.current_exercise = self.pending_exercise
                self.current_counter = self._get_or_create_counter(self.current_exercise)

            self.pending_exercise = None
            self.pending_count = 0

    def _draw_all_landmarks(self, frame, pose_landmarks):
        h, w, _ = frame.shape
        points = []

        for idx in SELECTED_INDICES:
            lm = pose_landmarks[idx]
            x, y = int(lm.x * w), int(lm.y * h)
            points.append((x, y))

            if 0 <= x < w and 0 <= y < h:
                cv2.circle(frame, (x, y), 4, (0, 255, 255), -1)

        return points

    def _draw_full_skeleton(self, frame, pose_landmarks):
        h, w, _ = frame.shape
        points = self._draw_all_landmarks(frame, pose_landmarks)

        for i, j in SKELETON_EDGES:
            if i < len(points) and j < len(points):
                x1, y1 = points[i]
                x2, y2 = points[j]

                if 0 <= x1 < w and 0 <= y1 < h and 0 <= x2 < w and 0 <= y2 < h:
                    cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

        return frame

    def _update_rep_counter(self, frame, pose_landmarks):
        if self.current_counter is None:
            return frame

        if self.current_exercise not in EXERCISE_COUNTER_RULES:
            return frame

        h, w, _ = frame.shape
        config = EXERCISE_COUNTER_RULES[self.current_exercise]
        p1_idx, p2_idx, p3_idx = config["points"]

        def get_point(idx):
            lm = pose_landmarks[idx]
            return int(lm.x * w), int(lm.y * h)

        p1 = get_point(p1_idx)
        p2 = get_point(p2_idx)
        p3 = get_point(p3_idx)

        angle = calculate_angle(p1, p2, p3)
        self.current_state = self.current_counter.update(angle)

        cv2.circle(frame, p1, 6, (255, 0, 0), -1)
        cv2.circle(frame, p2, 6, (0, 255, 0), -1)
        cv2.circle(frame, p3, 6, (0, 0, 255), -1)

        cv2.line(frame, p1, p2, (0, 255, 0), 3)
        cv2.line(frame, p2, p3, (0, 255, 0), 3)

        cv2.putText(
            frame,
            str(int(angle)),
            (p2[0], p2[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2,
        )

        return frame

    def process_frame(self, frame):
        timestamp_ms = int((time.time() - self.start_time) * 1000)
        confidence = 0.0

        result = self.extractor.extract_from_frame(frame, timestamp_ms)

        if not result["detected"]:
            self.idle_frames += 1
            if self.idle_frames > IDLE_FRAME_THRESHOLD:
                self._reset_state()

            return frame, self.current_exercise, self.current_state["reps"], confidence

        keypoints = result["normalized_keypoints"]
        pose_landmarks = result["pose_landmarks"]

        frame = self._draw_full_skeleton(frame, pose_landmarks)

        motion_score = self._compute_motion(keypoints)
        self.prev_keypoints = keypoints

        if motion_score < MOTION_THRESHOLD:
            self.idle_frames += 1
        else:
            self.idle_frames = 0

        if self.idle_frames > IDLE_FRAME_THRESHOLD:
            self._reset_state()
            return frame, self.current_exercise, self.current_state["reps"], confidence

        self.sequence_buffer.append(keypoints)
        if len(self.sequence_buffer) > SEQUENCE_LENGTH:
            self.sequence_buffer.pop(0)

        if len(self.sequence_buffer) == SEQUENCE_LENGTH:
            seq = np.array(self.sequence_buffer, dtype=np.float32)
            model_input = sequence_to_model_input(seq)
            model_input = torch.tensor(model_input, dtype=torch.float32).unsqueeze(0)

            with torch.no_grad():
                output = self.model(model_input)
                probs = torch.softmax(output, dim=1)
                conf, pred_label = torch.max(probs, dim=1)
                confidence = conf.item()

            predicted_class = IDX_TO_CLASS[pred_label.item()]
            self._update_prediction_state(predicted_class, confidence)

        if self.current_counter is not None:
            frame = self._update_rep_counter(frame, pose_landmarks)

        return frame, self.current_exercise, self.current_state["reps"], confidence

    def close(self):
        self.extractor.close()