import torch
import torch.nn as nn

class MelodyLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        """
        初始化 MelodyLSTM 模型。

        参数:
        - input_size: 每个音符的特征维度（例如 24 维 one-hot 编码）。
        - hidden_size: LSTM 隐藏层的神经元数量。
        - output_size: 输出的维度（对于二分类问题为 1）。
        """
        super(MelodyLSTM, self).__init__()
        
        # 定义 LSTM 层
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        
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
        # LSTM 层输出
        lstm_out, (h_n, c_n) = self.lstm(x)  # 获取 LSTM 层的输出
        
        # 取 LSTM 输出序列的最后一个时间步的隐藏状态
        last_hidden_state = h_n[-1]  # (batch_size, hidden_size)
        
        # 通过全连接层进行分类
        output = self.fc(last_hidden_state)
        
        # Sigmoid 激活，输出概率值
        output = self.sigmoid(output)  # (batch_size, 1)
        
        return output
