# California Housing Price Predictor

A random forest estimates the median house value of a California census-block group from eight inputs. The project includes a training notebook, a FastAPI prediction service, and a Dockerfile.

This dataset describes areas rather than individual houses. It is historical learning data, so the predictions are not current property valuations.

## Project files

| File | Purpose |
| --- | --- |
| `train_housing_predictor.ipynb` | Explore the data, engineer features, train, and evaluate models. |
| `app.py` | Validate requests, recreate the engineered features, and serve predictions. |
| `requirements.txt` | Python dependencies for the API and model. |
| `Dockerfile` | Build a container that runs the API. |
| `housing_model.pkl` | Trained model artifact, created separately and excluded from Git. |

## Get the model file

The model artifact is about 101 MiB and is excluded from the repository. Run the training notebook in Colab to create `housing_model.pkl`, download it, and put it in the same directory as `app.py` and `Dockerfile`. The saved artifact must contain the trained model under `"model"` and its ordered feature names under `"feature_names"`.

The API expects these original inputs: `longitude`, `latitude`, `housing_median_age`, `total_rooms`, `total_bedrooms`, `population`, `households`, and `median_income`. It derives `rooms_per_household`, `bedrooms_per_room`, and `people_per_household` before predicting. Keep training and API feature engineering consistent.

The model was trained with Python 3.13, scikit-learn 1.6.1, NumPy 2.1.3, and pandas 2.2.3. Load the pickle only if you trust its source.

## Run locally on Windows

From PowerShell in the project directory:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app:app --reload
```

Open http://127.0.0.1:8000/docs for the interactive API documentation, or http://127.0.0.1:8000/health to check that the service started. Press Ctrl+C to stop the server.

## Run with Docker

Start Docker Desktop and run these commands from the project directory after placing `housing_model.pkl` beside the Dockerfile:

```powershell
docker build -t housing-predictor .
docker run --rm -p 8000:8000 housing-predictor
```

Open http://127.0.0.1:8000/docs. Stop any locally running Uvicorn server before starting the container, because both use port 8000.

## Request a prediction

In `/docs`, expand **POST /predict**, select **Try it out**, and submit:

```json
{
  "longitude": -122.23,
  "latitude": 37.88,
  "housing_median_age": 41,
  "total_rooms": 880,
  "total_bedrooms": 129,
  "population": 322,
  "households": 126,
  "median_income": 8.3252
}
```

A response from the trained model used in this project was:

```json
{"predicted_median_house_value": 427759.41}
```

The returned number is an estimated area median value in US dollars. Retraining the model can change it.


## Status

The API and Docker image have been tested locally. Public deployment has not been set up.
