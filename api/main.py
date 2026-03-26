from fastapi import FastAPI
import joblib
import numpy as np
import pandas as pd
from src.utils.common import load_object
from api.schemas import (
    StudentInput,
    PredictionResponse
)
from src.pipeline.predict_pipeline import PredictPipeline
from src.config.configuration import ConfigurationManager

'''
# Load artifacts
MODEL_PATH = 'artifacts/models/final_model.pkl'
SCALER_PATH = 'artifacts/preprocessor.pkl'

model = load_object(MODEL_PATH)
scaler = load_object(SCALER_PATH)
'''

app = FastAPI(
    title="Customer Segmentation API",
    description="Assigns students of the Online Learning Platform to one of three "
        "behavioural personas using a K-Means clustering model trained on "
        "engagement (minutes watched) and monetary (CLV) signals.\n\n"
        "**Personas:**\n"
        "- `0` — 🎯 The Driven Learner (High engagement, Low CLV)\n"
        "- `1` — 💤 The Passive Payer  (Low engagement, Mid CLV)\n"
        "- `2` — 🏆 The Champion       (High engagement, High CLV)\n",
    version="1.0.0"
)

@app.get("/")
def home():
    return {'message': 'Welcome, are you ready to get your customers segemented.'}

@app.get("/about")
def about():
    return {'message': 'We are a well reputed company, specialized in Customer Segmentation.'}

@app.get("/health")
def health():
    return {'status': 'healthy'}

@app.post('/predict')
def predict(data: StudentInput):
    df = pd.DataFrame([{
        "minutes_watched": data.minutes_watched,
        "CLV": data.clv,
        "region": data.region,
        "channel": data.channel
    }])

    config = ConfigurationManager()
    predict_pipeline_config = config.get_predict_pipeline_config()

    predict_pipeline = PredictPipeline(config=predict_pipeline_config)

    df = predict_pipeline.predict(df)

    return PredictionResponse(
        minutes_watched=data.minutes_watched,
        clv=data.clv,
        cluster=int(df['cluster'].iloc[0]),
        persona=str(df['persona'].iloc[0])
    )