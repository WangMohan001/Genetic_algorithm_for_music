import os
import numpy as np
import torch
from torch.utils.data import Dataset, random_split
from sklearn.model_selection import train_test_split
import random

class MelodyDataset(Dataset):
    def __init__(self, data_dir, seq_len=10, input_size=24):
        """
        初始化数据集。

        参数:
        - data_dir: 包含所有 .npy 文件的目录。
        - random_data_ratio: 随机旋律的比例，介于 0 到 1 之间。
        - seq_len: 音符序列的长度，默认为 10。
        - input_size: 每个音符的维度，默认为 24（表示 one-hot 编码）。
        """
        self.data_dir = data_dir
        self.seq_len = seq_len
        self.input_size = input_size
        
        self.data = []
        # 加载数据并创建数据集
        if data_dir != "":
            self._load_data(data_dir, 1)
        
    def _load_data(self, file_dir,  target_label=1, flip=False, reverse=False):
        """
        从目录读取所有 .npy 文件，并根据需要生成标签。
        """
        # 读取目录下的所有 .npy 文件
        files = [f for f in os.listdir(file_dir) if f.endswith('.npy')]
        #print(self.files)
        for file in files:
            file_path = os.path.join(file_dir, file)
            data = np.load(file_path, allow_pickle=True)[:, 0]
            base = np.min(data)
            # 假设 .npy 文件中的第一列是音符序列，标签为 1
            if data.shape[0] >= self.seq_len:  # 确保数据的列数大于等于 seq_len
                for i in range(data.shape[0] - self.seq_len + 1):  # 生成滑动窗口
                    seq = data[i:i + self.seq_len]
                    score = np.zeros((self.seq_len, self.input_size))
                    for j in range(self.seq_len):
                        score[j, min(self.input_size - 1, int(seq[j] - base))] = 1
                    self.data.append((score, target_label))
                    if flip:
                        self.data.append((score[::-1].copy(), target_label))  # Make a copy after reversing
                    if reverse:
                        self.data.append((score[:, ::-1].copy(), target_label))  # Make a copy after reversing along columns
                    if flip and reverse:
                        self.data.append((score[::-1, ::-1].copy(), target_label))
                    
    def _generate_random_data(self, num_samples):
        """
        生成随机的音符序列。
        
        参数:
        - num_samples: 需要生成的样本数量。
        """
        for _ in range(num_samples):
            sample = np.zeros((self.seq_len, self.input_size))
            for i in range(self.seq_len):
                sample[i, random.randint(0, self.input_size-1)] = 1
            self.data.append((sample, 0))
    def _balance_data(self):
        """
        平衡数据集，使好旋律和随机旋律的数量相等。
        """
        good_melody_count = len([d for d in self.data if d[1] == 1])
        random_data_count = len([d for d in self.data if d[1] == 0])
        
        if good_melody_count > random_data_count:
            self._generate_random_data(good_melody_count - random_data_count)
    def _shuffle_data(self):
        """
        打乱数据集。
        """
        random.shuffle(self.data)

        
    def __len__(self):
        """
        返回数据集的大小。
        """
        return len(self.data)
    
    def __getitem__(self, idx):
        """
        获取数据集中的某一项数据。
        
        参数:
        - idx: 数据的索引。
        
        返回:
        - 音符序列 (Tensor)，标签 (Tensor)。
        """
        seq, label = self.data[idx]
        return torch.tensor(seq, dtype=torch.float32), torch.tensor(label, dtype=torch.float32)
    @staticmethod
    def from_data(data, seq_len, input_size):
        """
        从给定的 data 和 seq_len 创建一个新的 MelodyDataset 实例。

        参数:
        - data: 数据，列表形式，包含音符序列和标签。
        - seq_len: 每个音符序列的长度。
        - input_size: 每个音符的维度（默认为 24）。

        返回:
        - 一个 MelodyDataset 实例。
        """
        dataset = MelodyDataset(data_dir="")  # 不读取文件
        dataset.data = data
        dataset.seq_len = seq_len
        dataset.input_size = input_size
        return dataset
    
    def split_data(self, test_size=0.2, random_seed=42):
        """
        将数据集分割成训练集和验证集。

        参数:
        - test_size: 验证集的比例（0到1之间，默认为 0.2）。
        - random_seed: 随机种子，用于确保可重复性。

        返回:
        - train_data: 训练集数据。
        - val_data: 验证集数据。
        """
        # 使用 sklearn 的 train_test_split 将数据分为训练集和验证集
        train_data, val_data = train_test_split(self.data, test_size=test_size, random_state=random_seed)
        
        # 创建并返回两个新的 Dataset 实例
        train_dataset = MelodyDataset.from_data(train_data, self.seq_len, self.input_size)
        val_dataset = MelodyDataset.from_data(val_data, self.seq_len, self.input_size)

        return train_dataset, val_dataset
# 示例用法：
if __name__ == "__main__":
    data_dir = './data'  # 这里填入你的目录
    dataset = MelodyDataset(data_dir)
    dataset._balance_data()
    dataset._shuffle_data()
    print(f"Dataset size: {len(dataset)}")
    for i in range(5):
        seq, label = dataset[i]
        print(f"Sample {i+1}:")
        print(f"Sequence:\n{seq}")
        print(f"Label: {label.item()}")
