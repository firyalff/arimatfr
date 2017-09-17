from pandas import read_csv
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import csv
import time

series = read_csv('./data/spain_fertility_TFR.csv', header=0, parse_dates=[0], index_col=0, squeeze=True)

X = series.values

size = int(len(X) * 0.5)
train, test = X[0:size], X[size:len(X)]

finalpredictions= []

history = [x for x in train]
predictions = list()
for t in range(len(test)):
    model = ARIMA(history, order=(2,1,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    obs = test[t]
    
    history.append(obs)
    finalpredictions.append([obs, yhat[0]])
    print('predicted=%f, expected=%f' % (yhat, obs))
    
with open("%s-prediction.csv" % (time.time()), 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Expected', 'Predictions'])
    for predictiondata in finalpredictions:
        filewriter.writerow(predictiondata)

error = mean_squared_error(test, predictions)

print('Test MSE: %.3f' % error)

pyplot.plot(test)
pyplot.plot(predictions, color='red')
pyplot.show()