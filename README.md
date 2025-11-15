# Email Classification API

A FastAPI application that classifies emails into predefined categories using zero-shot learning with the Facebook BART model.

## Features

- **Zero-Shot Classification**: Uses Facebook BART model for classification without task-specific training
- **Categories**: Classifies emails into:
  - application submitted
  - call for interview
  - rejected
- **RESTful API**: Easy-to-use HTTP endpoints
- **Confidence Scores**: Returns confidence scores for each classification
- **Health Check**: Built-in health check endpoint

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Transformers
- PyTorch
- Pydantic

## Installation

1. Clone the repository:
```bash
git clone https://github.com/suyogrdahal/email-classification-api.git
cd email-classification-api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /health
```
Returns the health status and model loading state.

### Classify Email
```
POST /classify
```

Request body:
```json
{
  "sender": "hr@company.com",
  "subject": "We are pleased to inform you",
  "body": "Dear Candidate, we are happy to offer you an interview slot..."
}
```

Response:
```json
{
  "sender": "hr@company.com",
  "subject": "We are pleased to inform you",
  "classification": "call for interview",
  "confidence": 0.9876
}
```

### Get Categories
```
GET /categories
```
Returns the list of available classification categories.

## Interactive API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Model Details

- **Model**: facebook/bart-large-mnli
- **Task**: Zero-shot classification
- **Framework**: Hugging Face Transformers
- **Languages**: English

## Example Usage

Using Python requests library:
```python
import requests

url = "http://localhost:8000/classify"
email = {
    "sender": "recruiter@company.com",
    "subject": "Interview Scheduled",
    "body": "Your interview has been scheduled for next Monday at 10 AM."
}

response = requests.post(url, json=email)
print(response.json())
```

Using curl:
```bash
curl -X POST "http://localhost:8000/classify" \
  -H "Content-Type: application/json" \
  -d '{"sender":"hr@company.com","subject":"Interview Call","body":"We would like to call you for an interview"}'
```

## Performance Notes

- The model downloads approximately 1.6GB on first run (cached locally)
- First classification request may take 10-30 seconds as the model loads
- Subsequent requests are faster (typically < 1 second)
- For production, consider using GPU acceleration

## Future Improvements

- Add batch classification endpoint
- Implement caching layer
- Add model quantization for faster inference
- Support for custom categories
- Rate limiting and authentication
- Docker containerization

## License

MIT

## Author

Suyog Rdahal
