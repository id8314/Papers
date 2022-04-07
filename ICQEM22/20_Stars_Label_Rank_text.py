from time import time
from unittest.util import _MAX_LENGTH
from numpy import float64
from transformers import pipeline
from common import ptime, now
import pandas as pd

cols={
    'star_rating':pd.Series(dtype='int8'),
    'sentiment':pd.Series(dtype='int8'),
    'score':pd.Series(dtype='float64'),
    'review_body':pd.Series(dtype='string'),
    'modelo':pd.Series(dtype='string')
    }  
data = pd.DataFrame(cols)
data.style.format({
'score': lambda val: f'{val:,.16f}',
})

def create_pickle(modelo):
    sentiment_pipeline=pipeline("sentiment-analysis",model=modelo,max_length=512,truncation=True)
    
    global data
    
    print(f"Start: {now()}")
    t0 = time()
    n = 0

    print("Starting processing")

    with open("amazon_reviews_us_Automotive_v1_00_SHORT.tsv","r",encoding="utf-8") as sf:
        while True:
            line = sf.readline()
            if not line: # or n > 19
                break
            if n > 0: # skip header (n == 0)
                f = line.split('\t')
                oraculo = sentiment_pipeline(f[13], truncation=True)
                label=oraculo[0]['label']
                score= float64(oraculo[0]['score'])
                row = pd.DataFrame([{'modelo':modelo,'star_rating':f[7],'sentiment':label,'score':score,'review_body':f[13]}])
                data = pd.concat([data,row])

            n+=1
            print(f"\r{n} lines processed ",end="")

    print(f"\nProcessing time for model {modelo}: {ptime(time()-t0)}\n")

modelo=['mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis',
        'yiyanghkust/finbert-tone',
        'ProsusAI/finbert',
        'cardiffnlp/twitter-roberta-base-sentiment',       
        'oferweintraub/bert-base-finance-sentiment-noisy-search'
        ]
for m in modelo:
    create_pickle(m)

data.to_pickle("modelos.pkl")
