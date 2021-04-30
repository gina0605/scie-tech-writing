import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np


def ax(x, a):
    return a * x


def axb(x, a, b):
    return a * x + b


def axbyc_log(X, a, b, c):
    x, y = X
    return a * np.log10(x) + b * np.log10(y) + c


def axbyc(X, a, b, c):
    x, y = X
    return a * x + b * y + c


def get_popt_R2(f, xdata, ydata):
    popt, _ = curve_fit(f, xdata, ydata)
    residuals = ydata - f(xdata, *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((ydata - np.mean(ydata))**2)
    r_squared = 1 - (ss_res / ss_tot)
    return popt, r_squared


def plot_xys(xdatas, ydatas, styles = None, colors = None, ttl = '', xlbl = '', ylbl = '',
             xlim = (None, None), ylim = (None, None), legends = None, alphas=None, **kwargs):
    '''
    xdatas, ydatas : List of np arrays.
    styles : List of styles for plots.
             If None, defaults to ['o', ..., 'o'].
    ttl : Title of the graph.
          Defaults to empty string.
    xlbl, ylbl : Label of x-, y-axis.
                 Defaults to empty string.
    xlim, ylim : Binary tuple for the range to show on graph.
                 Defaults to (None, None).
    legends : List of legends for each plot.
              Defaults to [None, ..., None].
    '''
    if not styles:
        styles = ['o'] * len(xdatas)
    if not colors:
        colors = [None] * len(xdatas)
    if not legends:
        legends = [None] * len(xdatas)
    if not alphas:
        alphas = [None] * len(xdatas)

    for i in range(len(xdatas)):
        plt.plot(xdatas[i], ydatas[i], styles[i], label = legends[i], color = colors[i], alpha=alphas[i], **kwargs)
    if len(xdatas) > 1 and any(legends):
        plt.legend()
    plt.title(ttl)
    plt.xlabel(xlbl)
    plt.ylabel(ylbl)
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.show()


def plot_trends(xdatas, ydatas, legends = None, trend_func = None, colors = None,
                many_colors = None, trend_legend = None, alphas=None, **kwargs):
    '''
    xdatas, ydats : List of np arrays.
    legends : List of legends of each data.
                May appear as '{legend}' or '{legend} data' or '{legend} trend line'.
              If None, defaults to ['', ..., '']
              If value is None, do not add legend for the plot.
    trend_func : The function for trend line.
                 If None, do not draw trend line.
    colors : List of colors to draw plots.
             Default to the matplotlib default colors.
    many_colors : Whether to draw data plot and trend plot with different colors.
                  If None, defaults to True iff there is only one data.
    trend_legend : Whether to add legends to trend lines.
                   If None, defaults to True iff there is only one data.
    **kwargs : ttl, xlbl, xlim, ylim.
    '''

    if not legends:
        legends = [''] * len(xdatas)
    if not colors:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    if alphas is None:
        alphas = [None] * len(xdatas)
    if many_colors == None:
        many_colors = len(xdatas) == 1
    if trend_legend == None:
        trend_legend = len(xdatas) == 1
    if not trend_func:
        many_colors = False
        trend_legend = False

    new_xdatas = []
    new_ydatas = []
    new_alphas = []
    new_legends = []
    new_colors = []
    for i in range(len(xdatas)):
        new_xdatas.append(xdatas[i])
        new_ydatas.append(ydatas[i])
        new_alphas.append(alphas[i])
        lgd = legends[i]
        if lgd != None and trend_legend:
            lgd = lgd + " data"
        new_legends.append(lgd)
        new_colors.append(colors[(i * 2 if many_colors else i) % len(colors)])
        if trend_func:
            popt, r_squared = get_popt_R2(trend_func, xdatas[i], ydatas[i])
            print("popt :", popt, ", R^2 :", r_squared)
            x_min = np.min(xdatas[i])
            x_max = np.max(xdatas[i])
            nxdata = np.arange(x_min, x_max, (x_max - x_min) / 100)
            new_xdatas.append(nxdata)
            new_ydatas.append(trend_func(nxdata, *popt))
            new_alphas.append(1)
            lgd = legends[i]
            if lgd != None and trend_legend:
                lgd = lgd + " trend line"
            else:
                lgd = None
            new_legends.append(lgd)
            new_colors.append(colors[(i * 2 + 1 if many_colors else i) % len(colors)])
    styles = (['o', '-'] if trend_func else ['o']) * len(xdatas)
    plot_xys(new_xdatas, new_ydatas, styles, new_colors, legends=new_legends, alphas=new_alphas, **kwargs)


def plot_trend(xdata, ydata, **kwargs):
    plot_trends([xdata], [ydata], **kwargs)


def plot_level_calculated_level(level, independent_var, f, popt, alpha, unzip=True, ylbl="Calculated level", **kwargs):
    if unzip:
        calculated_level = np.array(f(independent_var, *popt))
    else:
        calculated_level = np.array(f(independent_var, popt))
    print("Average difference: " + str(np.mean(abs(level - calculated_level))))
    print("Average square: " + str(np.mean(np.square(level - calculated_level))))
    lnspace = np.arange(1, 30, 29/100)
    plot_xys([level, lnspace], [calculated_level, lnspace], styles=['o', '-'], xlbl="Real level", ylbl=ylbl, xlim=(0, 31), ylim=(0, 31), alphas=[alpha, 1], legends=["result", "y=x"], **kwargs)
