from genetic.fitness.fitness import Fitness
from genetic.item.music_piece import MusicPiece
import numpy as np

#给定一个参考个体
segment = [60, 63, 64, 60, 69, 0, 67, 69, 300, 0, 700, 0, 60, 300, 71,60, 63, 64, 60, 69, 0, 67, 69, 300, 0, 700, 0, 60, 300, 71]
def creat_reference1(rp_length:int =len(segment),rp_pace:float=0.5,rp_base_pitch:int =60,rp_beat:int =4):
    reference_piece=MusicPiece(rp_length,rp_pace,rp_base_pitch,rp_beat)
    for i, note in enumerate(segment):
            if note == 0:  # 表示休止符
                reference_piece.notes[i] = [0, int(rp_pace * 1000)]
            elif note == 300 or note == 700:  # 表示节奏调整
                reference_piece.notes[i] = [0, note]
            else:
                reference_piece.notes[i] = [note, int(rp_pace * 1000)]  # 音符和持续时间
    return reference_piece

#随机生成参考个体
def creat_reference2(length=32, base_pitch=60, pace=0.5, beat=4):
    music_piece = MusicPiece(length, pace, base_pitch, beat)
    # 随机生成音符
    for i in range(length):
        # 随机生成音高 (可以调整范围)
        pitch = np.random.choice(range(60, 73))  # 假设音高在60到72之间
        # 随机生成持续时间
        duration = np.random.choice([300, 700, int(pace * 1000)])  # 可以是固定值或按节奏调整
        # 随机生成休止符
        if np.random.random() < 0.2:  # 20%的概率是休止符
            pitch = 0
            duration = int(pace * 1000)  # 默认休止符持续时间
        music_piece.notes[i] = [pitch, duration]
    return music_piece

#这是有参考个体的fitness函数
class Fitness_example2(Fitness):
    def __init__(self,reference_piece:MusicPiece=creat_reference2(),bad_notes:list=[50,51,52],w1:float=0.4,w2:float=0,w3:float=0.3,w4:float=0.3,sigma:float=0.1):
        #初始化
        self.reference_piece=reference_piece
        self.w1=w1
        self.w2=w2
        self.w3=w3
        self.w4=w4
        self.sigma=sigma
        self.bad_notes=bad_notes
        

    def normalize_notes(self,notes):
        max_pitch = np.max(notes[:, 0])
        min_pitch = np.min(notes[:, 0])
        max_duration = np.max(notes[:, 1])
        min_duration = np.min(notes[:, 1])
        
        # 将时值归一化到 [0, 1] 范围
        if max_pitch!=min_pitch:
            notes[:, 0] = (notes[:, 0] - min_pitch) / (max_pitch - min_pitch) if max_pitch != min_pitch else notes[:, 0]
        if max_duration!=min_duration:
            notes[:, 1] = (notes[:, 1] - min_duration) / (max_duration - min_duration) if max_duration != min_duration else notes[:, 1]   
        return notes
    
    def same_len(self,reference_notes,music_notes):
        if len(music_notes) > len(reference_notes):
            reference_notes = np.tile(reference_notes, (len(music_notes) // len(reference_notes) + 1, 1))[:len(music_notes)]
        elif len(music_notes) < len(reference_notes):
            music_notes = np.tile(music_notes, (len(reference_notes) // len(music_notes) + 1, 1))[:len(reference_notes)]
        return reference_notes,music_notes


    def pitch_diff(self, reference_notes, music_notes):
    # 计算音符音高的差异
        music_notes = np.nan_to_num(music_notes, nan=0)  # 将 NaN 转换为 0
        valid_indices = ~np.isnan(reference_notes[:, 0]) & ~np.isnan(music_notes[:, 0])  # 筛选有效音符
        
        # 计算音高差异
        pitch_differences = np.abs(reference_notes[valid_indices, 0] - music_notes[valid_indices, 0])
        
        # 添加一个小扰动，使相似度在所有迭代中都有变化
        pitch_similarity = 1 - np.mean(pitch_differences)
        
        return max(0, min(1, pitch_similarity)) 

    def beat_diff(self,reference_notes, music_notes):
        return 0
    def duration_diff(self, reference_notes, music_notes):
        # 计算节奏差异
        duration_differences = np.abs(reference_notes[:, 1] - music_notes[:, 1])
        
        # 直接对时值差异进行求和并计算相似度
        # 由于已经归一化，因此无需再除以最大差异
        duration_similarity = 1 - (np.sum(duration_differences) / len(reference_notes))
        
        # 确保返回的相似度在合理范围内
        return max(0, min(1, duration_similarity))  # 保证相似度在[0,1]区间内



    
    def rest_diff(self,reference_notes,music_notes):
        #计算休止符差异
        rest_matches = np.sum(
            (reference_notes[:, 0] == 0) == (music_notes[:, 0] ==0)
        )
        rest_similarity = rest_matches / len(reference_notes)
        return rest_similarity
    
    def bad_note_diff(self,music_notes):
        bad_note_count = np.sum(np.isin(music_notes[:, 0], self.bad_notes))
        return 1 - (bad_note_count / len(music_notes))



    def evaluate(self, music_piece: MusicPiece) -> float:
        val=0
        reference_notes = self.reference_piece.get_notes()
        music_notes = music_piece.get_notes()
        reference_notes=self.normalize_notes(reference_notes)
        music_notes=self.normalize_notes(music_notes)
        if len(music_notes) == 0 or np.any(np.isnan(music_notes[:, 0])):
            return float('-inf')  # 无效片段
        reference_notes,music_notes=self.same_len(reference_notes,music_notes)
        total_weight = self.w1 + self.w2 + self.w3 + self.w4
        val=(self.w1*self.pitch_diff(reference_notes,music_notes)+\
                self.w2*self.beat_diff(reference_notes,music_notes)+\
                self.w3*self.duration_diff(reference_notes,music_notes)+\
                    self.w4*self.rest_diff(reference_notes,music_notes))/total_weight
        #print(self.pitch_diff(reference_notes,music_notes),self.duration_diff(reference_notes,music_notes))
        return val