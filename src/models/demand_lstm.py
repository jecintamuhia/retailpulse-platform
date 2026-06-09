import torch
import torch.nn as nn
from torch.utils.data import Dataset
class DemandSequenceDataset(Dataset):
 def __init__(self, target_array, window=30):
 self.data = torch.tensor(target_array, dtype=torch.float32)
 self.window = window
 def __len__(self):
 return len(self.data) - self.window
 def __getitem__(self, idx):
 return self.data[idx : idx + self.window].unsqueeze(-1), self.data[idx + self.window]
class EnterpriseDemandLSTM(nn.Module):
 def __init__(self, in_dim=1, hidden_dim=64, layers=2):
 super().__init__()
 self.lstm = nn.LSTM(in_dim, hidden_dim, layers, batch_first=True)
 self.fc = nn.Linear(hidden_dim, 1)
 def forward(self, x):
 out, _ = self.lstm(x)
 return self.fc(out[:, -1, :]).squeeze(-1)
