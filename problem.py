import numpy as np
from enum import Enum
import scr.StatisticalClasses as Stat

class coinstate(Enum):
    """State of coin"""

    HEAD = 1
    TAIL = 0

class Game:
    def __init__(self, id, head_prob):

        self._id = id
        self._headProb = head_prob
        self._rnd = np.random
        self._rnd.seed(self._id)
        self._flipResult = coinstate.HEAD
        self._trails = []
        self._reward = -250

    def simulate(self, n_time_steps):

        t = 0  # simulation time

        while t < n_time_steps:

            if self._rnd.sample() < self._headProb:
                self._flipResult = coinstate.HEAD
                self._trails.append(self._flipResult)
            else:
                self._flipResult = coinstate.TAIL
                self._trails.append(self._flipResult)
            t += 1
    def get_exp_value(self, n_time_steps):
        i = 2
        while i < n_time_steps:
            if self._trails[i] == coinstate.HEAD and self._trails[i-1] == coinstate.TAIL and self._trails[i-2] == coinstate.TAIL:
                self._reward += 100
            i += 1
        return self._reward
class Cohort:
    def __init__(self, id, cohort_size, head_prob):
        self._cohorts = []
        self._expValue = []
        self._loss = []
        self._cohortSize = cohort_size
        self._sumStat_expectedReward = None
        self._sumStat_expectedLossProb = None


        n = 1
        while n <= cohort_size:
            game = Game(id * cohort_size + n, head_prob)
            self._cohorts.append(game)
            n += 1


    def simulate(self, n_time_steps):
        for game in self._cohorts:
            game.simulate(n_time_steps)#call the simulation step in class Game
            value = game.get_exp_value(n_time_steps)# Value stands for reward for each time of game
            if not (value is None):
                self._expValue.append(value)

        for value in self._expValue:
            if value < 0:
                self._loss.append(1)

            else:
                self._loss.append(0)

        self._sumStat_expectedReward = Stat.SummaryStat('Expected Reward', self._expValue)
        self._sumStat_expectedLossProb = Stat.SummaryStat('Expected Loss', self._loss)

    def get_exp_value(self):
        return self._expValue

    def get_initial_cohort_size(self):

        return self._cohortSize

    def get_loss_prob(self):

        return self._sumStat_expectedLossProb.get_mean()

    def get_CI_exp_value(self):
        alpha=0.05
        return self._sumStat_expectedReward.get_t_CI(alpha)

    def get_CI_loss_prob(self):
        alpha=0.05
        return self._sumStat_expectedLossProb.get_t_CI(alpha)

    def get_ave_exp_value(self):
        self._sumStat_expectedReward.get_mean()

class multiCohorts:

    def __init__(self, ids, cohort_sizes, head_probs):

        self._ids = ids
        self._cohortsizes = cohort_sizes
        self._headProbs = head_probs
        self._expValues = []
        self._meanExpValue = []
        self._sumStat_meanExpValue = None

    def simulate(self, n_time_steps):

        for i in self._ids:
            cohorts = multiCohorts(self._ids[i],self._cohortsizes[i],self._headProbs[i])
            output = cohorts.simulate(n_time_steps)
            self._expValues.append(Cohort.get_exp_value())
            self._meanExpValue.append(output.get_ave_exp_value())

    def get_cohort_mean_result(self, cohort_index):

        return self._meanExpValue[cohort_index]

    def get_cohort_CI_mean_result(self,cohort_index,alpha):
        st = Stat.SummaryStat('', self._expValues[cohort_index])
        return st.get_t_CI(alpha)

    def get_mean_expValue(self):
        return self._sumStat_meanExpValue.get_mean()

    def get_cohort_PI_expValue(self, cohort_index,alpha):
        st = Stat.SummaryStat('',self._expValues[cohort_index])
        return st.get_PI(alpha)

    def get_PI_mean_expValue(self):
        alpha = 0.05
        return self._sumStat_meanExpValue.get_PI(alpha)
