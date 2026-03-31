import cv2

from src.pipeline.realtime_pipeline import RealtimePipeline


def format_exercise_name(exercise):
    if exercise is None:
        return "No Exercise"

    pretty_names = {
        "squat": "Squat",
        "pushup": "Push-Up",
        "bicep_curl": "Bicep Curl",
        "shoulder_press": "Shoulder Press",
        "hammer_curl": "Hammer Curl",
    }

    return pretty_names.get(exercise, exercise.replace("_", " ").title())


def draw_ui(frame, exercise, reps, confidence, stage=None, angle=None):
    h, w, _ = frame.shape

    panel_w = 420
    panel_h = 190

    cv2.rectangle(frame, (10, 10), (10 + panel_w, 10 + panel_h), (25, 25, 25), -1)
    cv2.rectangle(frame, (10, 10), (10 + panel_w, 10 + panel_h), (70, 70, 70), 2)

    display_exercise = format_exercise_name(exercise)
    display_stage = stage if stage is not None else "---"
    display_angle = str(int(angle)) if angle is not None else "---"

    if exercise is None:
        exercise_color = (180, 180, 180)
    else:
        exercise_color = (0, 255, 180)

    cv2.putText(
        frame,
        "AI FITNESS COACH",
        (25, 38),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        f"Exercise: {display_exercise}",
        (25, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        exercise_color,
        2,
    )

    cv2.putText(
        frame,
        f"Reps: {reps}",
        (25, 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2,
    )

    cv2.putText(
        frame,
        f"Stage: {display_stage}",
        (25, 145),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 200, 255),
        2,
    )

    cv2.putText(
        frame,
        f"Angle: {display_angle}",
        (25, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255, 255, 0),
        2,
    )

    cv2.putText(
        frame,
        f"Confidence: {confidence:.2f}",
        (w - 220, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        "ESC to exit",
        (w - 145, h - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (200, 200, 200),
        2,
    )


def main():
    pipeline = RealtimePipeline()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera error")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame from camera.")
                break

            frame = cv2.flip(frame, 1)

            annotated_frame, current_exercise, reps, confidence = pipeline.process_frame(frame)

            current_state = getattr(
                pipeline,
                "current_state",
                {"stage": None, "angle": None}
            )

            draw_ui(
                annotated_frame,
                current_exercise,
                reps,
                confidence,
                stage=current_state.get("stage"),
                angle=current_state.get("angle"),
            )

            cv2.imshow("AI Fitness Coach", annotated_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break

    finally:
        cap.release()
        pipeline.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()