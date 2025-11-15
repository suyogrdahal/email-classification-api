from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
import logging

from transformers import pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Email Classification API",
    description="Classifies emails into job-related categories",
    version="2.0.0"
)

# Lazy-loaded classifier
classifier = None

def load_classifier():
    """Load model only once"""
    global classifier
    if classifier is None:
        try:
            classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=-1  # CPU
            )
            logger.info("Zero-shot classifier loaded.")
        except Exception as e:
            logger.error(f"Error loading classifier: {e}")
            raise


# 🔥 OPTIMIZED categories
CATEGORIES = [
    "application_received",
    "interview_invitation",
    "application_rejected",
    "job_offer",
    "not_job_related"
]

# Friendly names for output
CATEGORY_MAPPING = {
    "application_received": "application submitted",
    "interview_invitation": "call for interview",
    "application_rejected": "rejected",
    "job_offer": "job offer",
    "not_job_related": "not related to job application",
}


class EmailRequest(BaseModel):
    sender: str
    subject: str
    body: str


class ClassificationResponse(BaseModel):
    sender: str
    subject: str
    classification: Literal[
        "application submitted",
        "call for interview",
        "rejected",
        "job offer",
        "not job related (spam/marketing)",
        "not related to job application"
    ]
    confidence: float


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": classifier is not None
    }


@app.post("/classify", response_model=ClassificationResponse)
def classify_email(email: EmailRequest):
    try:
        load_classifier()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Model load error: {str(e)}")

    # Combine subject + body
    text = f"Subject: {email.subject}\n\nBody: {email.body}"

    try:
        result = classifier(
            text,
            CATEGORIES,
            hypothesis_template="The email is about {}.",
            multi_class=False
        )

        top_label = result["labels"][0]
        top_score = float(result["scores"][0])

        friendly = CATEGORY_MAPPING.get(top_label, top_label)

        logger.info(f"Classified '{email.subject}' as '{friendly}' ({top_score:.4f})")

        return ClassificationResponse(
            sender=email.sender,
            subject=email.subject,
            classification=friendly,
            confidence=round(top_score, 4)
        )

    except Exception as e:
        logger.error(f"Classification error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
