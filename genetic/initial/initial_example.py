from genetic.initial.initial import Initial
from genetic.item.music_piece import MusicPiece
import numpy as np
import random
class Initial_example(Initial):
    def __init__(self):
        pass

    def initial(self) -> MusicPiece:
        major_scale = np.array([-5, -3, -1, 0, 2, 4, 5, 7, 9, 11])
        minor_scale = np.array([-5, -4, -2, 0, 2, 3, 5, 7, 8, 10])
        use_major = random.random() < 0.5  
        length = random.randint(10, 20)
        pace = random.random() * 0.5 + 1
        music_piece = MusicPiece(0, pace)
        for i in range(length):
            if use_major:
                note = major_scale[random.randint(0, 9)]
            else:
                note = minor_scale[random.randint(0, 9)]
            music_piece.add_note(note, 1)