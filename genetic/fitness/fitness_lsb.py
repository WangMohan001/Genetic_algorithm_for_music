from genetic.fitness.fitness import Fitness
from genetic.item.music_piece import MusicPiece
import numpy as np

class CompositeFitness2(Fitness):
    def __init__(self, LargestInterval: int = 6, LongnoteLen: int = 2, Speed: int = 0, Contor: int = 3):
        super().__init__()
        self.LargestInterval = LargestInterval
        self.maxlen = Contor
        self.speed = Speed
        self.ll = LongnoteLen
        
    def evaluate(self, music_piece):
        notes = music_piece.get_notes()
        val = 0
        if len(notes) == 0:
            return float('-inf')  # 无效片段
        for i in notes:
            if np.isnan(i[0]):
                return float('-inf')  # 无效片段
        val += self.IntervalPenalty(notes)
        val += self.PatternMatching(notes)
        val += self.Suspensions(notes)
        val += self.Downbeat(notes)
        val += self.Halfbar(notes)
        val += self.Longnote(notes)
        val += self.Contour(notes)
        val += self.Speed(notes)
        return val/600
    
    def ischord(self,note):
        '''
        判断一个音符是不是和弦
        '''
        return False
    def IntervalPenalty(self, notes: np.ndarray):
        '''
        对过高的音程差进行惩罚。
        '''
        ret = 0
        for i in range(1,len(notes)):
            if abs(notes[i,0]-notes[i-1,0]) >= self.LargestInterval:
                ret -= 20*(abs(notes[i,0]-notes[i-1,0])-self.LargestInterval)
        return ret
    def PatternMatching(self, notes: np.ndarray):
        '''
        对特定的特征进行奖励。
        考虑到文章中并没有给出特定的pattern，这部分暂时留白。
        '''
        pass
        return 0
    def Suspensions(self, notes: np.ndarray):
        '''
        对特定的悬浮和弦进行奖励和惩罚。
        难评，我们这里好像没有和弦
        '''
        pass
        return 0
    def Downbeat(self, notes: np.ndarray):
        '''
        对每个小节的第一个音进行奖励和惩罚。
        '''
        ret = 0
        currlen = 0
        for i in range(len(notes)):
            if currlen <= 0 and currlen + notes[i,1] >= 0:
                if notes[i,0] == 0:
                    ret += 10
            currlen += notes[i,1]
            if currlen >= 4:
                currlen -= 4
        return ret
    def Halfbar(self, notes: np.ndarray):
        '''
        对每个小节的次强音进行奖励和惩罚。
        '''
        ret = 0
        currlen = 0
        for i in range(len(notes)):
            if currlen <= 2 and currlen + notes[i,1] >= 2:
                if notes[i,0] == 0:
                    ret += 5
            currlen += notes[i,1]
            if currlen >= 4:
                currlen -= 4
        return ret
    def Longnote(self, notes: np.ndarray):
        '''
        对每个音符的长度进行奖励和惩罚。
        '''
        ret = 0
        for i in range (0,len(notes)):
            if notes[i,1] > self.ll:
                if self.ischord(notes[i]):
                    ret += 10
                elif notes[i,0] == 0:
                    ret -= 20
                else:
                    ret += 5
        return ret
    def Contour(self, notes: np.ndarray):
        '''
        对轮廓进行奖励
        '''
        ret = 0
        for i in range (0,len(notes)):
            for j in range (0,i):
                k = 0
                same = 0
                while j+k<i and i+k < len(notes) and k < self.maxlen:
                    if notes[j,0]==notes[i,0]:
                        same += 1
                        ret = max(ret, same*30)
                    else:
                        break
                    k += 1
                        
        return ret
    def Speed(self, notes: np.ndarray):
        '''
        对速度进行奖励
        '''
        ret = 0
        self.bonus = 0
        if self.speed == 0:
            self.bonus = 1
        if self.speed == 1:
            self.bonus = 0.5
        if self.speed == 2:
            self.bonus = 0.25
        for i in range (0,len(notes)):
            if notes[i,1] == self.bonus:
                ret += 5
        return ret
        
