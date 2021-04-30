from read_csv import read_csvs, cvs_specimen, avg_level_by_solved_tries
from plot_data import *
import numpy as np
from matplotlib.colors import Normalize
from math import log10, floor


def get_avg(dirname):
    solved_cnt_avg = []
    avg_tries_avg = []
    for level in range(1, 31):
        solved_cnt_sum = 0
        avg_tries_sum = 0
        with open(dirname + "/" + str(level) + ".csv", "r") as f:
            lines = f.readlines()
            for line in lines:
                data = line[:-1].split(",")
                solved_cnt_sum += int(data[1])
                avg_tries_sum += float(data[2])
            solved_cnt_avg.append(solved_cnt_sum / len(lines))
            avg_tries_avg.append(avg_tries_sum / len(lines))
    return solved_cnt_avg, avg_tries_avg


def print_avg(dirname):
    solved_cnt_avg, avg_tries_avg = get_avg(dirname)
    print("level\tsolved_cnt\tavg_tries")
    for level in range(1, 31):
        print("{:3d}\t{:9.3f}\t{:7.3f}".format(level, solved_cnt_avg[level - 1], avg_tries_avg[level - 1]))


def draw_solved_level_plot(dirname):
    level, solved, tries = read_csvs(dirname)
    plot_trend(np.array(solved), np.array(level), xlbl="solved", ylbl="level", xlim=(None, 50000), alphas=[0.03], ttl="level - solved")


def draw_log_solved_level_plot(dirname):
    level, solved, tries = read_csvs(dirname)
    plot_trend(np.log10(np.array(solved)), np.array(level), xlbl="log10(solved)", ylbl="level", alphas=[0.05], trend_func=axb, ttl="level - log(solved)")


def draw_tries_level_plot(dirname):
    level, solved, tries = read_csvs(dirname)
    plot_trend(np.array(tries), np.array(level), xlbl="avg_tries", ylbl="level", xlim=(0, 15), ylim=(0, 30), alphas=[0.02], ttl="level - avg_tries")


def draw_log_tries_level_plot(dirname):
    level, solved, tries = read_csvs(dirname)
    plot_trend(np.array(np.log10(tries)), np.array(level), xlbl="log10(avg_tries)", ylbl="level", ylim=(0, 30), alphas=[0.02], trend_func=axb, ttl="level - log(avg_tries)")


def draw_tries_solved_plot(dirname):
    level, solved, tries = read_csvs(dirname)
    plot_trend(np.array(solved), np.array(tries), xlbl="solved", ylbl="avg_tries", xlim=(0, 15000), ylim=(0, 20), alphas=[0.01])


def draw_tries_log_solved_plot(dirname):
    level, solved, tries = read_csvs(dirname)
    plot_trend(np.array(np.log10(solved)), np.array(tries), xlbl="log10(solved)", ylbl="avg_tries", xlim=(None, None), ylim=(0, 20), alphas=[0.01])


def draw_log_tries_log_solved_plot(dirname):
    level, solved, tries = read_csvs(dirname)
    plot_trend(np.array(np.log10(solved)), np.array(np.log10(tries)), xlbl="log10(solved)", ylbl="log10(avg_tries)", xlim=(None, 5), ylim=(None, 1.5), alphas=[0.02])


def draw_level_per_log(dirname):
    level_avg = avg_level_by_solved_tries(dirname)
    #print(level_avg)
    plt.imshow(level_avg, cmap=plt.get_cmap('gist_ncar'), norm=Normalize(vmin=-4, vmax=42, clip=True), origin='lower', extent=[0, 5, 0, 1.4], aspect='auto')
    plt.title("avg level by log(avg_tries), log(solved)")
    plt.xlabel("log10(solved)")
    plt.ylabel("log10(avg_tries)")
    plt.colorbar()
    plt.show()


def get_trend_level_per_log(dirname):
    K = 100
    level_avg = avg_level_by_solved_tries(dirname, K=K)
    levels = []
    log_solved = []
    log_tries = []
    for i in range(K):
        for j in range(K):
            if level_avg[j][i] < 40:
                levels.append(level_avg[j][i])
                log_solved.append((i + 0.5) / K * 5)
                log_tries.append((j + 0.5) / K * 1.4)
    levels = np.array(levels)
    log_solved = np.array(log_solved)
    log_tries = np.array(log_tries)
    popt, r_squared = get_popt_R2(axbyc, (log_solved, log_tries), levels)
    print("popt :", popt, ", R^2 :", r_squared)
    plot_level_calculated_level(levels, (log_solved, log_tries), axbyc, popt, 0.1, ttl="Comparison between formula and avg level")


def draw_calculated_level_log_solved_log_tries(dirname, a, b, c):
    K = 100
    xmax = 5
    ymax = 1.4
    level, solved, tries = read_csvs(dirname)
    calculated_level = np.zeros([K, K])
    for i in range(K):
        for j in range(K):
            x = i * xmax / K
            y = j * ymax / K
            calculated_level[j][i] = a * x + b * y + c
    #print(level_avg)
    plt.imshow(calculated_level, cmap=plt.get_cmap('gist_ncar'), norm=Normalize(vmin=-4, vmax=42, clip=True), origin='lower', extent=[0, xmax, 0, ymax], aspect='auto')
    plt.title("level per log(avg_tries), log(solved)")
    plt.xlabel("log10(solved)")
    plt.ylabel("log10(avg_tries)")
    plt.colorbar()
    plt.show()


def get_trend_level_log_solved_log_tries(dirname, needed_ppl=1):
    level, solved, tries = read_csvs(dirname, needed_ppl)
    popt, r_squared = get_popt_R2(axbyc_log, (solved, tries), level)
    calculated_level = np.array(axbyc_log((solved, tries), *popt))
    new_calculated_level = calculated_level * 2 - 15
    print("popt :", popt, ", R^2 :", r_squared)
    print("Average difference: " + str(np.mean(abs(np.array(level) - calculated_level))))
    #print("Average difference(new): " + str(np.mean(abs(np.array(level) - new_calculated_level))))
    #print("Average difference(mean):" + str(np.mean(abs(np.array(level) - np.mean(np.array(level))))))
    print("Average square: " + str(np.mean(np.square(np.array(level) - calculated_level))))
    #print("Average square(new): " + str(np.mean(np.square(np.array(level) - new_calculated_level))))
    #print("Average square(mean): " + str(np.mean(np.square(np.array(level) - np.mean(np.array(level))))))
    lnspace = np.arange(1, 30, 29/100)
    plot_xys([level, lnspace], [calculated_level, lnspace], styles=['o', '-'], xlbl="Real level", ylbl="Calculated level", xlim=(0, 31), ylim=(0, 31), alphas=[0.01, 1])
    #plot_xys([level, lnspace], [new_calculated_level, lnspace], styles=['o', '-'], xlbl="Real level", ylbl="Calculated level", alphas=[0.01, 1])


def get_trend_level_log_solved_log_tries_normalized(dirname):
    level, solved, tries = cvs_specimen(dirname, 100)
    popt, r_squared = get_popt_R2(axbyc_log, (solved, tries), level)
    calculated_level = np.array(axbyc_log((solved, tries), *popt))
    print("popt :", popt, ", R^2 :", r_squared)
    print("Average difference: " + str(np.mean(abs(np.array(level) - calculated_level))))
    print("Average square: " + str(np.mean(np.square(np.array(level) - calculated_level))))
    lnspace = np.arange(1, 30, 29/100)
    plot_xys([level, lnspace], [calculated_level, lnspace], styles=['o', '-'], xlbl="Real level", ylbl="Calculated level", alphas=[0.1, 1])


def plot_total_level_calculated_level(dirname, f, popt, alpha=0.01, unzip=True, **kwargs):
    level, solved, tries = read_csvs(dirname)
    plot_level_calculated_level(np.array(level), (np.array(solved), np.array(tries)), f, popt, alpha, unzip=unzip, **kwargs)


def plot_best_level_calculated_level(dirname):
    def f(x, avg_level):
        solved, tries = x
        y = []
        for s, t in zip(solved, tries):
            i = floor(log10(s) / 5 * 100)
            j = floor(log10(t) / 1.4 * 100)
            if i < 100 and j < 100:
                y.append(avg_level[j][i])
            else:
                y.append(15.5)
        return y

    K = 100
    level_avg = avg_level_by_solved_tries(dirname, K=K)
    plot_total_level_calculated_level(dirname, f, level_avg, unzip=False, ttl="Comparison between avg level of cell and real data", ylbl="avg level")


if __name__ == "__main__":
    dirname = "result/210430-004716"
    #draw_tries_level_plot(dirname)
    #draw_log_tries_level_plot(dirname)
    #draw_solved_level_plot(dirname)
    #draw_log_solved_level_plot(dirname)
    ###draw_log_tries_log_solved_plot(dirname)
    #draw_level_per_log(dirname)
    #plot_best_level_calculated_level(dirname)
    #get_trend_level_per_log(dirname)
    #draw_calculated_level_log_solved_log_tries(dirname, -3.06589321, 11.92013778, 14.07985813)
    plot_total_level_calculated_level(dirname, axbyc_log, [-3.06589321, 11.92013778, 14.07985813])

