from pandas import read_csv
from matplotlib import pyplot
from pandas.tools.plotting import autocorrelation_plot


series = read_csv('./data/shampoo.csv', header=0, parse_dates=[0], index_col=0, squeeze=True)
autocorrelation_plot(series)
pyplot.show()