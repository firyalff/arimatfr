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
def updatePredictionData (age, year, prediction, model):
    prediction= str(prediction)
    with connection.cursor() as cursor:
        sql = "INSERT INTO asfr_prediction (batch_id, model, year, age, prediction, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (batchid, model, year, age, prediction, timestamp))
    connection.commit()
    return

#mse logging
def logMSE (batchId, age, error):
    with connection.cursor() as cursor:
        sql = "INSERT INTO asfr_error_log (batch_id, age, mean_squared_error, mean_absolute_error) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (batchid, age, str(error[0]), str(error[1])))
    connection.commit()
    return
    
#projection function
def projectionARIMA (asfrdata, processedAge, p, d, q):
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
        currentyear= agerange['maxyear']-(len(X)-size-t-1)
        #print('currentyear=%d ||| predicted=%f ||| expected=%f' % (currentyear, yhat, obs))
        updatePredictionData(processedAge, currentyear, yhat[0], currentmodel)
    
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
        # selecting age range in data
        sql = "SELECT min(age) as minage, max(age) as maxage, min(year) as minyear, max(year) as maxyear FROM asfr"
        cursor.execute(sql)
        agerange = cursor.fetchone()
        
        # Store data in vector
        for x in range(agerange["minage"], agerange["maxage"]):
            sql = "SELECT (rate*1000) as rate FROM asfr where age = %s ORDER BY year ASC"
            cursor.execute(sql, (x))
            result = cursor.fetchall()

            asfr= []

            for data in result:
                asfr.append(round(data['rate'], 3))
                
            print('Current age = %d' % (x))
            p, d, q= 2, 1, 1
            result= projectionARIMA(asfr, x, p, d, q)
            print('MSE: %.3f  |||   MAE: %.3f' % (result[0], result[1]))
            logMSE(batchid, x, result)
            
finally:
    connection.close()

