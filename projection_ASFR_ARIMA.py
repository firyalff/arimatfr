import pymysql.cursors
#from pandas import read_csv
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='bukanwolverine',
                             db='tfrtesis',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

asfrs= []

def updatePredictionData (age, year, prediction):
    with connection.cursor() as cursor:
        sql = "UPDATE asfr SET prediction= %s WHERE age = %s AND year = %s" % (prediction[0], age, year)
        print(sql)
        cursor.execute(sql)
    connection.commit()
    return

def projectionARIMA (asfrdata, processedAge):
    X = asfrdata
    size = int(len(X) * 0.66)
    train, test = X[0:size], X[size:len(X)]

    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(5,1,0))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        currentyear= agerange['maxyear']-(len(X)-size-t-1)
        print('currentyear=%d ||| predicted=%f ||| expected=%f' % (currentyear, yhat, obs))
        updatePredictionData(processedAge, currentyear, yhat)
    
    error = mean_squared_error(test, predictions)

    print('Test MSE: %.3f' % error)

    pyplot.plot(test)
    pyplot.plot(predictions, color='red')
    pyplot.show()
    return




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
            projectionARIMA(asfr, x)
            
finally:
    connection.close()

