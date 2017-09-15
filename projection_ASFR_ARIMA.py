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
print(asfrs)
# fetching data for ASFR projection, then store it in list
try:
    with connection.cursor() as cursor:
        # selecting age range in data
        sql = "SELECT min(age) as minage, max(age) as maxage FROM asfr"
        cursor.execute(sql)
        agerange = cursor.fetchone()
        
        # Store data in vector
        for x in range(agerange["minage"], agerange["maxage"]+1):
            sql = "SELECT (rate*1000) as rate FROM asfr where age = %s"
            cursor.execute(sql, (x))
            result = cursor.fetchall()

            asfr= []

            for data in result:
                asfr.append(round(data['rate'], 3))
            
            asfrs.append(asfr)
            
finally:
    connection.close()

print(asfrs)

#project each asfr in list 
for asfrdata in asfrs:
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
        print('predicted=%f, expected=%f' % (yhat, obs))
    
    error = mean_squared_error(test, predictions)

    print('Test MSE: %.3f' % error)

    pyplot.plot(test)
    pyplot.plot(predictions, color='red')
    pyplot.show()