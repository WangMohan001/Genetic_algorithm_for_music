import torch
import torch.nn as nn
import numpy as np
from genetic.fitness.fitness import Fitness
from genetic.item.music_piece import MusicPiece

from genetic.fitness.fitness_js import CompositeFitness as Fitness1
from genetic.fitness.fitness_ljh import FitnessChineseMusic as Fitness2
from genetic.fitness.fitness_lsb import CompositeFitness2 as Fitness3
from genetic.fitness.fitness_lstm import Fitness_LSTM as Fitness4
from genetic.fitness.fitness_lsy import CompositeFitness3 as Fitness5
from genetic.fitness.fitness_wmh import Fitness_neighbor as Fitness6

class MergedFitness(Fitness):
    def __init__(self):
        super().__init__()
        self.functions = []
        self.functions.append(Fitness1())
        self.functions.append(Fitness2())
        self.functions.append(Fitness3(Speed=2))
        self.functions.append(Fitness4())
        self.functions.append(Fitness5())
        self.functions.append(Fitness6())
        self.weights = [1,1,2,4,1,1]
        self.sigmoid = nn.Sigmoid()
        
    def evaluate(self, music_piece: MusicPiece) -> float:
        '''
        把所有人的适应度函数合并在一起。但是问题是，每个人的适应度函数值域都不一样，如果直接简单加起来的话效果是不好的。因此采用正则化，先把所有人的输出值都映射到0到1之间，然后再进行加权合并。
        因为表达的范围更多了，所以在权值选择合理的情况下，这个合并之后的适应度函数不会劣于每个人自己的适应度函数。
        '''
        ret = 0
        for i in range (6):
            val = self.functions[i].evaluate(music_piece)
            val = torch.tensor(val)
            val = self.sigmoid(val)
            val = val.item()
            val *= self.weights[i]
            ret += val
        
        '''
        我们希望得到的值越高越好，因此使用指数奖励
        '''
        return np.exp(ret-sum(self.weights)/2)
        