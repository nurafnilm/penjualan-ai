Python ini dijalankan menggunakan uv.
```
uv venv
.venv\Scripts\activate
```

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

## screenshoot percobaan
memasukkan file csv:
<img width="1919" height="958" alt="image" src="https://github.com/user-attachments/assets/0ec4e390-f83b-4487-9b81-03ab233c3109" />

respons:
<img width="1919" height="965" alt="image" src="https://github.com/user-attachments/assets/a0e090a3-4edc-4975-b0c4-cf9f03c88806" />

