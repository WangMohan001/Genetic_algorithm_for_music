import torch
import torch.nn as nn
from genetic.fitness.fitness import Fitness
from genetic.item.music_piece import MusicPiece
import numpy as np

class MelodyTransformer(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_heads, num_layers, seq_len):
        """
        初始化 MelodyTransformer 模型。

        参数:
        - input_size: 每个音符的特征维度（例如 25 维，包括时值特征）。
        - hidden_size: Transformer 编码器的隐藏层维度。
        - output_size: 输出的维度（对于二分类问题为 1）。
        - num_heads: 多头注意力的头数。
        - num_layers: Transformer 编码器的层数。
        - seq_len: 输入序列的长度。
        """
        super(MelodyTransformer, self).__init__()
        
        self.input_size = input_size
        self.seq_len = seq_len
        
        # 定义输入特征映射到隐藏层维度的线性层
        self.input_fc = nn.Linear(input_size, hidden_size)
        
        # 定义位置编码
        self.positional_encoding = nn.Parameter(torch.zeros(1, seq_len, hidden_size))
        
        # 定义 Transformer 编码器层
        encoder_layer = nn.TransformerEncoderLayer(d_model=hidden_size, nhead=num_heads, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # 定义全连接层
        self.fc = nn.Linear(hidden_size, output_size)
        
        # 定义 Sigmoid 激活函数，用于二分类任务
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        """
        前向传播函数。

        参数:
        - x: 输入数据，形状为 (batch_size, seq_len, input_size)。

        返回:
        - output: 模型输出，形状为 (batch_size, 1)，表示旋律是否为好的旋律的概率。
        """
        # 输入特征映射到隐藏层维度
        x = self.input_fc(x)  # (batch_size, seq_len, hidden_size)
        
        # 添加位置编码
        x = x + self.positional_encoding[:, :x.size(1), :]  # 保持序列长度一致
        
        # Transformer 编码器输出
        transformer_out = self.transformer(x)  # (batch_size, seq_len, hidden_size)
        
        # 取最后一个时间步的输出
        last_hidden_state = transformer_out[:, -1, :]  # (batch_size, hidden_size)
        
        # 通过全连接层进行分类
        output = self.fc(last_hidden_state)
        
        # Sigmoid 激活，输出概率值
        output = self.sigmoid(output)  # (batch_size, 1)
        
        return output

class Fitness_Transformer(Fitness):
    def __init__(self):
        """
        初始化 Fitness 类，用于评估音乐片段。
        """
        # 参数配置：调整为适合的维度和模型超参数
        input_size = 25
        hidden_size = 64
        output_size = 1
        num_heads = 4
        num_layers = 4
        seq_len = 10
        
        self.model = MelodyTransformer(input_size, hidden_size, output_size, num_heads, num_layers, seq_len)
        self.model.load_state_dict(torch.load('genetic/models/checkpoint_Transformer.pt'))
        self.model.eval()

    def evaluate(self, music_piece: MusicPiece) -> float:
        """
        评估给定音乐片段的质量。

        参数:
        - music_piece: MusicPiece 对象，包含音乐片段信息。

        返回:
        - 一个浮点数，表示音乐片段的得分。
        """
        data = music_piece.get_notes()
        base = np.min(data)
        seq_len = 10
        input_size = 25
        scores = []
        for i in range(data.shape[0] - seq_len + 1):
            seq = data[i:i + seq_len]
            score = np.zeros((seq_len, input_size))
            for j in range(seq_len):
                score[j, min(input_size - 2, int(seq[j][0] - base))] = 1
                score[j, -1] = seq[j][1]
            scores.append(score)
        if len(scores) == 0:
            return 0
        scores = np.array(scores)
        scores = torch.tensor(scores).float()
        outputs = self.model(scores)
        return outputs.mean().item()  