from genetic.item.music_piece import MusicPiece
from abc import ABC, abstractmethod
import random

#base class for crossover functions
class Crossover(ABC):
    def __init__(self):
        pass

    #crossover two music pieces
    def crossover(self, music_piece1: MusicPiece, music_piece2: MusicPiece ) -> tuple[MusicPiece, MusicPiece]:
        Crossover_operators = [self.one_point_crossover, self.two_point_crossover]
    
        weights = [0.5, 0.5]  # 保持这两个选择的平等概率
        # 使用 random.choices 选择一个交叉操作函数,uniform_crossover没有加 加了之后虽然fitness提高，但是得到的音乐片段会很奇怪
        chosen_crossover = random.choices(Crossover_operators, weights)[0]  # 取第一个元素
    
        return chosen_crossover(music_piece1,music_piece2)
    
    def one_point_crossover(self, music_piece1: MusicPiece, music_piece2: MusicPiece):
        length1=music_piece1.get_length()
        length2=music_piece2.get_length()
        point = random.randint(1, min(length1,length2)-1)
        child_1 = music_piece1.get_part(0,point)
        child_1_2=music_piece2.get_part(point,length2)
        child_1.append(child_1_2)
        child_2 = music_piece2.get_part(0,point)
        child_2_2=music_piece1.get_part(point,length1)
        child_2.append(child_2_2)
        return child_1, child_2

    def two_point_crossover(self, music_piece1: MusicPiece, music_piece2: MusicPiece):
        length1=music_piece1.get_length()
        length2=music_piece2.get_length()
        point_1 = random.randint(0, min(length1, length2) - 1)
    
        point_2 = random.randint(point_1 + 1, min(length1, length2)) 
        child_1=music_piece1.get_part(0,point_1)
        child_1_2=music_piece2.get_part(point_1,point_2)
        child_1_3=music_piece1.get_part(point_2,length1)
        child_1.append(child_1_2)
        child_1.append(child_1_3)
        
        child_2=music_piece2.get_part(0,point_1)
        child_2_2=music_piece1.get_part(point_1,point_2)
        child_2_3=music_piece2.get_part(point_2,length2)
        child_2.append(child_2_2)
        child_2.append(child_2_3)
        return child_1, child_2

    def uniform_crossover(self, music_piece1: MusicPiece, music_piece2: MusicPiece):
        length1=music_piece1.get_length()
        length2=music_piece2.get_length()
        
        total_piece=music_piece1
        total_piece.append(music_piece2)
        pool =total_piece.get_notes()
        # 打乱音符池
        random.shuffle(pool)
        
        child_notes_1 = pool[:length1]
        child_notes_2 = pool[length1:]
        
        child_1=MusicPiece(length1,music_piece1.pace,music_piece1.base_pitch,music_piece1.beat)
        child_1.notes=child_notes_1
        child_2=MusicPiece(length2,music_piece2.pace,music_piece2.base_pitch,music_piece2.beat)
        child_2.notes=child_notes_2
        return child_1,child_2
