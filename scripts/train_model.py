import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
# Load and preprocess data
filename = "breathing_dataset.csv"
data = pd.read_csv(filename)
feature_cols = ['mean', 'std', 'min', 'max']
X = data[feature_cols].astype(float).values
scaler = StandardScaler()
X = scaler.fit_transform(X)
y = LabelEncoder().fit_transform(data['label'].values)
#  Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")
#  Convert to PyTorch tensors
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Shape: [batch, channels, seq_len]
X_train_t = torch.tensor(X_train, dtype=torch.float32).unsqueeze(1).to(device)
X_test_t = torch.tensor(X_test, dtype=torch.float32).unsqueeze(1).to(device)
y_train_t = torch.tensor(y_train, dtype=torch.long).to(device)
y_test_t = torch.tensor(y_test, dtype=torch.long).to(device)

# Define 1D CNN model
class Simple1DCNN(nn.Module):
    def __init__(self, input_channels=1, seq_len=4, num_classes=2):
        super(Simple1DCNN, self).__init__()
        self.conv1 = nn.Conv1d(input_channels, 16, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm1d(16)
        self.pool = nn.MaxPool1d(2)
        self.conv2 = nn.Conv1d(16, 32, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm1d(32)
        seq_len_after_pool = seq_len // 2
        self.fc1 = nn.Linear(32 * seq_len_after_pool, 64)
        self.fc2 = nn.Linear(64, num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.pool(x)
        x = self.relu(self.bn2(self.conv2(x)))
        x = torch.flatten(x, 1)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


# Initialize model, loss, optimizer
model = Simple1DCNN(input_channels=1, seq_len=X.shape[1], num_classes=len(np.unique(y))).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)
# Training loop
epochs = 20
for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()
    outputs = model(X_train_t)
    loss = criterion(outputs, y_train_t)
    loss.backward()
    optimizer.step()
    if (epoch+1) % 5 == 0:
        print(f"Epoch {epoch+1}/{epochs} - Loss: {loss.item():.4f}")
# Evaluation
model.eval()
with torch.no_grad():
    outputs = model(X_test_t)
    preds = torch.argmax(outputs, dim=1).cpu().numpy()

acc = accuracy_score(y_test, preds)
prec = precision_score(y_test, preds, average='weighted', zero_division=0)
rec = recall_score(y_test, preds, average='weighted', zero_division=0)
cm = confusion_matrix(y_test, preds)

print("\n===== Evaluation Metrics =====")
print(f"Accuracy: {acc:.2f}")
print(f"Precision: {prec:.2f}")
print(f"Recall: {rec:.2f}")
print(f"Confusion Matrix:\n{cm}")
