from src.pose.extractor import PoseExtractor

# مسار الموديل
MODEL_PATH = "models/pose_landmarker.task"

# ⚠️ اسم الفيديو عندك فيه مسافة مش underscore
VIDEO_PATH = "data/raw_videos/shoulder_press/shoulder press_1.mp4"

# إنشاء extractor
extractor = PoseExtractor(MODEL_PATH)

# تشغيل على الفيديو
raw, normalized, metadata = extractor.extract_from_video(VIDEO_PATH)

# طباعة النتائج
print("Raw shape:", raw.shape)
print("Normalized shape:", normalized.shape)
print("Frames processed:", len(metadata))

# قفل الموديل
extractor.close()