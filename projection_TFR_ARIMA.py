import pymysql.cursors
import pandas as pd
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import uuid
import time
import datetime
import metrics

#get current timestamp
ts = time.time()
timestamp = str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

#set prediction batch id
batchid= str(uuid.uuid4())

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='bukanwolverine',
                             db='tfrtesis',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

#insert prediction to database
def updatePredictionData (year, prediction, model):
    prediction= str(prediction)
    with connection.cursor() as cursor:
        sql = "INSERT INTO tfr_prediction (batch_id, model, year, prediction, created_at) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (batchid, model, year, prediction, timestamp))
    connection.commit()
    return

#mse logging
def logMSE (batchId, error):
    with connection.cursor() as cursor:
        sql = "INSERT INTO tfr_error_log (batch_id, mean_squared_error, mean_absolute_error) VALUES (%s, %s, %s)"
        cursor.execute(sql, (batchid, str(error[0]), str(error[1])))
    connection.commit()
    return
    
#projection function
def projectionARIMA (asfrdata, p, d, q):
    X = asfrdata
    
    currentmodel= 'ARIMA %d, %d, %d' % (p, d, q)
    
    size = int(len(X) * 0.66)
    train, test = X[0:size], X[size:len(X)]

    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(p,d,q))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        currentyear= years['maxyear']-(len(X)-size-t-1)
        #print('currentyear=%d ||| predicted=%f ||| expected=%f' % (currentyear, yhat, obs))
        updatePredictionData(currentyear, yhat[0], currentmodel)
    
    MSerror = mean_squared_error(test, predictions)
    MAerror = mean_absolute_error(test, predictions)
    
    train= pd.DataFrame(train)
    
    MASerror = metrics.MASE(train, pd.DataFrame(test), pd.DataFrame(predictions))

    print(MASerror)

    pyplot.plot(test)
    pyplot.plot(predictions, color='red')
    pyplot.show()
    return MSerror, MAerror


# fetching data for ASFR projection, then project ASFR
try:
    with connection.cursor() as cursor:
        sql = "SELECT min(year) as minyear, max(year) as maxyear FROM tfr ORDER BY year ASC"
        cursor.execute(sql)
        years = cursor.fetchone()
         
        sql = "SELECT (rate*1000) as rate FROM tfr ORDER BY year ASC"
        cursor.execute(sql)
        result = cursor.fetchall()
        asfr= []
        for data in result:
            asfr.append(round(data['rate'], 3))  
                
        p, d, q= 2, 1, 1
        result= projectionARIMA(asfr, p, d, q)
        print('MSE: %.3f  |||   MAE: %.3f' % (result[0], result[1]))
        logMSE(batchid, result)
           
            
finally:
    connection.close()

