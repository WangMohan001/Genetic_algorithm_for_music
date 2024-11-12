from midi2audio import FluidSynth
import numpy as np

def midi_to_audio(sound_font: str, midi_file: str, mp3_file: str) -> None:
    FluidSynth(sound_font=sound_font).midi_to_audio(midi_file, mp3_file)
    print(f"Audio file saved to {mp3_file}")


def roulette_wheel_selection(population, fitness, m, temperature):
    
    if temperature == 0:
        best_indices = np.argsort(fitness)[-m:]
        selected_population = [population[i] for i in best_indices]
        return selected_population

    adjusted_fitness = np.exp(np.array(fitness) / temperature)
    
    total_fitness = np.sum(adjusted_fitness)
    
    selection_probs = adjusted_fitness / total_fitness
    
    selected_indices = np.random.choice(len(population), size=m, p=selection_probs)
    
    selected_population = [population[i] for i in selected_indices]
    
    return selected_population
