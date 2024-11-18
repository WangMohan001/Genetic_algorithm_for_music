from genetic.fitness.fitness import Fitness
from genetic.item.music_piece import MusicPiece
import numpy as np

class Fitness_example(Fitness):
    def __init__(self):
        pass

    def evaluate(self, music_piece: MusicPiece) -> float:
        return -abs(np.var(music_piece.get_notes()[:, 0]) - 10) - 0.2 * (music_piece.get_length() - 30)  * (music_piece.get_length() - 30)