from genetic.inherit.mutate import Mutate
from genetic.item.music_piece import MusicPiece

import random
class Crossover_example(Mutate):

    def crossover(self, music_piece1: MusicPiece, music_piece2: MusicPiece) -> tuple[MusicPiece, MusicPiece]:
        #get the length of the music pieces
        length1 = music_piece1.get_length()
        length2 = music_piece2.get_length()

        break_point1 = random.randint(0 + 1, length1 - 1)
        break_point2 = random.randint(0 + 1, length2 - 1)
        part1_1 = music_piece1.get_part(0, break_point1)
        part1_2 = music_piece1.get_part(break_point1, length1)
        part2_1 = music_piece2.get_part(0, break_point2)
        part2_2 = music_piece2.get_part(break_point2, length2)

        part1_1.append(part2_2)
        part2_1.append(part1_2)
        return part1_1, part2_1
