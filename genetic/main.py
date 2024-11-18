import argparse
from genetic.algorithm.genetic_algorithm import Genetic_algorithm
from genetic.inherit.mutate_example import Mutate_example
from genetic.inherit.crossover_example import Crossover_example
from genetic.item.music_piece import MusicPiece
from genetic.fitness.fitness_example import Fitness_example
from genetic.fitness.fitness_all import Fitness_all
from genetic.initial.initial_example import Initial_example
from genetic.terminator.n_round_terminator import NRoundTerminator
from genetic.utils.utils import midi_to_audio
import numpy as np
import mido
import json

def main():
    # 使用 argparse 解析命令行参数
    parser = argparse.ArgumentParser(description="Run Genetic Algorithm for Music Generation")
    parser.add_argument('config_path', type=str, help="Path to the configuration JSON file")
    parser.add_argument('sound_font', type=str, help="Path to the sound font file")
    parser.add_argument('output_midi', type=str, help="Output MIDI file name")
    parser.add_argument('output_audio', type=str, help="Output audio file name")
    parser.add_argument('instrument', type=str, help="Instrument name to be used in the MIDI file")
    parser.add_argument('instrument_json_path', type=str, help="Path to instrument mapping JSON file")

    args = parser.parse_args()

    # 获取命令行传入的参数
    config_path = args.config_path
    sound_font = args.sound_font
    output_midi = args.output_midi
    output_audio = args.output_audio
    instrument = args.instrument
    instrument_json_path = args.instrument_json_path

    # 打印出所有传入的参数
    print(f"Using config file: {config_path}")
    print(f"Sound font file: {sound_font}")
    print(f"Output MIDI file: {output_midi}")
    print(f"Output audio file: {output_audio}")
    print(f"Instrument used: {instrument}")
    print(f"Instrument JSON file: {instrument_json_path}")
    
    # 初始化遗传算法
    genetic_algorithm = Genetic_algorithm(
        NRoundTerminator(15), 
        Fitness_all(), 
        Mutate_example(), 
        Crossover_example(), 
        Initial_example(), 
        config_path
    )
    
    # 运行遗传算法
    best, all = genetic_algorithm.simulate()
    # 输出最佳结果
    print(best)
    best.output_midi(output_midi, instrument, instrument_json_path)
    
    # 将 MIDI 文件转换为音频
    midi_to_audio(sound_font, output_midi, output_audio)

if __name__ == "__main__":
    main()
