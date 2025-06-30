from app.services.openai import run_gpt_completion

def process_email(subject: str, body: str):
    prompt = f"""
You are an email triage assistant.

Given the subject and body of an email, classify it into one of: ["sales", "support", "other"], summarize the content, and suggest a brief professional reply.

Subject: {subject}
Body:
{body}

Respond in JSON like:
{{"category": "...", "summary": "...", "suggested_reply": "..."}}
"""

    response = run_gpt_completion(prompt)
    return response
