from typing import List

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


def generate_messages(
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
