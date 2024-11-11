from genetic.item.music_piece import MusicPiece
from abc import ABC, abstractmethod

#base class for initial generation functions
class Initial(ABC):
    def __init__(self):
        pass
    #generate a list of music pieces for the initial generation
    @abstractmethod
    def generate(self, population_size: int) -> [MusicPiece]:
        pass