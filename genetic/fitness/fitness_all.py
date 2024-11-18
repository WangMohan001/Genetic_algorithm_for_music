from genetic.fitness.fitness import Fitness
from genetic.item.music_piece import MusicPiece
import numpy as np

# a fitness function that evaluates the variance of the consecutive notes of the music piece.
class Fitness_neighbor(Fitness):
    def __init__(self):
        pass

    def evaluate(self, music_piece: MusicPiece) -> float:
        notes = music_piece.get_notes()
        score = 0
        for i in range(len(notes) - 1):
            if abs(notes[i][0] - notes[i + 1][0]) == 1 or abs(notes[i][0] - notes[i + 1][0]) == 2:
                score += 1.0
                continue
            if abs(notes[i][0] - notes[i + 1][0]) == 3 or abs(notes[i][0] - notes[i + 1][0]) == 4:
                score += 1.0
                continue
            if notes[i][0] == notes[i + 1][0]:
                score += 0.9
                continue
            if abs(notes[i][0] - notes[i + 1][0]) == 5 or abs(notes[i][0] - notes[i + 1][0]) == 6:
                score += 0.8
                continue
            if abs(notes[i][0] - notes[i + 1][0]) == 7:
                score += 0.7
                continue
            if abs(notes[i][0] - notes[i + 1][0]) >= 10:
                score -= 0.5 * (abs(notes[i][0] - notes[i + 1][0]) - 9)

        if len(notes) > 1:
            score /= len(notes) - 1
        return score
#coutour of melody(3 consecutive)
class Fitness_contour(Fitness):
    def __init__(self):
        pass

    def evaluate(self, music_piece: MusicPiece) -> float:
        notes = music_piece.get_notes()
        score = 0
        for i in range(len(notes) - 2):
            #rising
            if notes[i][0] < notes[i + 1][0] and notes[i + 1][0] < notes[i + 2][0]:
                score += 1.0
                continue
            #falling
            if notes[i][0] > notes[i + 1][0] and notes[i + 1][0] > notes[i + 2][0]:
                score += 1.0
                continue
            #flat
            if notes[i][0] == notes[i + 1][0] and notes[i + 1][0] == notes[i + 2][0]:
                score += 0.5
                continue
        if len(notes) > 2:
            score /= len(notes) - 2
        return score
    
#fitness function that evaluates whether the start and end notes are the base note
class Fitness_base(Fitness):
    def __init__(self):
        pass

    def evaluate(self, music_piece: MusicPiece) -> float:
        notes = music_piece.get_notes()
        score = 0
        if notes[0][0] == 0:
            score += 1.0
        if notes[-1][0] == 0:
            score += 1.0
        return score

#fitness function that evaluates how many notes are in the scale
class Fitness_scale(Fitness):
    def __init__(self):
        pass

    def evaluate(self, music_piece: MusicPiece) -> float:
        notes = music_piece.get_notes()
        score = 0
        for note in notes:
            if (note[0] % 12 + 12) % 12 in [0, 2, 4, 5, 7, 9, 11]:
                score += 1
        if len(notes) > 0:
            score /= len(notes)
        return score

#penalty to the notes that crosses a bar
class Fitness_bar(Fitness):
    def __init__(self):
        pass

    def evaluate(self, music_piece: MusicPiece) -> float:
        notes = music_piece.get_notes()
        score = 0
        beat = music_piece.get_beat()
        ti = 0
        for note in notes:
            ti += note[1]
            if ti > beat:
                score -= 1.0
                ti = 0
            if ti >= beat:
                ti -= beat
        if len(notes) > 0:
            score /= len(notes)
        return score

#fitness function that evaluates the total length of rests in the music piece
class Fitness_rest(Fitness):
    def __init__(self, target: float = 0.1):
        self.target = target

    def evaluate(self, music_piece: MusicPiece) -> float:
        notes = music_piece.get_notes()
        num = 0
        for note in notes:
            if np.isnan(note[0]):
                num += 1
        if len(notes) > 0:
            num /= len(notes)
        return -60 * (num - self.target) * (num - self.target)

class Fitness_length(Fitness):
    def __init__(self, target: float = 30):
        self.target = target

    def evaluate(self, music_piece: MusicPiece) -> float:
        return - (music_piece.get_length() - self.target) * (music_piece.get_length() - self.target)

class Fitness_all(Fitness):
    def __init__(self):
        self.fitnesses = [Fitness_neighbor(), Fitness_contour(), Fitness_base(), Fitness_scale(), Fitness_bar(), Fitness_rest(), Fitness_length()]

    def evaluate(self, music_piece: MusicPiece) -> float:
        score = 0
        for fitness in self.fitnesses:
            score += fitness.evaluate(music_piece)
        return score