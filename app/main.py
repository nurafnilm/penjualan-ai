from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import tempfile
import shutil
from .predict import run_forecast  # Import dari file sama folder

app = FastAPI(title="Forecast ML Service", version="1.0.0")

@app.post("/predict", response_model=dict)
async def predict(
    csv_file: UploadFile = File(..., description="CSV file with historical data"),
    periods: int = Form(30, description="Number of days to forecast")
):
    try:
        # Save uploaded file ke temp
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            shutil.copyfileobj(csv_file.file, tmp)
            tmp_path = tmp.name

        # Jalankan forecast
        result = run_forecast(tmp_path, periods)

        # Cleanup
        os.unlink(tmp_path)

        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)