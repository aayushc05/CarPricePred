# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('Index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_LPG=0
    Fuel_Diesel=0
    Fuel_Electric=0
    Seller_Type_Dealer=0
    if request.method == 'POST':
        Year = int(request.form['year'])
        Kms_Driven=int(request.form['kms_driven'])
        Owner=int(request.form['owner'])
        Fuel_Petrol=request.form['fuel_Petrol']
        if(Fuel_Petrol=='Petrol'):
                Fuel_Petrol=1
                Fuel_Diesel=0
                Fuel_LPG=0
                Fuel_Electric=0              
        elif(Fuel_Petrol=='Diesel'):
                Fuel_Petrol=0
                Fuel_Diesel=1
                Fuel_LPG=0
                Fuel_Electric=0
        elif(Fuel_Petrol=='Electric'):
                Fuel_Petrol=0
                Fuel_Diesel=0
                Fuel_LPG=0
                Fuel_Electric=1
        elif(Fuel_Petrol=='LPG'):
                Fuel_Petrol=0
                Fuel_Diesel=0
                Fuel_LPG=1
                Fuel_Electric=0
        else:
                Fuel_Petrol=0
                Fuel_Diesel=0
                Fuel_LPG=0
                Fuel_Electric=0
        Year=2020-Year
        Seller_Type_Individual=request.form['seller_type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
            Seller_Type_Dealer=0
        elif(Seller_Type_Individual=='Dealer'):
            Seller_Type_Individual=0
            Seller_Type_Dealer=1
        else:
            Seller_Type_Individual=0
            Seller_Type_Dealer=0
        Transmission_Manual=request.form['Transmission_Manual']
        if(Transmission_Manual=='Manual'):
            Transmission_Manual=1
        else:
            Transmission_Manual=0
        prediction=model.predict([[Kms_Driven,Owner,Year,Fuel_Diesel,Fuel_Petrol,Fuel_Electric,Fuel_LPG,Seller_Type_Individual,Seller_Type_Dealer,Transmission_Manual]])
        output=round(prediction[0],0)
        if output<0:
            return render_template('Index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('Index.html',prediction_text="You Can Sell The Car at Rs. {}".format(output))
    else:
        return render_template('Index.html')

if __name__=="__main__":
    app.run(debug=True)

