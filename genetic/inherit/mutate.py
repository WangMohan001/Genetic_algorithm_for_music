from genetic.item.music_piece import MusicPiece
from abc import ABC, abstractmethod
import random

#base class for mutation functions
class Mutate(ABC):
    def __init__(self):
        pass

    #mutate a music piece
    @abstractmethod
    def mutate(self, music_piece: MusicPiece) -> MusicPiece:
        pass