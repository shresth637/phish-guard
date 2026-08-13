from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os
import urllib.parse
from .feature_extraction import extract_features

app = FastAPI()

# Load the AI files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "phishing_model.joblib")
FEATURES_PATH = os.path.join(BASE_DIR, "model", "model_features.joblib")

model = joblib.load(MODEL_PATH)
required_features = joblib.load(FEATURES_PATH)

# Industry Standard: The Allowlist (Top trusted domains to bypass the AI)
TRUSTED_DOMAINS = {
    "google.com", "youtube.com", "facebook.com", "twitter.com", 
    "instagram.com", "linkedin.com", "github.com", "microsoft.com", 
    "apple.com", "amazon.com", "paypal.com"
}

class URLRequest(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"message": "AI Phishing Detector API is live!"}

@app.post("/api/predict")
def predict_url(req: URLRequest):
    # 1. Clean the URL and extract the domain
    parsed = urllib.parse.urlparse(req.url if req.url.startswith('http') else 'http://' + req.url)
    domain = parsed.netloc.replace("www.", "")
    
    # 2. Check the Allowlist FIRST (Defense in Depth)
    if domain in TRUSTED_DOMAINS:
        return {"url": req.url, "status": "safe", "note": "Verified by Allowlist"}

    # 3. If it's an unknown site, ask the AI
    features = extract_features(req.url, required_features)
    prediction = model.predict(features)
    
    status = "safe" if prediction[0] == 1 else "malicious"
    return {"url": req.url, "status": status, "note": "Analyzed by AI"}