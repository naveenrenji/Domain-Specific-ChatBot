import pandas as pd
import torch
from torch.utils.data import TensorDataset, DataLoader
from sklearn.metrics import classification_report
from tqdm import tqdm



# Load data
df = pd.read_csv('feasibilityDataChatGPT.csv')
df['description'] = df['description'].fillna('missing').apply(lambda x: x.lower())

df['description'] = df['description'].apply(lambda x: x.lower())

novelty_counts = df['feasibility'].value_counts()
print("Number of novel descriptions:", novelty_counts[1])
print("Number of non-novel descriptions:", novelty_counts[0])