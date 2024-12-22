import argparse
from genetic.algorithm.genetic_algorithm import Genetic_algorithm
from genetic.inherit.mutate_example import Mutate_example
from genetic.inherit.crossover_example import Crossover_example
from genetic.inherit.crossover import Crossover
from genetic.inherit.mutate import Mutate
from genetic.item.music_piece import MusicPiece
from genetic.fitness.fitness_transformer import Fitness_Transformer
from genetic.initial.initial_example_new import Initial_example
from genetic.terminator.n_round_terminator import NRoundTerminator
from genetic.utils.utils import midi_to_audio
import numpy as np
import mido
import json

def main():
    # 获取命令行传入的参数
    config_path = "genetic/configs/config_algorithm.json"
    sound_font = "genetic/soundfronts/27.3mg_symphony_hall_bank.SF2"
    instrument = "violin"

    
    # 初始化遗传算法
    genetic_algorithm = Genetic_algorithm(
        NRoundTerminator(15), 
        Fitness_Transformer(), 
        Mutate(), 
        Crossover(), 
        Initial_example(), 
        config_path
    )
    
    # 运行遗传算法
    for i in range(2000):
        genetic_algorithm.start()
        best, all = genetic_algorithm.simulate()
        best = best.get_notes()
        #print(best)
        best = np.array(best)
        np.save(f'generated/iter1_num{i}.npy', best)
if __name__ == "__main__":
    main()
