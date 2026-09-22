from pathlib import Path
import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field



MODEL_PATH = Path(__file__).parent / "housing_model.pkl"
with open(MODEL_PATH, "rb") as file:
    artifact = pickle.load(file)

model = artifact["model"]
feature_names = artifact["feature_names"]


app = FastAPI(title="California Housing Price API",
    description=("Predicts the median house value of a California "
        "census-block group."),
    version="1.0.0",)


class HousingInput(BaseModel):
    longitude: float = Field(ge=-180, le=180)
    latitude: float = Field(ge=-90, le=90)
    housing_median_age: float = Field(ge=0)
    total_rooms: float = Field(gt=0)
    total_bedrooms: float = Field(ge=0)
    population: float = Field(ge=0)
    households: float = Field(gt=0)
    median_income: float = Field(ge=0)


@app.get("/")
def root():
    return {
        "message": "California Housing Price API",
        "documentation": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(data: HousingInput):
    row = data.model_dump()
    row["rooms_per_household"] = (row["total_rooms"] / row["households"])
    row["bedrooms_per_room"] = (row["total_bedrooms"] / row["total_rooms"])
    row["people_per_household"] = (row["population"] / row["households"])

    input_df = pd.DataFrame([row])
    input_df = input_df[feature_names]
    prediction = model.predict(input_df)[0]

    return {"predicted_median_house_value": round(float(prediction), 2,)}