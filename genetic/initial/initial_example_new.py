from genetic.initial.initial import Initial
from genetic.item.music_piece import MusicPiece
import numpy as np
import random
class Initial_example(Initial):
    def __init__(self):
        pass

    def generate(self, population_size: int) -> [MusicPiece]:
        notes = []
        durations = []
        notes.append([0,0,7,7,9,9,7,5,5,4,4,2,2,0])#小星星
        durations.append([1,1,1,1,1,1,2,1,1,1,1,1,1,2])
        notes.append([4,4,5,7,7,5,4,2,0,0,2,4,2,0,0])#欢乐颂
        durations.append([1,1,1,1,1,1,1,1,1,1,1,1,1.5,0.5,1])
        notes.append([4,4,7,9,12,12,9,7,7,9,7,4,4,7,9,12,12,9,7,7,9,7])#茉莉花
        durations.append([1,0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0.5,2,1,0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0.5,2])
        notes.append([7,7,7,4,7,9,9,7,4,2,4,7,4,2,0,0,2,0])
        durations.append([1,1,1,0.5,0.5,1,1,2,1,0.5,0.5,1,0.5,0.5,1,0.5,0.5,2])
        notes.append([7,4,7,12,9,12,7,7,0,2,4,2,0,2])#送别
        durations.append([1,0.5,0.5,2,1,1,2,1,0.5,0.5,1,0.5,0.5,4])
        notes.append([7,4,7,12,11,9,12,7,7,2,4,5,-1,0])
        durations.append([1,0.5,0.5,1.5,0.5,1,1,2,1,0.5,0.5,1.5,0.5,4])
        notes.append([-3,-1,0,-3,0,-1,-3,-1,-8,-1,0,2,-1,2,2,0,-1,-3])#喀秋莎
        durations.append([1.5,0.5,1.5,0.5,1,0.5,0.5,1,1,1.5,0.5,1.5,0.5,0.5,0.5,0.5,0.5,2])
        notes.append([7,0,2,4,5,4,2,4,-5,7,2,5,4,2,2,-3,2,4,7,0])#在希望的田野上
        durations.append([1,0.5,0.5,0.5,0.5,0.5,0.5,3,1,1,0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0.5,2])
        notes.append([7,7,9,2,0,0,-3,2,7,7,9,12,9,7,0,0,-3,2])#东方红
        durations.append([1,0.5,0.5,2,1,0.5,0.5,2,1,1,0.5,0.5,0.5,0.5,1,0.5,0.5,2])
        notes.append([4,2,-1,0,4,2,0,-1,-3,-3,5,4,4,2,-1,0,4,2,0,-1,-3,-3,-3,-3])#青春舞曲
        durations.append([0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0.5,2,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0.5,2])


        population = []
        for i in range(population_size):
            note_l = notes[i%10];
            duration_l = durations[i%10];
            length = len(note_l);
            pace = random.random() * 0.5 + 1
            music_piece = MusicPiece(0, pace);
            for i in range(length):
                music_piece.add_note(note_l[i], duration_l[i])
            population.append(music_piece)
        return population