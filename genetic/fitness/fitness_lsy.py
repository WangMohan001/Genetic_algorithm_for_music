import fractions
from typing import Counter
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
    def __init__(self,reference_piece:MusicPiece=creat_reference2(),bad_notes:list=[50,51,52],w1:float=0.3,w2:float=0.1,w3:float=0.4,w4:float=0.2,sigma:float=0.1):
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
            notes[:, 0] = (notes[:, 0] - min_pitch) /float((max_pitch - min_pitch))
        if max_duration!=min_duration:
            notes[:, 1] = (notes[:, 1] - min_duration) /float((max_duration - min_duration))
        return notes
    
    def same_len(self,reference_notes,music_notes):
        if len(music_notes) > len(reference_notes):
            reference_notes = np.tile(reference_notes, (len(music_notes) // len(reference_notes) + 1, 1))[:len(music_notes)]
        elif len(music_notes) < len(reference_notes):
            music_notes = np.tile(music_notes, (len(reference_notes) // len(music_notes) + 1, 1))[:len(reference_notes)]
        return reference_notes,music_notes


    def pitch_diff(self, reference_notes, music_notes):

        pitch_differences = np.abs(reference_notes[:, 0] - music_notes[:, 0])
        return np.mean(pitch_differences) 

    def beat_diff(self,reference_notes, music_notes):
        return 0
    
    def duration_diff(self, reference_notes, music_notes):
        # 计算节奏差异
        duration_differences = np.abs(reference_notes[:, 1] - music_notes[:, 1])
        return  np.mean(duration_differences)



    
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
        #reference_notes = self.normalize_notes(reference_notes)
        #music_notes = self.normalize_notes(music_notes)
        if len(music_notes) == 0 or np.any(np.isnan(music_notes[:, 0])):
            return float('-inf')  # 无效片段
        reference_notes,music_notes=self.same_len(reference_notes,music_notes)
        val1=self.pitch_diff(reference_notes,music_notes)
        val2=self.beat_diff(reference_notes,music_notes)
        val3=self.duration_diff(reference_notes,music_notes)
        val4=self.rest_diff(reference_notes,music_notes)
        val = (self.w1 * val1 + self.w2 * val2 + self.w3 * val3 + self.w4 * val4)
    
        #print(self.pitch_diff(reference_notes,music_notes),self.duration_diff(reference_notes,music_notes))
        return val
'''
快节奏，情感强烈的音乐：音高范围广，高音符密度，节奏多样性强，高潮音符强烈，轮廓方向多变，轮廓稳定性低
慢节奏，安静的音乐：与上面相反
悲伤的：轮廓方向主要下降，轮廓稳定性中等偏高
欢快的：轮廓方向上升为主，高潮音符温和，协和音程比例高
'''
'''
type = input("Please choose the type for the music (classical/early/nursery): ").strip().lower()
    while type not in ['classical', 'early','nursery']:
        print("Invalid input! ")
        type = input("Please choose the type for the music (classical/early/nursery): ").strip().lower()
'''#可以将其添加到main.py中实现一个简单的交互
class CompositeFitness3(Fitness):
    def __init__(self,type:str="classical"):
        #初始化
        self.type = type.lower()  # 确保输入是小写
        self.weights = self.get_weights_for_emotion()

    def get_weights_for_emotion(self):
        # 根据类型调整权重
        if self.type == 'classical':
            # 对于classical
            return {
                "pitch_range": 0.15,
                #"dissonant_intervals": -0.5,
                #"contour_stability": 1.0,
                "note_density": 0.20,
                #"rhythmic_variety": 0.6,
                #"contour_direction": 0.1,
                "Repeated_Rhythm_Patterns_of_3":0.05,
                "Repeated_Rhythm_Patterns_of_4":0.05,
                "Movement_by_Step":0.18,
                "repeated_pitch_patterns_3":0.07,
                "repeated_pitch_patterns_4":0.05,
                "repeated_duration":0.15
                

            }
        elif self.type == 'early':
            # early
            return {
                "pitch_range": 0.12,
                #"dissonant_intervals": -0.5,
                #"contour_stability": 1.0,
                "note_density": 0.18,
                #"rhythmic_variety": 0.6,
                #"contour_direction": 0.1,
                "Repeated_Rhythm_Patterns_of_3":0.08,
                "Repeated_Rhythm_Patterns_of_4":0.07,
                "Movement_by_Step":0.15,
                "repeated_pitch_patterns_3":0.10,
                "repeated_pitch_patterns_4":0.08,
                "repeated_duration":0.15
            }
        elif self.type=='nursery':
            # nursery
            return {
                "pitch_range": 0.12,
                #"dissonant_intervals": -0.5,
                #"contour_stability": 1.0,
                "note_density": 0.15,
                #"rhythmic_variety": 0.6,
                #"contour_direction": 0.1,
                "Repeated_Rhythm_Patterns_of_3":0.10,
                "Repeated_Rhythm_Patterns_of_4":0.08,
                "Movement_by_Step":0.15,
                "repeated_pitch_patterns_3":0.10,
                "repeated_pitch_patterns_4":0.08,
                "repeated_duration":0.12
            }
    
    def calculate_intervals(self,music_piece:MusicPiece):
        # 计算旋律中相邻音符的音程
        intervals = []
        for i in range(1, len(music_piece.notes)):
            pitch1 = music_piece.notes[i-1][0]
            pitch2 = music_piece.notes[i][0]
            interval = abs(pitch2 - pitch1)  # 计算音程
            intervals.append(interval)
        return intervals
    
    def repeated_pitch_patterns_3(self,music_piece:MusicPiece):
        # 创建三音符组合
        notes = music_piece.notes
        # 确保每个音符的数据被转换为元组
        notes = [tuple(note) for note in notes]
        patterns = [tuple(notes[i:i+3]) for i in range(len(notes) - 2)]
        
        # 统计重复的三音符组合
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
        # 返回重复频率
        if len(patterns) == 0:  # 避免除以 0 的情况
            return 0
        return sum(count > 1 for count in pattern_counts.values()) / len(patterns)
    
    def repeated_duration(self,music_piece:MusicPiece):
        # 统计时值重复的情况
        durations=music_piece.notes[:,1]
        duration_counts = Counter(durations)
        # 计算重复的时值占比
        total = len(durations)
        repeated = sum(count > 1 for count in duration_counts.values())
        return repeated / total


    def Movement_by_Step(self, music_piece: MusicPiece):
        # 音程步进比例
        intervals = self.calculate_intervals(music_piece)  # 获取所有音程
        diatonic_step_count = 0  # 音阶步进音程计数
        total_intervals = len(intervals)  # 总音程数

        for interval in intervals:
            if interval in [1, 2]: 
                diatonic_step_count += 1

        return diatonic_step_count / total_intervals if total_intervals > 0 else 0

    def pitch_variety(self,music_piece:MusicPiece):
        #音高多样性
        notes = music_piece.get_notes()
        pitches = [note[0] for note in notes if note[0] > 0]
        if len(pitches) == 0:  # 如果没有音符，返回 0
            return 0.0
        distinct_pitches = len(set(pitches))
        return distinct_pitches / len(pitches)
    
    def pitch_range(self,music_piece:MusicPiece):
        #音高范围
        notes=music_piece.get_notes()
        pitches = [note[0] for note in notes if note[0] > 0]

        if len(pitches) == 0:  # 如果没有音符，返回 0
            return 0     
        max_pitch = max(pitches)
        min_pitch = min(pitches)

        return (max_pitch - min_pitch)/24
    
    def Dissonant_degree(self,interval: int)->float:
        if interval == 10:
            return 0.5
        elif interval in [6, 11] or interval >= 13:
            return 1.0
        else:
            return 0.0
        
    def Dissonant_Intervals(self,music_piece:MusicPiece):
        #不协和音程比例
        notes = music_piece.get_notes()
        pitches = [note[0] for note in notes if note[0] > 0]
        if len(pitches) < 2:
            return 0.0
        intervals = [abs(pitches[i] - pitches[i - 1]) for i in range(1, len(pitches))]
        total_dissonance = sum(self.Dissonant_degree(interval) for interval in intervals)

        return total_dissonance / len(intervals)
    
    def Contour_Stability(self, music_piece: MusicPiece):
        #轮廓稳定性
        notes = music_piece.get_notes()
        intervals = [notes[i+1][0] - notes[i][0] for i in range(len(notes) - 1)]  # 计算相邻音符之间的音程差
        same_direction = 0  # 计数连续的方向相同的音程
        total_intervals = len(intervals)  # 音程总数
        for i in range(1, len(intervals)):
            if (intervals[i] > 0 and intervals[i-1] > 0) or (intervals[i] < 0 and intervals[i-1] < 0):
                same_direction += 1
        return same_direction / total_intervals if total_intervals > 0 else 0
    
    def Climax_Strength(self, music_piece: MusicPiece):
        #高潮强度
        notes = music_piece.get_notes()
        pitches = [note[0] for note in notes]
        climax_pitch = max(pitches)  # 假设高潮音符为音高最高的音符
        climax_count = pitches.count(climax_pitch)
        return 1 / climax_count if climax_count > 0 else 0
    
    def Repeated_Rhythmic_Value(self, music_piece: MusicPiece):
        # 获取音符列表
        notes = music_piece.get_notes()
        intervals = [(notes[i - 1], notes[i]) for i in range(1, len(notes))]  # 获取音符配对

        repeated_duration_count = 0  # 重复节奏值计数
        total_intervals = len(intervals)  # 总音程数

        for note1, note2 in intervals:
            duration1, duration2 = note1[1], note2[1]  # 获取每个音符的持续时间
            if duration1 == duration2:  # 检查持续时间是否相同
                repeated_duration_count += 1

        # 返回重复节奏值比例
        return repeated_duration_count / total_intervals if total_intervals > 0 else 0

    def get_rhythm_ratios(self, durations):
        """将持续时间转化为相对比例序列"""
        durations = [float(d) for d in durations if isinstance(d, (int, float))]
    
        # 如果数据不足以计算比率，直接返回空元组
        if len(durations) < 2:
            return tuple()
        
        ratios = []
        for i in range(1, len(durations)):
            if durations[i - 1] != 0:  # 避免除以 0
                # 直接用浮点数计算比例
                ratio = durations[i] / durations[i - 1]
                ratios.append(ratio)
        return tuple(ratios)

    def Repeated_Rhythm_Patterns(self, music_piece: MusicPiece, pattern_length: int):
        """通用方法，计算指定长度的重复节奏模式比例"""
        notes = music_piece.get_notes()
        durations = [note[1] for note in notes]  # 提取音符时值

        if len(durations) < pattern_length + 1:  # 音符不足以构成模式
            return 0.0

        # 构建指定长度的节奏比例模式
        patterns = {}
        for i in range(len(durations) - pattern_length):
            pattern = self.get_rhythm_ratios(durations[i:i + pattern_length])
            if pattern in patterns:
                patterns[pattern] += 1
            else:
                patterns[pattern] = 1

        # 统计重复模式
        repeated_count = sum(1 for count in patterns.values() if count > 1)

        # 分母计算：总音符数 - pattern_length - 1
        denominator = len(durations) - pattern_length - 1
        return repeated_count / denominator if denominator > 0 else 0.0

    def Repeated_Rhythm_Patterns_of_3(self, music_piece: MusicPiece):
        """三音符重复节奏模式"""
        return self.Repeated_Rhythm_Patterns(music_piece, pattern_length=3)

    def Repeated_Rhythm_Patterns_of_4(self, music_piece: MusicPiece):
        """四音符重复节奏模式"""
        return self.Repeated_Rhythm_Patterns(music_piece, pattern_length=4)
    
    def Note_Density(self, music_piece: MusicPiece):
        #音符密度
        notes = music_piece.get_notes()
        quanta = music_piece.length  # 获取总量度数
        return len(notes) / quanta if quanta > 0 else 0
    
    def Rhythmic_Variety(self, music_piece: MusicPiece):
        #旋律多样性
        notes = music_piece.get_notes()
        durations = set(note[1] for note in notes)  # 获取所有不同的音符持续时间
        return len(durations) / 16  # 假设最大节奏值为16（从半音符到全音符）
    
    def Contour_Direction(self,music_piece:MusicPiece):
        #轮廓方向
        notes = music_piece.get_notes()
        intervals = [notes[i+1][0] - notes[i][0] for i in range(len(notes) - 1)]  # 计算相邻音符的音程差
        rising_intervals = sum(1 for interval in intervals if interval > 0)  # 上升的音程数
        total_intervals = len(intervals)
        return rising_intervals / total_intervals if total_intervals > 0 else 0

    def evaluate(self, music_piece: MusicPiece) -> float:

        # 计算每个特征的值
        pitch_range_value = self.pitch_range(music_piece)
        note_density_value = self.Note_Density(music_piece)
        Repeated_Rhythm_Patterns_of_3_value=self.Repeated_Rhythm_Patterns_of_3(music_piece)
        Repeated_Rhythm_Patterns_of_4_value=self.Repeated_Rhythm_Patterns_of_4(music_piece)
        Movement_by_Step_value=self.Movement_by_Step(music_piece)
        repeated_pitch_patterns_3_value=self.repeated_pitch_patterns_3(music_piece)
        repeated_pitch_patterns_4_value=self.repeated_pitch_patterns_4(music_piece)
        repeated_duration=self.repeated_duration(music_piece)
        # 计算总评分
        score = 0.0

        # 根据每个特征的值与权重计算总分
        score += self.weights["pitch_range"] * pitch_range_value
        score += self.weights["note_density"] * note_density_value
        score += self.weights["Repeated_Rhythm_Patterns_of_3"] * Repeated_Rhythm_Patterns_of_3_value
        score += self.weights["Repeated_Rhythm_Patterns_of_3"] * Repeated_Rhythm_Patterns_of_4_value
        score += self.weights["Movement_by_Step"] * Movement_by_Step_value
        score += self.weights["repeated_pitch_patterns_3"] * repeated_pitch_patterns_3_value
        score += self.weights["repeated_pitch_patterns_3"] * repeated_pitch_patterns_4_value
        score += self.weights["repeated_duration"] *repeated_duration

        total_weight = sum(abs(weight) for weight in self.weights.values())
        normalized_score = score / total_weight if total_weight > 0 else 0

        return normalized_score

           