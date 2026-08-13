# AI Phishing Detector API 🛡️

A lightning-fast, machine learning-powered API built with FastAPI that analyzes URLs and predicts whether they are safe or malicious (phishing).

This project was built to prioritize real-time inference speed and security. Instead of relying on slow, risky HTML web-scraping, the AI is trained exclusively on **15 lexical features** extracted directly from the URL string. It also implements an industry-standard **Defense in Depth** architecture using an Allowlist to bypass AI processing for known trusted domains, eliminating false positives for major platforms.

## 🚀 Tech Stack
* **Framework:** FastAPI, Python
* **Machine Learning:** Scikit-Learn (Random Forest Classifier), Pandas, Joblib
* **Server:** Uvicorn
* **Deployment:** Vercel (Serverless Functions)

## 🧠 How It Works
1. **Request Intake:** The API receives a POST request containing a target URL.
2. **Allowlist Verification:** The URL domain is checked against a static Allowlist of highly trusted global domains (e.g., Google, GitHub, Microsoft). If matched, it is immediately flagged as safe.
3. **Lexical Feature Extraction:** If the domain is unknown, a custom extraction pipeline breaks the URL string down into 15 mathematical and structural features (e.g., Character Ratios, Subdomain Counts, IP-based routing).
4. **AI Prediction:** The extracted features are fed into a pre-trained Random Forest model which returns a `safe` or `malicious` verdict.

## 📡 API Endpoints

### 1. Health Check
* **Endpoint:** `GET /`
* **Description:** Verifies the API is live.
* **Response:**
  ```json
  {
    "message": "AI Phishing Detector API is live!"
  }
  ```

### 2. Predict URL
* **Endpoint:** `POST /api/predict`
* **Description:** Analyzes a URL and returns a security verdict.
* **Request Body:**
  ```json
  {
    "url": "http://secure-update-paypal-account-login.com/auth"
  }
  ```
* **Response Body:**
  ```json
  {
    "url": "http://secure-update-paypal-account-login.com/auth",
    "status": "malicious",
    "note": "Analyzed by AI"
  }
  ```

## 💻 Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/shresth637/phishing-detactor.git
   cd phishing-detactor
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the Uvicorn server:
   ```bash
   uvicorn api.index:app --reload
   ```

4. Test the API: Open your browser and navigate to `http://127.0.0.1:8000/docs` to use the interactive Swagger UI.
