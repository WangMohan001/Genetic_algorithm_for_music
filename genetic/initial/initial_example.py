from genetic.initial.initial import Initial
from genetic.item.music_piece import MusicPiece
import numpy as np
import random
class Initial_example(Initial):
    def __init__(self):
        pass

    def generate(self, population_size: int) -> [MusicPiece]:
        population = []
        major_scale = np.array([-5, -3, -1, 0, 2, 4, 5])
        minor_scale = np.array([-5, -4, -2, 0, 2, 3, 5])
        for i in range(population_size):
            use_major = random.random() < 0.5  
            length = random.randint(10, 20)
            pace = random.random() * 0.5 + 1
            music_piece = MusicPiece(0, pace)
            for i in range(length):
                if use_major:
                    note = major_scale[random.randint(0, 6)]
                else:
                    note = minor_scale[random.randint(0, 6)]
                music_piece.add_note(note, 1)
            population.append(music_piece)
        return population