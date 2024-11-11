from genetic.inherit.mutate import Mutate
from genetic.item.music_piece import MusicPiece

import random
class Mutate_example(Mutate):

    def mutate(self, music_piece: MusicPiece) -> MusicPiece:
        rand = random.random()
        if rand < 0.3:
            return music_piece.retrograde()
        elif rand < 0.6:
            return music_piece.invert()
        elif rand < 0.8:
            return music_piece.transpose(random.randint(-4, 4))
        else:
            return music_piece.retrograde_invert()