from genetic.item.music_piece import MusicPiece
from abc import ABC, abstractmethod
import random

#base class for mutation functions
class Mutate(ABC):
    def __init__(self):
        pass

    #mutate a music piece
    #music_piece中相应function已修改
    def mutate(self, music_piece: MusicPiece) -> MusicPiece:
        mutation_operators = [self.retrograde_mutate, self.invert_mutate, 
                              self.transpose_mutate, self.invert_retrograde_mutate]
        chosen_mutation = random.choice(mutation_operators)
        return chosen_mutation(music_piece)
    def retrograde_mutate(self,music_piece: MusicPiece):
        return music_piece.retrograde() 
    def invert_mutate(self,music_piece:MusicPiece):
        return music_piece.invert(random.randint(0,music_piece.get_length()-1))
    def transpose_mutate(self,music_piece:MusicPiece):
        return music_piece.transpose(random.randint(-2, 2))
    def invert_retrograde_mutate(self,music_piece:MusicPiece):
        return music_piece.invert_retrograde(random.randint(0,music_piece.get_length()-1))
    def transpose_retrograde_mutate(self,music_piece:MusicPiece):
        return music_piece.transpose_retrograde(random.randint(-2, 2))
    