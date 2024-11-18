from genetic.fitness.fitness import Fitness
from genetic.item.music_piece import MusicPiece
import numpy as np


def create_reference_piece():
    # 定义参考音乐片段的长度、步伐和基准音高
    length = 8  # 例如参考片段有16个音符
    pace = 1.0  
    base_pitch = 60  

    reference = MusicPiece(length, pace, base_pitch)

    pitches = [60, 62, 64, 65, 67, 69, 71, 72]
    durations = [1, 1, 1, 1, 1, 1, 1, 1]
    
    for pitch, duration in zip(pitches, durations):
        reference.add_note(pitch, duration)
    
    return reference

def normalize_notes(notes):
    max_pitch = np.max(notes[:, 0])
    min_pitch = np.min(notes[:, 0])
    max_duration = np.max(notes[:, 1])
    min_duration = np.min(notes[:, 1])
    
    # 将音高归一化到 [0, 1] 范围
    notes[:, 0] = (notes[:, 0] - min_pitch) / (max_pitch - min_pitch) if max_pitch != min_pitch else notes[:, 0]
    
    # 将时值归一化到 [0, 1] 范围
    notes[:, 1] = (notes[:, 1] - min_duration) / (max_duration - min_duration) if max_duration != min_duration else notes[:, 1]
    
    return notes

class Fitness_example(Fitness):
    def __init__(self):
        pass

    def evaluate(self, music_piece: MusicPiece) -> float:
        reference_notes = create_reference_piece().get_notes()
        music_notes = music_piece.get_notes()
        # 使用normalize对参考音符和生成的音符进行处理
        reference_notes = normalize_notes(reference_notes.copy())
        music_notes = normalize_notes(music_notes.copy())

        # 使reference_notes和music_notes具有相同的长度
        if len(music_notes) > len(reference_notes):
            reference_notes = np.tile(reference_notes, (len(music_notes) // len(reference_notes) + 1, 1))[:len(music_notes)]
        elif len(music_notes) < len(reference_notes):
            music_notes = np.tile(music_notes, (len(reference_notes) // len(music_notes) + 1, 1))[:len(reference_notes)]

        pitch_diff = np.sum((music_notes[:, 0] - reference_notes[:, 0])**2)
        duration_diff = np.sum((music_notes[:, 1] - reference_notes[:, 1])**2)

        alpha = 0.5
        beta = 0.5 
        fitness=-(alpha * pitch_diff + beta * duration_diff)
        
        return fitness 
