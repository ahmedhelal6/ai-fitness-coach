import torch
import torch.nn as nn
import torch.optim as optim

from src.dataset.builder import DatasetBuilder
from src.dataset.preprocess import prepare_dataset
from src.dataset.augmentation import augment_sequence
from src.model.stgcn import SimpleSTGCN

MODEL_PATH = "models/pose_landmarker.task"
DATA_DIR = "data/raw_videos"

NUM_CLASSES = 5
TARGET_LENGTH = 100
BATCH_SIZE = 8
EPOCHS = 10
LR = 0.001

builder = DatasetBuilder()
X, y = builder.build_from_folder(DATA_DIR, MODEL_PATH)

aug_X = []
aug_y = []

for seq, label in zip(X, y):
    aug_X.append(seq)
    aug_y.append(label)

    aug_X.append(augment_sequence(seq, TARGET_LENGTH))
    aug_y.append(label)

X_tensor, y_tensor = prepare_dataset(aug_X, aug_y, TARGET_LENGTH)

print("Dataset shape:", X_tensor.shape)

dataset = torch.utils.data.TensorDataset(X_tensor, y_tensor)
loader = torch.utils.data.DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

num_joints = X_tensor.shape[-1]
model = SimpleSTGCN(num_joints=num_joints, num_classes=NUM_CLASSES)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LR)

for epoch in range(EPOCHS):
    total_loss = 0.0

    for batch_X, batch_y in loader:
        optimizer.zero_grad()

        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(loader)
    print(f"Epoch [{epoch+1}/{EPOCHS}] - Loss: {avg_loss:.4f}")

print("Training finished")
torch.save(model.state_dict(), "exercise_model.pth")
print("Model saved to exercise_model.pth")