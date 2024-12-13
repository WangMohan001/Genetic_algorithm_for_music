from genetic.fitness.fitness import Fitness
from genetic.item.music_piece import MusicPiece
import numpy as np

class FitnessChineseMusic(Fitness):
    def __init__(self, OmegaMode: float = 0.1, OmegaMelody: float = 0.3, OmegaTonic: float = 0.3):
        super().__init__()

        self.OmegaMode = OmegaMode  # 调式的加权系数
        self.OmegaMelody = OmegaMelody  # 旋律波动性的加权系数
        self.OmegaTonic = OmegaTonic  # 音程平缓性的加权系数
        self.OutOfKeyWeight = 1;
        # 调式相关
        self.tonic = 0  # 假设主音为 0
        self.major_stable_notes = [-10, -8, -5, -3, 0, 2, 4, 7, 9]
        self.minor_stable_notes = [-9, -7, -5, -2, 0, 3, 5, 7, 10]  # 稳定音（例如 C 大调中的音符）
        

    def evaluate(self, music_piece):
        notes = music_piece.get_notes()
        if len(notes) == 0 or all(np.isnan(note[0]) for note in notes):
            return float('-inf')  # 无效片段

        fitness = 0
        fitness += self.fitness_mode(notes)    # 调式评分
        fitness += self.fitness_melody(notes)  # 旋律波动性评分
        fitness += self.fitness_tonic(notes)   # 音程平缓性评分
        fitness += self.OutOfKeyPenalty(notes)
        
        return fitness

    def fitness_mode(self, notes: np.ndarray):
        """
        计算旋律是否符合调式的适应度，评估主音和稳定音的使用。
        """
        tonic_count = 0
        major_stable_count = 0
        minor_stable_count = 0
        total_notes = len(notes)

        for note in notes:
            if note[0] == self.tonic:
                tonic_count += 1
            if note[0] in self.major_stable_notes:
                major_stable_count += 1
            if note[0] in self.minor_stable_notes:
                minor_stable_count += 1

        tonic_ratio = tonic_count 
        stable_ratio = max(major_stable_count, minor_stable_count)

        mode_fitness = 3 * tonic_ratio + stable_ratio  # 两者加权
        return self.OmegaMode * mode_fitness

    def fitness_melody(self, notes: np.ndarray):
        """
        计算旋律的波动性，确保大跳前有反向运动。
        """
        melody_fitness = 0
        for i in range(2, len(notes)):
            interval = abs(notes[i][0] - notes[i-1][0])
            
            if interval > 4:  # 大跳
                prev_interval = abs(notes[i-1][0] - notes[i-2][0])
                if prev_interval > interval:  # 有反向运动
                    melody_fitness += 1
                else:
                    melody_fitness -= 1
        
        return self.OmegaMelody * melody_fitness

    def fitness_tonic(self, notes: np.ndarray):
        """
        计算旋律中的二度和三度音程的使用情况，确保旋律平缓。
        """
        tonic_fitness = 0
        tonic_intervals = [1, 2, 3, 4]  # 二度和三度音程
        total_intervals = 0
        tonic_intervals_count = 0

        for i in range(1, len(notes)):
            interval = abs(notes[i][0] - notes[i-1][0])
            if interval in tonic_intervals:
                tonic_intervals_count += 1
            total_intervals += 1

        return self.OmegaTonic * tonic_intervals_count
    
    def OutOfKeyPenalty(self, notes: np.ndarray):
        """
        惩罚不属于目标调性音符。
        """
        penalty_major = 0
        penalty_minor = 0
        major_scale = np.array([-10, -8, -7, -5, -3, -1, 0, 2, 4, 5, 7, 9, 11])
        minor_scale = np.array([-10, -9, -7, -5, -4, -2, 0, 2, 3, 5, 7, 8, 10])
        key_notes = {0, 2, 4, 5, 7, 9, 11}  # 大调内的音符编号（以C调为例）
        for note in notes:
            if note[0] not in major_scale:
                penalty_major -= self.OutOfKeyWeight
            if note[0] not in minor_scale:
                penalty_minor -= self.OutOfKeyWeight
        return max(penalty_major, penalty_minor)
