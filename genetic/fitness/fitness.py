from genetic.item.music_piece import MusicPiece
from abc import ABC, abstractmethod

#base class for fitness functions
class Fitness(ABC):
    def __init__(self):
        pass

    #evaluate the fitness of a music piece
    @abstractmethod
    def evaluate(self, music_piece: MusicPiece) -> float:
        pass