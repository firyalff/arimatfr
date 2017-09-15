import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from pandas import read_csv
from pandas import datetime

def parser(x):
	return datetime.strptime('190'+x, '%Y-%m')

series = read_csv('./data/shampoo.csv', header=0, parse_dates=[0], squeeze=True, date_parser=parser)

r = robjects.r

itsmr = importr('itsmr')


m = r.matrix(r.rnorm(200), ncol=5)
pca = r.princomp(m)
r.plot(pca, main="Eigen values")
r.biplot(pca, main="biplot")