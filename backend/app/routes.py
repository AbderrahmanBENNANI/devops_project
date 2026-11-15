import os, stripe
from flask import Blueprint, request, jsonify, send_file
from pydantic import ValidationError
from io import BytesIO
from .schemas import CVData, LetterData
from .pdf import build_cv, build_letter

api = Blueprint("api", __name__)

def parse(model):
    try:
        return model.model_validate(request.get_json(force=True))
    except ValidationError as exc:
        return None, exc.errors()
    except Exception:
        return None, [{"msg": "Invalid JSON body"}]

@api.post("/documents/cv/pdf")
def cv_pdf():
    parsed = parse(CVData)
    if isinstance(parsed, tuple): return jsonify(error="validation_error", details=parsed[1]), 400
    pdf = build_cv(parsed)
    return send_file(BytesIO(pdf), mimetype="application/pdf", as_attachment=True, download_name="mon-cv.pdf")

@api.post("/documents/letter/pdf")
def letter_pdf():
    parsed = parse(LetterData)
    if isinstance(parsed, tuple): return jsonify(error="validation_error", details=parsed[1]), 400
    pdf = build_letter(parsed)
    return send_file(BytesIO(pdf), mimetype="application/pdf", as_attachment=True, download_name="lettre-motivation.pdf")

@api.post("/payments/checkout")
def checkout():
    key = os.getenv("STRIPE_SECRET_KEY")
    if not key:
        return jsonify(error="payments_not_configured"), 503
    stripe.api_key = key
    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=[{"price_data": {"currency": "eur", "product_data": {"name": "Export PDF"},
                         "unit_amount": 199}, "quantity": 1}],
            success_url=os.getenv("STRIPE_SUCCESS_URL"),
            cancel_url=os.getenv("STRIPE_CANCEL_URL"),
        )
        return jsonify(checkout_url=session.url)
    except Exception:
        return jsonify(error="payment_provider_error"), 502

@api.post("/payments/webhook")
def stripe_webhook():
    secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    if not secret:
        return jsonify(error="webhook_not_configured"), 503
    payload = request.get_data()
    signature = request.headers.get("Stripe-Signature", "")
    try:
        event = stripe.Webhook.construct_event(payload, signature, secret)
    except Exception:
        return jsonify(error="invalid_webhook_signature"), 400
    # TODO production: enregistrer l'événement idempotent et délivrer un droit d'export
    if event["type"] == "checkout.session.completed":
        app_log = "payment_completed"
    return jsonify(received=True)
