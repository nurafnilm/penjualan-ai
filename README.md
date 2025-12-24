Python ini dijalankan menggunakan uv.

## Install Dependencies
```
uv pip install fastapi
uv pip install uvicorn
uv pip install pandas
uv pip install numpy
uv pip install prophet
uv pip install python-multipart
```

## Run the Server
`uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

## Endpoints
-   POST / predict : Upload CSV and get forecast (historical + future predictions).

## contoh csv format
```
date,projected_quantity
2026-01-01,100
2026-01-02,150
2026-01-03,120
```

## contoh hasil yang didapatkan
{
  "historical": [
    {
      "ds": "2026-01-01",
      "y": 100,
      "yhat": 105,
      "yhat_lower": 90,
      "yhat_upper": 120
    }
  ],
  "forecast": [
    {
      "ds": "2026-01-31",
      "yhat": 180,
      "yhat_lower": 150,
      "yhat_upper": 210
    }
  ]
}
