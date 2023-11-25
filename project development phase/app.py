import numpy as np
from numpy.core.fromnumeric import size
import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestRegressor
from flask import Flask, render_template, request
import pickle
import datetime as dt
import calendar

app = Flask(__name__)
loaded_model=pickle.load(open('final_model.pkl', 'rb'))

@app.route('/')
def start():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    store = int(request.form.get('store'))
    dept = int(request.form.get('dept'))
    date = request.form.get('date')
    isHoliday = request.form.get('isHolidayRadio') == "1"
    size = float(request.form.get('size'))
    temp = float(request.form.get('temp'))
    d=dt.datetime.strptime(date, '%Y-%m-%d')
    year = (d.year)
    month=d.month
    month_name=calendar.month_name[month]
    print("year", type(year))
    print("year val = ",year, type(year), month)
    X_test=pd.DataFrame({'Store': [store], 'Dept': [dept], 'Size': [size], 'Temperature': [temp], 
                          'IsHoliday': [isHoliday], 'Year':[year],"Month": [month]})
    print("X_test = ", X_test.head())
    print("type of X_test = ", type(X_test))
    print("predict = ", store, dept, date, isHoliday)
    y_pred=loaded_model.predict(X_test)
    output=round(y_pred[0],2)
    print("predicted = ", output)
    return render_template('index.html', output=output, store=store, dept=dept, month_name=month_name, year=year)


                 
if __name__ == '__main__' :
    app.run(debug=True)

