from fastapi import FastAPI
from fastapi.responses import JSONResponse
import joblib
import numpy as np
import pandas as pd
from src.utils.common import load_object
from api.schemas import (
    StudentInput,
    BatchStudentInput,
    PredictionResponse,
    BatchPredictionResponse
)
from src.pipeline.predict_pipeline import PredictPipeline
from src.config.configuration import ConfigurationManager

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
    return {'message': 'Welcome, are you ready to get your customers segmented.'}

@app.get("/about")
def about():
    return {'message': 'We are a well reputed company, specialized in Customer Segmentation.'}

@app.get("/health")
def health():
    return {'status': 'healthy'}

@app.post('/predict', response_model=PredictionResponse)
def predict(data: StudentInput):
    df = pd.DataFrame([{
        "minutes_watched": data.minutes_watched,
        "CLV": data.clv,
        "region": int(data.region),  # Convert string to int
        "channel": int(data.channel)  # Convert string to int
    }])

    config = ConfigurationManager()
    predict_pipeline_config = config.get_predict_pipeline_config()
    predict_pipeline = PredictPipeline(config=predict_pipeline_config)

    df = predict_pipeline.predict(df)

    return PredictionResponse(
        minutes_watched=data.minutes_watched,
        clv=data.clv,
        cluster=int(df['cluster'].iloc[0]),
        persona=str(df['persona'].iloc[0]),
        region=str(df['region'].iloc[0]),      # Include in response
        channel=str(df['channel'].iloc[0])    # Include in response
    )

@app.post('/predict/batch', response_model=BatchPredictionResponse)
def predict_batch(data: BatchStudentInput):
    # Include region and channel in batch processing
    df_input = pd.DataFrame([
        {
            "minutes_watched": s.minutes_watched, 
            "CLV": s.clv,
            "region": int(s.region),      # Add this
            "channel": int(s.channel)     # Add this
        }
        for s in data.students
    ])

    config = ConfigurationManager()
    predict_pipeline_config = config.get_predict_pipeline_config()
    predict_pipeline = PredictPipeline(config=predict_pipeline_config)

    df_result = predict_pipeline.predict(df_input)

    predictions = [
        PredictionResponse(
            minutes_watched=float(row["minutes_watched"]),
            clv=float(row["CLV"]),
            cluster=int(row["cluster"]),
            persona=str(row["persona"]),
            region=str(row["region"]),      # Include in response
            channel=str(row["channel"])     # Include in response
        )
        for _, row in df_result.iterrows()
    ]

    return BatchPredictionResponse(
        predictions=predictions,
        total=len(predictions),
    )