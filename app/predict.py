import os
import pandas as pd
import numpy as np
from prophet import Prophet
from prophet.serialize import model_from_json, model_to_json
import warnings

# Suppress plotly warning (biar gak spam output JSON)
warnings.filterwarnings("ignore", message="Importing plotly failed")

MODEL_PATH = os.path.join('models', 'prophet_model.json')

# Buat model dasar
model = Prophet(
    weekly_seasonality=True,
    yearly_seasonality=True,
    changepoint_prior_scale=0.8,
    seasonality_prior_scale=10,
    uncertainty_samples=200
)
model.add_country_holidays(country_name='ID')
model.add_regressor('is_weekend')

retrain = False

# Load model kalau ada
try:
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'r') as f:
            model = model_from_json(f.read())
except Exception:
    retrain = True

def run_forecast(csv_path: str, periods: int = 30):
    if not csv_path or not os.path.exists(csv_path):
        raise ValueError('CSV not found')

    # Load CSV
    df = pd.read_csv(csv_path)
    date_col = next((c for c in df.columns if c.lower() in ['date', 'tanggal', 'ds']), df.columns[0])
    value_col = next((c for c in df.columns if c.lower() in ['projected_quantity', 'value', 'penjualan', 'y', 'quantity']), df.columns[1])

    df['ds'] = pd.to_datetime(df[date_col])
    df['y'] = pd.to_numeric(df[value_col], errors='coerce')
    df = df[['ds', 'y']].dropna()

    if len(df) < 2:
        raise ValueError('Data too small (<2 rows)')

    df = df.sort_values('ds').reset_index(drop=True)

    # Tambah regressor
    df['is_weekend'] = (df['ds'].dt.dayofweek >= 5).astype(int)
    prophet_df = df[['ds', 'y', 'is_weekend']].copy()

    # Retrain kalau perlu
    if retrain:
        model.fit(prophet_df)
        os.makedirs('models', exist_ok=True)
        with open(MODEL_PATH, 'w') as f:
            f.write(model_to_json(model))

    # Predict
    future = model.make_future_dataframe(periods=periods)
    future['is_weekend'] = (future['ds'].dt.dayofweek >= 5).astype(int)
    forecast = model.predict(future)

    hist_len = len(prophet_df)

    # Historical
    historical = pd.DataFrame({
        'ds': forecast['ds'][:hist_len].dt.strftime('%Y-%m-%d').tolist(),
        'y': prophet_df['y'].round(0).astype(int).tolist(),
        'yhat': np.round(forecast['yhat'][:hist_len]).astype(int).tolist(),
        'yhat_lower': np.floor(forecast['yhat_lower'][:hist_len]).astype(int).tolist(),
        'yhat_upper': np.ceil(forecast['yhat_upper'][:hist_len]).astype(int).tolist()
    }).to_dict('records')

    # Forecast
    forecast_data = pd.DataFrame({
        'ds': forecast['ds'][hist_len:].dt.strftime('%Y-%m-%d').tolist(),
        'yhat': np.round(forecast['yhat'][hist_len:]).astype(int).tolist(),
        'yhat_lower': np.floor(forecast['yhat_lower'][hist_len:]).astype(int).tolist(),
        'yhat_upper': np.ceil(forecast['yhat_upper'][hist_len:]).astype(int).tolist()
    }).to_dict('records')

    return {
        "historical": historical,
        "forecast": forecast_data
    }