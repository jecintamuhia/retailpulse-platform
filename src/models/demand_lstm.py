import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class DemandSequenceDataset(Dataset):
    def __init__(self, target_array, window=30):
        self.scaler = MinMaxScaler()

        scaled = self.scaler.fit_transform(
            target_array.reshape(-1, 1)
        )

        self.data = torch.tensor(
            scaled,
            dtype=torch.float32
        )

        self.window = window

    def __len__(self):
        return len(self.data) - self.window

    def __getitem__(self, idx):
        x = self.data[idx: idx + self.window]
        y = self.data[idx + self.window]

        return x, y


class EnterpriseDemandLSTM(nn.Module):
    def __init__(
        self,
        in_dim=1,
        hidden_dim=64,
        layers=2
    ):
        super().__init__()

        self.lstm = nn.LSTM(
            input_size=in_dim,
            hidden_size=hidden_dim,
            num_layers=layers,
            batch_first=True
        )

        self.fc = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        out = self.fc(out)

        return out


def train_lstm_model(
    ts_array,
    epochs=10,
    batch_size=32,
    window=30
):
    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    dataset = DemandSequenceDataset(
        ts_array,
        window=window
    )

    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True
    )

    model = EnterpriseDemandLSTM().to(device)

    criterion = nn.MSELoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=0.001
    )

    model.train()

    for epoch in range(epochs):
        total_loss = 0.0

        for x, y in loader:
            x = x.to(device)
            y = y.to(device)

            optimizer.zero_grad()

            preds = model(x)

            loss = criterion(
                preds,
                y.view(-1, 1)
            )

            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(loader)

        print(
            f"Epoch {epoch + 1}/{epochs} | "
            f"Loss: {avg_loss:.6f}"
        )

    return model, dataset.scaler


def forecast_lstm(
    model,
    scaler,
    recent_sequence,
    steps=7
):
    device = next(model.parameters()).device

    model.eval()

    seq = scaler.transform(
        recent_sequence.reshape(-1, 1)
    )

    seq = torch.tensor(
        seq,
        dtype=torch.float32
    ).unsqueeze(0).to(device)

    predictions = []

    for _ in range(steps):
        with torch.no_grad():
            pred = model(seq).item()

        predictions.append(pred)

        new_value = torch.tensor(
            [[[pred]]],
            dtype=torch.float32,
            device=device
        )

        seq = torch.cat(
            [seq[:, 1:, :], new_value],
            dim=1
        )

    predictions = scaler.inverse_transform(
        np.array(predictions).reshape(-1, 1)
    )

    return predictions.flatten()