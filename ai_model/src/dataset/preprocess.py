from typing import List, Tuple

import numpy as np
import torch


def pad_or_truncate_sequence(sequence: np.ndarray, target_length: int) -> np.ndarray:
    """
    Make every sequence have the same number of frames.

    Args:
        sequence: shape (T, V, 4)
        target_length: required number of frames

    Returns:
        sequence with shape (target_length, V, 4)
    """
    if sequence.ndim != 3 or sequence.shape[2] != 4:
        raise ValueError(f"Expected shape (T, V, 4), got {sequence.shape}")

    current_length = sequence.shape[0]

    if current_length == target_length:
        return sequence

    if current_length > target_length:
        return sequence[:target_length]

    pad_count = target_length - current_length
    last_frame = sequence[-1:]
    padding = np.repeat(last_frame, pad_count, axis=0)

    return np.concatenate([sequence, padding], axis=0)


def sequence_to_model_input(sequence: np.ndarray) -> np.ndarray:
    """
    Convert sequence from (T, V, 4) to (C, T, V)

    We keep only x, y, z and ignore visibility for the model input.

    Args:
        sequence: shape (T, V, 4)

    Returns:
        shape (3, T, V)
    """
    if sequence.ndim != 3 or sequence.shape[2] != 4:
        raise ValueError(f"Expected shape (T, V, 4), got {sequence.shape}")

    xyz = sequence[:, :, :3]          # (T, V, 3)
    xyz = np.transpose(xyz, (2, 0, 1))  # (3, T, V)

    return xyz.astype(np.float32)


def prepare_dataset(
    X: List[np.ndarray],
    y: List[int],
    target_length: int,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Prepare full dataset for PyTorch model.

    Args:
        X: list of sequences, each shape (T, V, 4)
        y: list of integer labels
        target_length: fixed number of frames for all sequences

    Returns:
        X_tensor: shape (N, 3, target_length, V)
        y_tensor: shape (N,)
    """
    if len(X) == 0:
        raise ValueError("X is empty")

    if len(X) != len(y):
        raise ValueError("X and y must have the same length")

    processed_sequences = []

    for sequence in X:
        fixed_sequence = pad_or_truncate_sequence(sequence, target_length)
        model_input = sequence_to_model_input(fixed_sequence)
        processed_sequences.append(model_input)

    X_array = np.stack(processed_sequences, axis=0)  # (N, 3, T, V)
    y_array = np.array(y, dtype=np.int64)

    X_tensor = torch.tensor(X_array, dtype=torch.float32)
    y_tensor = torch.tensor(y_array, dtype=torch.long)

    return X_tensor, y_tensor