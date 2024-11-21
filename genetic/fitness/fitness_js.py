from genetic.fitness.fitness import Fitness
from genetic.item.music_piece import MusicPiece
import numpy as np

class CompositeFitness(Fitness):
    def __init__(self, rest_ratio_target: float = 0.1, hold_ratio_target: float = 0.15):
        """
        初始化适应度函数。
        :param rest_ratio_target: 休止符比例的目标值。
        :param hold_ratio_target: 延长音符比例的目标值。
        """
        super().__init__()
        self.rest_ratio_target = rest_ratio_target
        self.hold_ratio_target = hold_ratio_target

    def evaluate(self, music_piece: MusicPiece) -> float:
        """
        综合适应度函数。
        :param music_piece: 要评估的音乐片段。
        :return: 适应度得分（分数越高越好）。
        """
        notes = music_piece.get_notes()
        if len(notes) == 0:
            return float('-inf')  # 无效片段

        fitness = 0

        # 1. 相邻音符音程
        fitness += self._evaluate_intervals(notes)

        # 2. 旋律的走向
        fitness += self._evaluate_melody_direction(notes)

        # 3. 首尾音符是否为根音
        fitness += self._evaluate_start_end_notes(notes, music_piece.get_base_pitch())

        # 4. 休止符的比例
        fitness += self._evaluate_rest_ratio(notes)

        # 5. 延长音符比例
        fitness += self._evaluate_hold_ratio(notes)

        # 6. 旋律的重复性
        fitness += self._evaluate_repetitions(notes)

        return fitness

    def _evaluate_intervals(self, notes: np.ndarray) -> float:
        """
        对相邻音符音程的适应度进行评分。
        :param notes: 音符矩阵。
        :return: 音程适应度分数。
        """
        penalties = 0
        for i in range(1, len(notes)):
            interval = abs(notes[i, 0] - notes[i - 1, 0])
            if interval > 12:  # 惩罚过大的音程跳跃
                penalties += (interval - 12) * 0.1
        return max(0, len(notes) - penalties)

    def _evaluate_melody_direction(self, notes: np.ndarray) -> float:
        """
        对旋律的单调性和稳定性进行评分。
        :param notes: 音符矩阵。
        :return: 旋律方向适应度分数。
        """
        score = 0
        for i in range(2, len(notes)):
            a, b, c = notes[i - 2, 0], notes[i - 1, 0], notes[i, 0]
            if a < b < c or a > b > c:  # 单调递增或递减
                score += 1
            elif a == b == c:  # 稳定
                score += 0.9
        return score

    def _evaluate_start_end_notes(self, notes: np.ndarray, base_pitch: int) -> float:
        """
        对首尾音符是否为根音进行评分。
        :param notes: 音符矩阵。
        :param base_pitch: 基准音高。
        :return: 首尾音符适应度分数。
        """
        root_notes = [base_pitch, base_pitch + 12]  # 包括根音和高八度的根音
        start_in_root = notes[0, 0] in root_notes
        end_in_root = notes[-1, 0] in root_notes
        return (1 if start_in_root else 0) + (1 if end_in_root else 0)

    def _evaluate_rest_ratio(self, notes: np.ndarray) -> float:
        """
        对休止符比例进行评分。
        :param notes: 音符矩阵。
        :return: 休止符比例适应度分数。
        """
        rest_count = np.sum(notes[:, 0] == 0)  # 假设音高为0表示休止符
        rest_ratio = rest_count / len(notes)
        return -abs(rest_ratio - self.rest_ratio_target) * 10

    def _evaluate_hold_ratio(self, notes: np.ndarray) -> float:
        """
        对延长音符比例进行评分。
        :param notes: 音符矩阵。
        :return: 延长音符比例适应度分数。
        """
        hold_count = np.sum(notes[:, 1] > 1)  # 假设时值大于1表示延长音符
        hold_ratio = hold_count / len(notes)
        return -abs(hold_ratio - self.hold_ratio_target) * 10

    def _evaluate_repetitions(self, notes: np.ndarray) -> float:
        """
        对旋律重复性进行评分。
        :param notes: 音符矩阵。
        :return: 旋律重复性适应度分数。
        """
        score = 0
        for i in range(len(notes) - 1):
            if np.array_equal(notes[i], notes[i + 1]):  # 完全重复
                score += 1
            elif notes[i, 0] == notes[i + 1, 0]:  # 音高重复但时值不同
                score += 0.5
        return score
