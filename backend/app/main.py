from fastapi import FastAPI

app = FastAPI(
    title="SAGE AI Teacher",
    description="Adaptive AI Teacher API",
    version="1.0.0",
)

@app.get("/")
def root():
    return {"message": "SAGE AI Teacher API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
