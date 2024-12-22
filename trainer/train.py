import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from model import MelodyLSTM
from dataset import MelodyDataset
from tqdm import tqdm  # 导入 tqdm 进度条

def train(model, train_loader, criterion, optimizer, num_epochs=10):
    """
    训练模型的函数。

    参数:
    - model: 需要训练的模型。
    - train_loader: 训练数据加载器。
    - criterion: 损失函数。
    - optimizer: 优化器。
    - num_epochs: 训练的轮数，默认为 10。
    """
    for epoch in range(num_epochs):
        model.train()  # 设置模型为训练模式
        
        total_loss = 0.0
        correct = 0
        total = 0
        
        # 使用 tqdm 包裹 DataLoader 以显示进度条
        for batch_X, batch_Y in tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}", ncols=100):
            # 清空梯度
            optimizer.zero_grad()
            
            # 模型输出
            outputs = model(batch_X)
            
            # 计算损失
            loss = criterion(outputs.squeeze(), batch_Y)
            
            # 反向传播并更新权重
            loss.backward()
            optimizer.step()
            
            # 累加损失
            total_loss += loss.item()
            
            # 计算准确率
            predicted = (outputs > 0.5)# 如果概率大于 0.5，则预测为 1（好旋律）
            #print(predicted)
            predicted = predicted.numpy().flatten()
            #print(predicted)
            correct += sum(1 for i in range(len(predicted)) if predicted[i] == batch_Y[i])
            total += len(batch_Y)
        
        avg_loss = total_loss / len(train_loader)
        accuracy = correct / total * 100
        
        # 输出训练进度
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}, Accuracy: {accuracy:.2f}%")


def validate(model, val_loader, criterion):
    """
    验证模型的函数。

    参数:
    - model: 需要验证的模型。
    - val_loader: 验证数据加载器。
    - criterion: 损失函数。
    
    返回:
    - val_loss: 验证集上的损失。
    - val_accuracy: 验证集上的准确率。
    """
    model.eval()  # 设置模型为评估模式
    
    total_loss = 0.0
    correct = 0
    total = 0
    
    # 使用 tqdm 包裹验证集
    with torch.no_grad():  # 不计算梯度
        for batch_X, batch_Y in tqdm(val_loader, desc="Validation", ncols=100):
            outputs = model(batch_X)
            loss = criterion(outputs.squeeze(), batch_Y)
            total_loss += loss.item()
            
            # 计算准确率
            predicted = (outputs > 0.5)# 如果概率大于 0.5，则预测为 1（好旋律）
            #print(predicted)
            predicted = predicted.numpy().flatten()
            #print(predicted)
            correct += sum(1 for i in range(len(predicted)) if predicted[i] == batch_Y[i])
            total += len(batch_Y)
           # print(batch_Y)
           # print(predicted)
            #print((predicted == batch_Y).sum().item())
    
    val_loss = total_loss / len(val_loader)
    val_accuracy = correct / total * 100
    
    return val_loss, val_accuracy

def main():
    """
    主函数，初始化数据集，模型，损失函数，优化器，并启动训练过程。
    """
    # 设置数据集目录
    data_dir = 'data'  # 这里是存放 .npy 文件的目录
    
    # 创建数据集
    dataset = MelodyDataset("")
    dataset._load_data(data_dir, reverse=True)  # 从文件加载数据集 
    print(len(dataset))
    dataset._load_data('data_iter3', 0, flip=True, reverse=True)  # 从文件加载数据集
    print(len(dataset))
    dataset._load_data('data_iter2', 0, flip=True, reverse=True)  # 从文件加载数据集

    print(len(dataset))
    dataset._load_data('data_iter1', 0, flip=True, reverse=True)  # 从文件加载数据集
    print(len(dataset))
    dataset._balance_data()  # 平衡数据集
    #dataset._generate_random_data(60000)
    print(len(dataset))
    dataset._shuffle_data()  # 打乱数据集
    train_dataset, val_dataset = dataset.split_data(test_size=0.2)  # 20% 验证集
    
    # 创建训练和验证数据加载器
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
    
    # 初始化模型
    input_size = 24  # 每个音符的 one-hot 编码维度
    hidden_size = 64  # LSTM 隐藏层的神经元数量
    output_size = 1  # 输出维度，二分类任务
    
    model = MelodyLSTM(input_size, hidden_size, output_size)
    
    # 设置损失函数和优化器
    criterion = torch.nn.BCELoss()  # 二分类交叉熵损失
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # 开始训练
    num_epochs = 15  # 训练 10 轮
    for epoch in range(num_epochs):
        # 训练阶段
        train(model, train_loader, criterion, optimizer, num_epochs=1)
        
        # 验证阶段
        val_loss, val_accuracy = validate(model, val_loader, criterion)
        
        # 输出验证结果
        print(f"Validation Loss: {val_loss:.4f}, Validation Accuracy: {val_accuracy:.2f}%")
        torch.save(model.state_dict(), f"models_iter2/checkpoint_{epoch+1}.pt")
    
    print("Training complete and model saved!")

if __name__ == '__main__':
    main()
