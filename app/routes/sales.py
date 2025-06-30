from fastapi import APIRouter
from app.agents.sales_agent import process_email
from app.services.gmail import get_latest_unread_emails

router = APIRouter()

@router.post("/agents/sales")
def run_sales_agent(n: int = 3):
    emails = get_latest_unread_emails(n)
    results = []

    for email in emails:
        subject = email.get("subject", "")
        body = email.get("body", "")
        result = process_email(subject, body)
        results.append({
            "subject": subject,
            "category": result,
        })

    return results
