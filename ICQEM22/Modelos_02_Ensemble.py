# data preparation for ensemble model training

import pandas as pd
import numpy as np

data = pd.read_pickle("modelos.pkl")
data['modelo']=data['modelo'].apply(lambda x: x.split('/')[0])

def fecth_model_prediction(data,review_body,model):
    model_prediction = data[(data['modelo']==model) & (data['review_body']==review_body)]
    if len(model_prediction) > 1:
        model_prediction = model_prediction[0:1]
    return model_prediction

def build_ensemble_dataframe(data):
    df = pd.DataFrame(np.zeros((len(data),7)),columns=['index','target','s1','s2','s3','s4','s5'], dtype = np.int8)
    df['index'] = df['index'].astype(np.uint32)
    model_list = data.modelo.unique()
    n = 0
    s = 1

    for index, row in data.iterrows():

        for model in model_list:
            prediction = fecth_model_prediction(data,row['review_body'],model)
            model_prediction = prediction["sentiment"][0]
            col = 's'+str(s)
            df.at[n,col] = model_prediction
            if s == 1:
                df.at[n,'index'] = n
                target = prediction["star_mapped"][0] 
                df.at[n,'target'] = target
            s += 1
            if s > 5:
                s = 1
                n += 1

        if n % 1000 == 0:
            print("Saving...",end='\r')
            df[0:n].to_pickle("modelos_ensemble.pkl")

        if n % 100 == 0:
            print(f" {n} reviews processed",end='\r')

    print(f"{n} reviews processed        \n")
    return df

dx = build_ensemble_dataframe(data)
dx.to_pickle("modelos_ensemble.pkl")
print(dx)
