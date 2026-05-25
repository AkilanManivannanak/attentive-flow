import json
import random
from pathlib import Path
from datetime import datetime, timedelta, timezone

FIRST_NAMES = [
    "Maya", "Jordan", "Avery", "Taylor", "Riley",
    "Casey", "Morgan", "Alex", "Sam", "Jamie"
]

CATEGORIES = [
    "women's fashion",
    "men's fashion",
    "home decor",
    "beauty",
    "fitness",
    "electronics",
    "kids apparel"
]

LOYALTY_TIERS = ["bronze", "silver", "gold", "platinum"]

EVENT_TYPES = [
    "product_viewed",
    "cart_abandoned",
    "purchase_completed",
    "browse_abandoned",
    "email_clicked",
    "sms_clicked",
    "push_opened",
    "price_drop",
    "back_in_stock"
]


def generate_customer(index: int) -> dict:
    first_name = random.choice(FIRST_NAMES)

    return {
        "user_id": f"u_{index:04d}",
        "first_name": first_name,
        "email": f"{first_name.lower()}{index}@example.com",
        "email_opt_in": random.random() < 0.85,
        "sms_opt_in": random.random() < 0.70,
        "push_opt_in": random.random() < 0.45,
        "rcs_supported": random.random() < 0.55,
        "app_installed": random.random() < 0.50,
        "loyalty_tier": random.choice(LOYALTY_TIERS),
        "cart_value": round(random.uniform(20, 350), 2),
        "favorite_category": random.choice(CATEGORIES),
        "last_purchase_days_ago": random.randint(1, 180),
        "purchase_count": random.randint(0, 20),
        "lifetime_value": round(random.uniform(25, 2500), 2)
    }


def generate_event(customer: dict) -> dict:
    days_ago = random.randint(0, 45)
    event_time = datetime.now(timezone.utc) - timedelta(days=days_ago)

    return {
        "event_id": f"evt_{random.randint(100000, 999999)}",
        "user_id": customer["user_id"],
        "event_type": random.choice(EVENT_TYPES),
        "timestamp": event_time.isoformat(),
        "category": customer["favorite_category"],
        "cart_value": customer["cart_value"],
        "channel": random.choice(["sms", "email", "push", "rcs", "web"])
    }


def main(num_customers: int = 1000, events_per_customer: int = 5) -> None:
    output_dir = Path(__file__).parent

    customers = [generate_customer(i) for i in range(1, num_customers + 1)]

    events = []
    for customer in customers:
        for _ in range(events_per_customer):
            events.append(generate_event(customer))

    customers_path = output_dir / "synthetic_customers.json"
    events_path = output_dir / "synthetic_events.json"

    with open(customers_path, "w") as f:
        json.dump(customers, f, indent=2)

    with open(events_path, "w") as f:
        json.dump(events, f, indent=2)

    print(f"Generated {len(customers)} customers at {customers_path}")
    print(f"Generated {len(events)} events at {events_path}")


if __name__ == "__main__":
    main()
