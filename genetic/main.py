from genetic.algorithm.genetic_algorithm import Genetic_algorithm
from genetic.inherit.mutate_example import Mutate_example
from genetic.inherit.crossover_example import Crossover_example
from genetic.item.music_piece import MusicPiece
from genetic.fitness.fitness_example import Fitness_example
from genetic.initial.initial_example import Initial_example
from genetic.terminator.n_round_terminator import NRoundTerminator
from genetic.utils.utils import midi_to_audio
import numpy
import random

def main():
    json_path = "C:\\Users\\dcyy8\\Documents\\courses\\musicmath\\Genetic_algorithm_for_music\\genetic\\configs\\config_algorithm.json"
    
    genetic_algorithm = Genetic_algorithm(NRoundTerminator(5), Fitness_example(), Mutate_example(), Crossover_example(), Initial_example(), json_path)
    best, all = genetic_algorithm.simulate()
    print(best)
    best.output_midi("result.midi", "violin")
    sound = "27.3mg_symphony_hall_bank.SF2"
    midi_to_audio(sound, "result.midi", "result.wav")
if __name__ == "__main__":
    main()

