import random
from math import log10, floor

seed = 179
random.seed(seed)
print("seed = " + str(seed))

def read_csv(dirname, level, needed_ppl=1):
    solved_cnts = []
    avg_triess = []
    with open(dirname + "/" + str(level) + ".csv", "r") as f:
        lines = f.readlines()
        for line in lines:
            data = line[:-1].split(",")
            if int(data[1]) >= needed_ppl:
                solved_cnts.append(int(data[1]))
                avg_triess.append(float(data[2]))
    return solved_cnts, avg_triess


def read_csvs(dirname, needed_ppl=1):
    levels = []
    solved_cnts = []
    avg_triess = []
    for level in range(1, 31):
        new_solved_cnts, new_avg_triess = read_csv(dirname, level, needed_ppl)
        levels += [level] * len(new_solved_cnts)
        solved_cnts += new_solved_cnts
        avg_triess += new_avg_triess
    return levels, solved_cnts, avg_triess


def cvs_specimen(dirname, num):
    levels = []
    solved_cnts = []
    avg_triess = []
    for level in range(1, 31):
        new_solved_cnts, new_avg_triess = read_csv(dirname, level)
        levels += [level] * num
        solved_cnts += [random.choice(new_solved_cnts) for _ in range(num)]
        avg_triess += [random.choice(new_avg_triess) for _ in range(num)]
    return levels, solved_cnts, avg_triess


def avg_level_by_solved_tries(dirname, K=100):
    level_sum = [[0] * K for i in range(K)]
    level_cnt = [[0] * K for i in range(K)]
    xmax = 5
    ymax = 1.4
    level, solved, tries = read_csvs(dirname)
    for i in range(len(level)):
        x = floor(log10(solved[i]) / xmax * K)
        y = floor(log10(tries[i]) / ymax * K)
        if x < K and y < K:
            level_sum[y][x] += level[i]
            level_cnt[y][x] += 1

    level_avg = [[] for i in range(K)]
    for i in range(K):
        for j in range(K):
            if level_cnt[i][j] == 0:
                z = 50
            else:
                z = level_sum[i][j] / level_cnt[i][j]
            level_avg[i].append(z)
    return level_avg


if __name__ == "__main__":
    read_csvs("result/210430-004716")
