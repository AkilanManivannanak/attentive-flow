import json
from typing import List

from backend.config import CUSTOMERS_PATH
from backend.schemas import CampaignBrief, Customer


def load_customers() -> List[Customer]:
    with open(CUSTOMERS_PATH, "r") as f:
        raw_customers = json.load(f)

    return [Customer(**customer) for customer in raw_customers]


def customer_matches_rules(customer: Customer, brief: CampaignBrief) -> bool:
    rules = brief.audience_rules

    cart_value_min = rules.get("cart_value_min")
    if cart_value_min is not None and customer.cart_value < cart_value_min:
        return False

    lifetime_value_min = rules.get("lifetime_value_min")
    if lifetime_value_min is not None and customer.lifetime_value < lifetime_value_min:
        return False

    last_purchase_days_ago_min = rules.get("last_purchase_days_ago_min")
    if (
        last_purchase_days_ago_min is not None
        and customer.last_purchase_days_ago < last_purchase_days_ago_min
    ):
        return False

    if rules.get("requires_sms_opt_in") and not customer.sms_opt_in:
        return False

    if rules.get("requires_email_opt_in") and not customer.email_opt_in:
        return False

    return True


def get_channel_eligible_customers(
    customers: List[Customer],
    channel: str,
) -> List[Customer]:
    if channel == "sms":
        return [customer for customer in customers if customer.sms_opt_in]

    if channel == "email":
        return [customer for customer in customers if customer.email_opt_in]

    if channel == "push":
        return [
            customer
            for customer in customers
            if customer.push_opt_in and customer.app_installed
        ]

    if channel == "rcs":
        return [
            customer
            for customer in customers
            if customer.sms_opt_in and customer.rcs_supported
        ]

    return customers


def segment_customers(brief: CampaignBrief, limit: int = 25) -> dict:
    customers = load_customers()

    matching_customers = [
        customer for customer in customers if customer_matches_rules(customer, brief)
    ]

    channel_counts = {}
    for channel in brief.channels:
        eligible_for_channel = get_channel_eligible_customers(
            matching_customers,
            channel.value,
        )
        channel_counts[channel.value] = len(eligible_for_channel)

    sample_customers = matching_customers[:limit]

    return {
        "audience_summary": (
            f"Found {len(matching_customers)} customers matching campaign rules. "
            f"Channel eligibility: {channel_counts}."
        ),
        "total_matching_customers": len(matching_customers),
        "channel_counts": channel_counts,
        "sample_customers": [customer.model_dump() for customer in sample_customers],
    }
