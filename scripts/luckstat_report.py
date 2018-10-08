from espnff import League
import numpy as np
from scipy.stats import rankdata

league_id = 864740
year = 2017

league = League(league_id, year)

week_in_progress = True

leagueteams = league.teams
num_teams = len(league.teams)
leaguescores = []
leaguewins = []
final = []

# Assemble matrix of scores by team and week
for team in leagueteams:
   teamscores = np.append(team,team.scores)
   leaguescores.append(teamscores)
   leaguewins.append(team.wins)

# Get number of weeks played
scores_only = np.array(leaguescores)[:,1:]
num_weeks = np.count_nonzero(np.apply_along_axis(np.count_nonzero,0,scores_only))
  
leaguescores_mat = np.array(leaguescores)[:,:(num_weeks)]

leagueranks = np.apply_along_axis(rankdata,0,leaguescores_mat[:,1:])
leaguewide_matchup_wins = leagueranks - 1
teamwins = np.apply_along_axis(sum,1,leaguewide_matchup_wins)

# Put together Team names, expected wins, actual wins, and matchup luck statistic
final.append(leagueteams)
final.append((teamwins/(num_weeks * (num_teams - 1))* num_weeks))
final.append(leaguewins)

luck_statistic = np.array(final)[2,:] - np.array(final)[1,:]

final.append(luck_statistic)

final = np.transpose(final)

print(final)
