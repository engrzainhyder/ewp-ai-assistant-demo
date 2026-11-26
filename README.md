# EWP AI Assistant — Portfolio Demo

[![tests](https://github.com/engrzainhyder/ewp-ai-assistant-demo/actions/workflows/tests.yml/badge.svg)](https://github.com/engrzainhyder/ewp-ai-assistant-demo/actions) ![python](https://img.shields.io/badge/python-3.10%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green)

A bilingual (English / Roman-Urdu / Urdu) FAQ chatbot built as a demonstration of the kind of assistant I developed for **Elliott Wave Pakistan (B&B Academy)**.

> **Note:** This is an independent, simplified demo using placeholder content. It contains none of the company's production code, FAQ scripts, pricing, contact details or branding.

## What it shows
- **Intent matching** with character n-gram TF-IDF and cosine similarity (pure Python, no heavy ML model). It tolerates typos and Roman-Urdu spelling variations.
- **Language detection** (English, Roman-Urdu, Urdu script).
- **Confidence threshold and fallback**, so unclear questions go to a human instead of getting a wrong answer.
- **Flask JSON API** (`POST /chat`) and a small chat page.
- **Tests** with pytest.

## Run it
```bash
pip install -r requirements.txt
python -m assistant.app        # http://localhost:5000
pytest
```

API example:
```bash
curl -X POST localhost:5000/chat -H 'Content-Type: application/json' -d '{"message":"fee kitni hai"}'
```

## Architecture
```
User message -> normalize -> n-gram TF-IDF vector -> cosine vs. FAQ patterns
            -> best score >= threshold ? FAQ answer : human-handoff fallback
```

## My role
Designed and built the conversational assistant for the academy's enrollment enquiries (production version is private).

## Possible extensions
Sentence-embedding matching, WhatsApp integration, admin UI for editing FAQs, analytics on unanswered questions.
