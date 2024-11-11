from genetic.item.music_piece import MusicPiece
from abc import ABC, abstractmethod
import random

#base class for crossover functions
class Crossover(ABC):
    def __init__(self, random_seed: int):
        self.random_seed = random_seed

    #crossover two music pieces
    @abstractmethod
    def crossover(self, music_piece1: MusicPiece, music_piece2: MusicPiece ) -> tuple[MusicPiece, MusicPiece]:
        pass