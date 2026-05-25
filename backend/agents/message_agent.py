import json
from typing import List

from openai import OpenAI

from backend.config import OPENAI_API_KEY, MODEL_NAME, USE_LLM_COPY
from backend.schemas import (
    CampaignBrief,
    Channel,
    Customer,
    MessageVariant,
)


def build_sms_message(brief: CampaignBrief, customer: Customer) -> MessageVariant:
    body = (
        f"{customer.first_name}, your {customer.favorite_category} picks "
        f"worth ${customer.cart_value:.2f} are still waiting. "
        f"Complete your order today. Reply STOP to opt out."
    )

    return MessageVariant(
        channel=Channel.sms,
        body=body,
        cta="Complete your order",
        personalization_used=[
            "first_name",
            "favorite_category",
            "cart_value",
        ],
    )


def build_email_message(brief: CampaignBrief, customer: Customer) -> MessageVariant:
    subject = f"Your cart is still waiting, {customer.first_name}"

    body = (
        f"Hi {customer.first_name},\n\n"
        f"You left some {customer.favorite_category} items in your cart. "
        f"Your current cart value is ${customer.cart_value:.2f}.\n\n"
        f"As a {customer.loyalty_tier} loyalty member, now is a great time "
        f"to complete your order and keep your shopping momentum going.\n\n"
        f"Return to your cart to finish checkout."
    )

    return MessageVariant(
        channel=Channel.email,
        subject=subject,
        body=body,
        cta="Return to cart",
        personalization_used=[
            "first_name",
            "favorite_category",
            "cart_value",
            "loyalty_tier",
        ],
    )


def build_push_message(brief: CampaignBrief, customer: Customer) -> MessageVariant:
    body = (
        f"{customer.first_name}, your {customer.favorite_category} cart is waiting. "
        f"Tap to complete your order."
    )

    return MessageVariant(
        channel=Channel.push,
        body=body,
        cta="Open app",
        personalization_used=[
            "first_name",
            "favorite_category",
        ],
    )


def build_rcs_message(brief: CampaignBrief, customer: Customer) -> MessageVariant:
    body = (
        f"Hi {customer.first_name}, your {customer.favorite_category} picks "
        f"are still in your cart. Want to finish checkout now?"
    )

    return MessageVariant(
        channel=Channel.rcs,
        body=body,
        cta="Finish checkout",
        personalization_used=[
            "first_name",
            "favorite_category",
        ],
    )


def generate_template_messages(
    brief: CampaignBrief,
    sample_customer: Customer,
) -> List[MessageVariant]:
    messages = []

    for channel in brief.channels:
        if channel == Channel.sms:
            messages.append(build_sms_message(brief, sample_customer))

        elif channel == Channel.email:
            messages.append(build_email_message(brief, sample_customer))

        elif channel == Channel.push:
            messages.append(build_push_message(brief, sample_customer))

        elif channel == Channel.rcs:
            messages.append(build_rcs_message(brief, sample_customer))

    return messages


def build_llm_prompt(brief: CampaignBrief, customer: Customer) -> str:
    return f"""
You are an AI lifecycle marketing workflow assistant.

Generate channel-specific ecommerce campaign messages for this campaign.

Campaign:
- Raw brief: {brief.raw_brief}
- Campaign type: {brief.campaign_type.value}
- Goal: {brief.goal}
- Channels: {[channel.value for channel in brief.channels]}
- Audience rules: {brief.audience_rules}
- Personalization fields: {brief.personalization_fields}

Customer:
- first_name: {customer.first_name}
- favorite_category: {customer.favorite_category}
- cart_value: {customer.cart_value}
- loyalty_tier: {customer.loyalty_tier}
- lifetime_value: {customer.lifetime_value}
- purchase_count: {customer.purchase_count}
- last_purchase_days_ago: {customer.last_purchase_days_ago}

Rules:
- Return valid JSON only.
- Output must be a list of message objects.
- Each object must contain:
  - channel: one of sms, email, push, rcs
  - subject: string or null
  - body: string
  - cta: string
  - personalization_used: list of strings
- SMS must include "Reply STOP to opt out."
- Push copy must be short.
- Do not claim false urgency like "only 1 left" unless given inventory data.
- Do not invent discounts.
- Keep the tone clear, helpful, and conversion-oriented.

Example JSON shape:
[
  {{
    "channel": "sms",
    "subject": null,
    "body": "Message here. Reply STOP to opt out.",
    "cta": "Complete your order",
    "personalization_used": ["first_name", "favorite_category"]
  }}
]
"""


def parse_llm_messages(raw_text: str) -> List[MessageVariant]:
    cleaned = raw_text.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned.removeprefix("```json").removesuffix("```").strip()
    elif cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```").removesuffix("```").strip()

    parsed = json.loads(cleaned)

    if not isinstance(parsed, list):
        raise ValueError("LLM response must be a JSON list.")

    return [MessageVariant(**item) for item in parsed]


def generate_llm_messages(
    brief: CampaignBrief,
    sample_customer: Customer,
) -> List[MessageVariant]:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not configured.")

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.4,
        messages=[
            {
                "role": "system",
                "content": (
                    "You generate compliant lifecycle marketing messages. "
                    "You must return valid JSON only."
                ),
            },
            {
                "role": "user",
                "content": build_llm_prompt(brief, sample_customer),
            },
        ],
    )

    raw_text = response.choices[0].message.content or ""
    messages = parse_llm_messages(raw_text)

    requested_channels = {channel.value for channel in brief.channels}
    filtered_messages = [
        message for message in messages if message.channel.value in requested_channels
    ]

    if not filtered_messages:
        raise ValueError("LLM returned no usable messages for requested channels.")

    return filtered_messages


def generate_messages(
    brief: CampaignBrief,
    sample_customer: Customer,
) -> List[MessageVariant]:
    """
    Generate campaign messages.

    Preferred path:
    - LLM-powered generation if OPENAI_API_KEY exists and USE_LLM_COPY=true.

    Fallback path:
    - Deterministic templates if LLM is unavailable, invalid, or disabled.
    """

    if USE_LLM_COPY and OPENAI_API_KEY:
        try:
            return generate_llm_messages(brief, sample_customer)
        except Exception:
            return generate_template_messages(brief, sample_customer)

    return generate_template_messages(brief, sample_customer)
