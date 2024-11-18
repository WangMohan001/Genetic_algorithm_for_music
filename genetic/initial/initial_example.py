from genetic.initial.initial import Initial
from genetic.item.music_piece import MusicPiece
import numpy as np
import random
class Initial_example(Initial):
    def __init__(self):
        pass

    def generate(self, population_size: int) -> [MusicPiece]:
        population = []
        major_scale = np.array([-10, -8, -7, -5, -3, -1, 0, 2, 4, 5, 7, 9, 11])
        minor_scale = np.array([-10, -9, -7, -5, -4, -2, 0, 2, 3, 5, 7, 8, 10])
        for i in range(population_size):
            use_major = random.random() < 0.5  
            length = random.randint(20, 40)
            pace = random.random() * 0.5 + 1
            music_piece = MusicPiece(0, pace)
            for i in range(length):
                t = random.random()
                if t < 0.4:
                    duration = 1
                elif t < 0.65:
                    duration = 0.5
                elif t < 0.85:
                    duration = 2
                elif t < 0.95:
                    duration = 0.25
                else:
                    duration = 4
                if random.random() < 0.1:
                    music_piece.add_rest(duration)
                else:
                    if use_major:
                        note = major_scale[random.randint(0, len(major_scale) - 1)]
                    else:
                        note = minor_scale[random.randint(0, len(minor_scale) - 1)]
                    music_piece.add_note(note, duration)
            population.append(music_piece)
        return population