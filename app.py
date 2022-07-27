import uvicorn
from fastapi import FastAPI
from Income import Income
import numpy as np
import pandas as pd
from sklearn import preprocessing
import pickle

app = FastAPI()
model = pickle.load(open('model.pkl', 'rb'))
encoder_dict = pickle.load(open('encoder.pkl', 'rb')) 

@app.get('/')
async def index():
  return {"message":"First Route"}

@app.post('/predict')
async def predict_income(data:Income):
    data = data.dict()  
    print(data)
    df=pd.DataFrame([list(data.values())], columns=['age','workclass','education','maritalstatus','occupation','relationship','race','gender','capitalgain','capitalloss','hoursperweek','nativecountry'])
    
    category_col =['workclass', 'education', 'maritalstatus', 'occupation', 'relationship', 'race', 'gender', 'nativecountry']
    for cat in encoder_dict:
        for col in df.columns:
            le = preprocessing.LabelEncoder()
            if cat == col:
                le.classes_ = encoder_dict[cat]
                for unique_item in df[col].unique():
                    if unique_item not in le.classes_:
                        df[col] = ['Unknown' if x == unique_item else x for x in df[col]]
                df[col] = le.transform(df[col])
    
    features_list = df.values.tolist()
    prediction = model.predict(features_list)
    output = int(prediction[0])
    if output == 1:
        text = ">50K"
    else:
        text = "<=50K"
    return {
        'prediction': 'Employee Income is {}'.format(text)
    }

if __name__ == '__main__':
    uvicorn.run(app,host="127.0.0.1",port=8000)
