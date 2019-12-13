#infographics
import csv
import math
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
data = []

with open('player_ranks.csv') as player_file:
    file_reader = csv.reader(player_file, delimiter=',')
    for row in file_reader:
        #print(row[0], row[1], row[2], row[3])
        if(row[1]==''):
            row[1]=0
        data.append([int(row[0]), int(row[1]), int(row[2]), int(row[3]) ] )

print('len(data): ' + str(len(data)))
labels = ['Unknown', 'Herald', 'Guardian', 'Crusader', 'Archon', 'Legend', 'Ancient', 'Divine', 'Immortal']

#9x20, 9=ranks, 20=500 game intervals
interval_size = 30
labels2 = [.5 * x for x in range(interval_size)]
intervals = [[0]*interval_size for _ in range(9)]
for i in data:
    if(int( (i[2] + i[3]) / 500) < interval_size): games = int( (i[2] + i[3]) / 500)
    else: games = interval_size - 1
    intervals[ int(i[1] / 10) ][ games ] += 1

#plots number of games for each rank
for x in range(9):
    x_ticks = np.arange(len(intervals[x])) # number of x ticks
    width = 0.8  # the width of the bars

    fig, ax = plt.subplots(figsize=(12,8))
    #ax.bar(self, x, height, width=0.8, bottom=None, *, align='center', data=None, **kwargs)

    for y in range(len(intervals[x])): #a bar for each x tick
        ax.bar(y, intervals[x][y] , width)

    ax.set_ylabel('Accounts')
    ax.set_xlabel('Number of Games Played(thousands)')
    ax.set_title('Rank: ' + str(labels[x]))
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(labels2)

    fig.tight_layout()
    plt.show()

#calculating standard deviation
games_by_rank = [[] for _ in range(9)] #list of number of games played by each account
avg_per_rank = [0] * 9

for i in data:
    games_by_rank[int(i[1] / 10) ].append(i[2] + i[3])

for i in range(len(avg_per_rank)): #caculates average number of games played for each rank
    total=0
    for n in range(len(games_by_rank[i])):
        total+=games_by_rank[i][n]
    avg_per_rank[i] = int(total / len(games_by_rank[i]))

print("avg_per_rank")
print(avg_per_rank)

st_dev = [0] * 9
for i in range(len(games_by_rank)):
    total = 0
    for n in range(len(games_by_rank[i])):
        total += (games_by_rank[i][n] - avg_per_rank[i])**2
    st_dev[i] = int( math.sqrt(total / len(games_by_rank[i]) ) )

print("st_dev")
print(st_dev)

#not sure if this is standard deviation or not
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12, 8))

bplot1 = axes.boxplot(games_by_rank, notch=True, vert=True, patch_artist=True, labels=labels)

axes.set_title('Is this Standard Devidation?')

axes.yaxis.grid(True)
axes.set_ylabel('# of games played')

plt.show()
