from genetic.terminator.terminator import Terminator
class NRoundTerminator(Terminator):
    def __init__(self, n_round):
        self.n_round = n_round

    def check_terminate(self, fitness:[float], generation:int)->bool:
        return n_generation >= self.n_round