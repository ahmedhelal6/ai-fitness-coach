import numpy as np


LEFT_RIGHT_PAIRS = [
    (1, 2),   # left_shoulder, right_shoulder
    (3, 4),   # left_elbow, right_elbow
    (5, 6),   # left_wrist, right_wrist
    (7, 8),   # left_hip, right_hip
    (9, 10),  # left_knee, right_knee
    (11, 12), # left_ankle, right_ankle
]


def add_gaussian_noise(sequence, std=0.01):
    seq = sequence.copy()
    noise = np.random.normal(0, std, seq.shape).astype(np.float32)
    seq += noise
    return seq


def random_scale(sequence, scale_range=(0.9, 1.1)):
    seq = sequence.copy()
    scale = np.random.uniform(scale_range[0], scale_range[1])
    seq[..., :2] *= scale
    return seq


def random_shift(sequence, shift_range=0.05):
    seq = sequence.copy()
    shift_x = np.random.uniform(-shift_range, shift_range)
    shift_y = np.random.uniform(-shift_range, shift_range)

    seq[..., 0] += shift_x
    seq[..., 1] += shift_y
    return seq


def horizontal_flip(sequence):
    seq = sequence.copy()

    # flip x
    seq[..., 0] = 1.0 - seq[..., 0]

    # swap left/right joints
    for left_idx, right_idx in LEFT_RIGHT_PAIRS:
        temp = seq[:, left_idx, :].copy()
        seq[:, left_idx, :] = seq[:, right_idx, :]
        seq[:, right_idx, :] = temp

    return seq


def temporal_crop_or_pad(sequence, target_length):
    seq = sequence.copy()
    t = len(seq)

    if t == target_length:
        return seq

    if t > target_length:
        start = np.random.randint(0, t - target_length + 1)
        return seq[start:start + target_length]

    pad_count = target_length - t
    last_frame = seq[-1:]
    pad = np.repeat(last_frame, pad_count, axis=0)
    return np.concatenate([seq, pad], axis=0)


def temporal_resample(sequence, target_length):
    seq = sequence.copy()
    old_len = len(seq)

    if old_len == target_length:
        return seq

    old_indices = np.linspace(0, old_len - 1, num=old_len)
    new_indices = np.linspace(0, old_len - 1, num=target_length)

    new_seq = []
    for idx in new_indices:
        left = int(np.floor(idx))
        right = min(left + 1, old_len - 1)
        alpha = idx - left
        frame = (1 - alpha) * seq[left] + alpha * seq[right]
        new_seq.append(frame)

    return np.array(new_seq, dtype=np.float32)


def random_speed_change(sequence, target_length, speed_range=(0.85, 1.15)):
    seq = sequence.copy()
    speed = np.random.uniform(speed_range[0], speed_range[1])

    new_len = max(5, int(len(seq) / speed))
    seq = temporal_resample(seq, new_len)
    seq = temporal_crop_or_pad(seq, target_length)

    return seq


def random_joint_dropout(sequence, dropout_prob=0.1):
    seq = sequence.copy()
    num_joints = seq.shape[1]

    for j in range(num_joints):
        if np.random.rand() < dropout_prob:
            seq[:, j, :] = 0.0

    return seq


def augment_sequence(sequence, target_length):
    seq = sequence.copy()

    # أولًا ظبطي الطول
    seq = temporal_crop_or_pad(seq, target_length)

    # اختيارات augmentation عشوائية
    if np.random.rand() < 0.7:
        seq = add_gaussian_noise(seq, std=0.01)

    if np.random.rand() < 0.5:
        seq = random_scale(seq, scale_range=(0.95, 1.05))

    if np.random.rand() < 0.5:
        seq = random_shift(seq, shift_range=0.03)

    if np.random.rand() < 0.5:
        seq = random_speed_change(seq, target_length, speed_range=(0.9, 1.1))

    if np.random.rand() < 0.3:
        seq = horizontal_flip(seq)

    if np.random.rand() < 0.2:
        seq = random_joint_dropout(seq, dropout_prob=0.05)

    return seq.astype(np.float32)