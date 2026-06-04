from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="CI/CD Pipeline Demo API", version="1.0.0")

class PredictionRequest(BaseModel):
    value: float

class PredictionResponse(BaseModel):
    input: float
    prediction: str
    confidence: float

@app.get("/health")
def health():
    return {"status": "ok", "service": "cicd-pipeline-api", "version": "1.0.0"}

@app.get("/metrics")
def metrics():
    return {
        "uptime": "healthy",
        "requests_processed": 1000,
        "error_rate": 0.01,
        "avg_response_time_ms": 45
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    # Simple threshold-based prediction
    if request.value > 0.5:
        prediction = "high"
        confidence = round(request.value, 4)
    else:
        prediction = "low"
        confidence = round(1 - request.value, 4)

    return PredictionResponse(
        input=request.value,
        prediction=prediction,
        confidence=confidence
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)