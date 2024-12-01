import fractions
from typing import Counter
from genetic.fitness.fitness import Fitness
from genetic.item.music_piece import MusicPiece
import numpy as np

class CompositeFitness3(Fitness):
    def __init__(self):
        pass

    def calculate_intervals(self,music_piece:MusicPiece):
        # 计算旋律中相邻音符的音程
        intervals = []
        for i in range(1, len(music_piece.notes)):
            pitch1 = music_piece.notes[i-1][0]
            pitch2 = music_piece.notes[i][0]
            interval = abs(pitch2 - pitch1)  # 计算音程
            intervals.append(interval)
        return intervals
    
    def Movement_by_Step(self, music_piece: MusicPiece):
        # 音程步进
        val=0.0
        intervals = self.calculate_intervals(music_piece)  # 获取所有音程
        for interval in intervals:
            if interval in [1, 2]: 
                val+=1
        return val/len(intervals)
    
    def Contour_Direction(self,music_piece:MusicPiece):
        #轮廓方向
        intervals =self.calculate_intervals(music_piece) 
        rising_intervals = sum(1 for interval in intervals if interval > 0)  # 上升的音程数
        total_intervals = len(intervals)
        rising_ratio=rising_intervals / total_intervals if total_intervals > 0 else 0
        score = 0.0        
        if rising_ratio > 0.6:
            score -= 0.3  # 上升趋势过强，可能减分
        elif rising_ratio > 0.4:
            score += 0.3  # 合适的上升比例，适当加分
        elif rising_ratio < 0.4:
            score -= 0.3  # 上升比例过低，旋律可能过于平稳，减分
        return score

        
    def Dissonant_Intervals(self,music_piece:MusicPiece):
        #不协和音程比例
        notes = music_piece.get_notes()
        pitches = [note[0] for note in notes if note[0] > 0]
        if len(pitches) < 2:
            return 0.0
        intervals =self.calculate_intervals(music_piece)
        score=0
        for interval in intervals:
            if interval == 10:
                score+=1.5
            elif interval in [6, 11] or interval >= 13:
                score+=1
            else:
                score+=0
        return 1-score/len(intervals)
        
    def Contour_Stability(self, music_piece: MusicPiece):
        #轮廓稳定性
        notes = music_piece.get_notes()
        intervals = [notes[i+1][0] - notes[i][0] for i in range(len(notes) - 1)]  # 计算相邻音符之间的音程差
        same_direction = 0  # 计数连续的方向相同的音程
        total_intervals = len(intervals)  # 音程总数
        for i in range(1, len(intervals)):
            if (intervals[i] > 0 and intervals[i-1] > 0) or (intervals[i] < 0 and intervals[i-1] < 0):
                same_direction += 1
        return same_direction / total_intervals
        
    
    def Climax_Strength(self, music_piece: MusicPiece):
        #高潮强度
        notes = music_piece.get_notes()
        pitches = [note[0] for note in notes]
        climax_pitch = max(pitches)  # 假设高潮音符为音高最高的音符
        climax_count = pitches.count(climax_pitch)
        if climax_count>2:
            return -0.15
        else:
            return 0.15
    
    def pitch_variety(self,music_piece:MusicPiece):
        #音高多样性
        notes = music_piece.get_notes()
        pitches = [note[0] for note in notes if note[0] > 0]
        if len(pitches) == 0:  # 如果没有音符，返回 0
            return 0.0
        distinct_pitches = len(set(pitches))
        return distinct_pitches / len(pitches)
    
    
    def Rhythmic_Variety(self, music_piece: MusicPiece):
        #旋律多样性
        notes = music_piece.get_notes()
        durations = set(note[1] for note in notes)  # 获取所有不同的音符持续时间
        return len(durations) / 16  # 假设最大节奏值为16（从半音符到全音符）
    '''  
    def Rest_Density(self,music_piece:MusicPiece):
        score=0.0
        rest_count=0
        notes = music_piece.get_notes()
        for note in notes:
            if np.isnan(note[0]):  # 判断是否为休止符（即 NaN）
                rest_count += 1
        rest_radio=rest_count/music_piece.get_length()
        if rest_radio >0.2:
            score-=0.2
        elif rest_radio>0.05 and rest_radio<0.15:
            score+=0.1
        return score
    '''
    #evaluate 将含nan的片段视为无效片段       

    def repeated_pitch_patterns_3(self,music_piece:MusicPiece):
        notes = music_piece.notes
        notes = [tuple(note) for note in notes]
        patterns = [tuple(notes[i:i+3]) for i in range(len(notes) - 2)]       # 统计重复的三音符组合
        pattern_counts = Counter(patterns)
        # 返回重复频率
        if len(patterns) == 0:  # 避免除以 0 的情况
            return 0
        return sum(count > 1 for count in pattern_counts.values()) / len(patterns)

    def repeated_pitch_patterns_4(self,music_piece:MusicPiece):
        # 创建四音符组合
        notes = music_piece.notes
        # 确保每个音符的数据被转换为元组
        notes = [tuple(note) for note in notes]
        patterns = [tuple(notes[i:i+4]) for i in range(len(notes) - 3)]
        pattern_counts = Counter(patterns) 
        if len(patterns) == 0:  # 避免除以 0 的情况
            return 0
        return sum(count > 1 for count in pattern_counts.values()) / len(patterns)
    
    def pitch_balance(self, music_piece: MusicPiece):
        score=1.0
        notes = music_piece.get_notes()
        low_pitch_count = 0  # 低音符的计数
        high_pitch_count = 0  # 高音符的计数
        total_count = len(notes)  # 音符总数
        
        # 遍历所有音符
        for note in notes:
            if note[0]< 0:
                low_pitch_count += 1  # 低音符计数
            elif note[0] >0:
                high_pitch_count += 1  # 高音符计数

        if abs(high_pitch_count-low_pitch_count)>total_count/2:
            score-=0.8
        elif abs(high_pitch_count-low_pitch_count)>total_count/3:
            score-=0.5
        if abs(high_pitch_count-low_pitch_count)<3:
            score+=0.8
        return score
    
    def duration_balance(self, music_piece: MusicPiece):
        notes = music_piece.get_notes()
        durations = [note[1] for note in notes if note[1] > 0]  # 排除无效的持续时间（例如休止符）
        
        if len(durations) == 0:
            return 1.0  # 如果没有有效音符，返回最优分数
        
        mean_duration = sum(durations) / len(durations)
        variance = sum((duration - mean_duration) ** 2 for duration in durations) / len(durations)
        stddev_duration = variance ** 0.5  # 持续时间的标准差
        if stddev_duration < 2:  # 假设标准差小于2是较为平衡的
            return 1.0  # 音符持续时间平衡
        elif stddev_duration < 4:  # 稍微有差异，降低分数
            return 0.6
        else:  # 如果标准差较大，分数较低
            return 0.3

    def evaluate(self, music_piece: MusicPiece) -> float:

        music_notes=music_piece.notes
        
        if len(music_notes) == 0 or np.any(np.isnan(music_notes[:, 0])):
            return float('-inf')  
        
        high_pitch=0
        low_pitch=0
        for note in music_notes:
            if note[0]<-15:
                low_pitch+=1
            elif note[0]>15:
                high_pitch+=1

        score=self.Movement_by_Step(music_piece)+self.Climax_Strength(music_piece)+\
        self.Contour_Direction(music_piece)+self.Contour_Stability(music_piece)+\
        self.Dissonant_Intervals(music_piece)+self.pitch_variety(music_piece)+\
        self.Rhythmic_Variety(music_piece)+\
        self.repeated_pitch_patterns_3(music_piece)+self.repeated_pitch_patterns_4(music_piece)+\
        self.pitch_balance(music_piece)
        length_penalty = 0.01 * len(music_piece.notes)  #惩罚过长的片段
        score -= length_penalty  # 减少总分以惩罚长片段
        #score-=0.01*(high_pitch+low_pitch) #惩罚过高过低pitch
        return score



def creat_reference():
    music_piece = MusicPiece(6, 1, 60, 4)
    music_piece.notes=[(11, 1), (12, 1), (16, 1), (14, 1), (12, 1), (12, 2)]
    return music_piece


class Fitness_example2(Fitness):
    def __init__(self,reference_piece:MusicPiece=creat_reference(),bad_notes:list=[50,51,52],w1:float=0.7,w2:float=0,w3:float=0.5,w4:float=0.7,sigma:float=0.1):
        #初始化
        self.reference_piece=reference_piece
        self.w1=w1
        self.w2=w2
        self.w3=w3
        self.w4=w4
        self.sigma=sigma
        self.bad_notes=bad_notes
        

    def same_len(self,reference_notes,music_notes):
        if len(music_notes) > len(reference_notes):
            reference_notes = np.tile(reference_notes, (len(music_notes) // len(reference_notes) + 1, 1))[:len(music_notes)]
        elif len(music_notes) < len(reference_notes):
            music_notes = np.tile(music_notes, (len(reference_notes) // len(music_notes) + 1, 1))[:len(reference_notes)]
        return reference_notes,music_notes


    def pitch_diff(self, reference_notes, music_notes):
       
        pitch_differences = np.abs(reference_notes[:,0] - music_notes[:, 0])
        
        # 计算音高相似度，取差异的均值
        pitch_similarity = 1 - np.mean(pitch_differences)
        return pitch_similarity 

    def beat_diff(self,reference_notes, music_notes):
        return 0
    
    def duration_diff(self, reference_notes, music_notes):
        # 计算节奏差异
        duration_differences = np.abs(reference_notes[:, 1] - music_notes[:, 1])
        duration_similarity = 1 - np.mean(duration_differences)
        
        return duration_similarity 

    
    def bad_note_diff(self,music_notes):
        bad_note_count = np.sum(np.isin(music_notes[:, 0], self.bad_notes))
        return -bad_note_count
    



    def evaluate(self, music_piece: MusicPiece) -> float:
        val=0
        reference_notes = self.reference_piece.get_notes()
        music_notes = music_piece.get_notes()
       
        if len(music_notes) == 0 or np.any(np.isnan(music_notes[:, 0])):
            return float('-inf')  # 无效片段
        reference_notes,music_notes=self.same_len(reference_notes,music_notes)

        val=self.w1*self.pitch_diff(reference_notes,music_notes)+\
                self.w2*self.beat_diff(reference_notes,music_notes)+\
                self.w3*self.duration_diff(reference_notes,music_notes)+\
                    1/self.sigma*self.bad_note_diff(music_notes)
       
        return val