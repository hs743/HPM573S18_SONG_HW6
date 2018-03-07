import problem as Model


headProb = 0.5
timeSteps = 20
cohortSize = 1000


myCohort = Model.Cohort(id=2, cohort_size=cohortSize, head_prob=headProb)
myCohort.simulate(timeSteps)
CI_ExpValue = myCohort.get_CI_exp_value()

CI_Loss = myCohort.get_CI_loss_prob()

print('95% CI of average expected reward is:', CI_ExpValue)

print('95% CI of average expected loss probablity is:', CI_Loss)

# Problem2:nterpretation of CI we calculate here
#For CI of expected reward of one thousand games, it means if we undergo so many times of the procedure(each procedure stands for
#1000 games and we calculate the confidence interval of expected reward), 95% confidence intervals we calculate will cover the true
#expected reward for this game.

#For CI of the probability of lossing games, it means if we undergo so many times of the procedure(each procedure stands for
#1000 games and we calculate the confidence interval of the probablity of lossing games), 95% confidence intervals we calculate
#  will cover the true probability of losing this game.

print("Problem 3")
#simulations for the owner

head_prob = 0.5
game_times = 20
owner_pop_size = 1000
num_sim_cohorts = 1000
alpha = 0.05

multiCohort = Model.multiCohorts(
    ids=range(num_sim_cohorts),
    cohort_sizes=[owner_pop_size]*num_sim_cohorts,
    head_probs=[head_prob]*num_sim_cohorts
)

multiCohort.simulate(game_times)
myCohort = Model.Cohort(id = 2, cohort_size=cohortSize,head_prob=headProb)

myCohort.simulate(timeSteps)


print("Average expected reward for the casino owner is:", myCohort.get_ave_exp_value())
print("95% CI of average reward for casino owner is:", myCohort.get_CI_exp_value())

#simulations for the gambler

head_prob = 0.5
game_times = 20
real_play_games = 10
num_sim_cohorts = 100


multiCohort = Model.multiCohorts(
    ids = range(num_sim_cohorts),
    cohort_sizes = [real_play_games] * num_sim_cohorts,
    head_probs = [head_prob]*num_sim_cohorts
)

multiCohort.simulate(game_times)

print('Projected mean reward for gambler is:', multiCohort.get_mean_expValue())
print('95% projection interval of average reward for the gambler is:', multiCohort.get_PI_mean_expValue())