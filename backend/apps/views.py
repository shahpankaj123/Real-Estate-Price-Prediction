from django.shortcuts import render
import joblib
import pickle
import json
import numpy as np
import pandas as pd
# Create your views here.
__locations = None
__data_columns = None
__model = None

def predict_price(location,sqft,bath,bhk):
    X=pd.read_csv("apps/colms.csv")
    loaded_model = joblib.load('../model/banglore_home_prices_model.pickle')  
    loc_index = np.where(X.columns==location)[0]
    print(loc_index)

    x = np.zeros(len(X.columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return loaded_model.predict([x])[0]


def Home(request):
    p=0
    if request.method=='POST':
        Squareft=request.POST['Squareft']
        uiBHK=request.POST['uiBHK']
        uiBathrooms=request.POST['uiBathrooms']
        loc=request.POST['uiLocation']
        print(Squareft,uiBathrooms,uiBHK,loc)
        price=predict_price(loc,Squareft,uiBathrooms,uiBHK)
        p=str(price)+' Lakh'
    with open('apps/columns.json', 'r') as file:
       data = json.load(file)    
    return render(request,'index.html',{'data':data,'res':p})