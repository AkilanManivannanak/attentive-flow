from typing import List

from backend.schemas import (
    Channel,
    ComplianceIssue,
    ComplianceResult,
    Customer,
    MessageVariant,
)


RISKY_URGENCY_TERMS = [
    "only 1 left",
    "last chance",
    "final chance",
    "expires immediately",
    "guaranteed",
]

DISCOUNT_TERMS = [
    "% off",
    "discount",
    "free",
    "coupon",
    "promo code",
]


def check_sms_compliance(message: MessageVariant) -> List[ComplianceIssue]:
    issues = []

    body_lower = message.body.lower()

    if "stop" not in body_lower and "opt out" not in body_lower:
        issues.append(
            ComplianceIssue(
                severity="high",
                issue="SMS message is missing opt-out language.",
                recommendation="Add clear opt-out language such as 'Reply STOP to opt out.'",
            )
        )

    if len(message.body) > 300:
        issues.append(
            ComplianceIssue(
                severity="medium",
                issue=f"SMS message is too long at {len(message.body)} characters.",
                recommendation="Shorten SMS copy to improve readability and deliverability.",
            )
        )

    return issues


def check_push_compliance(
    message: MessageVariant,
    customer: Customer | None = None,
) -> List[ComplianceIssue]:
    issues = []

    if customer is not None:
        if not customer.app_installed:
            issues.append(
                ComplianceIssue(
                    severity="high",
                    issue="Push message generated for a customer without the app installed.",
                    recommendation="Only send push notifications to customers with app_installed=true.",
                )
            )

        if not customer.push_opt_in:
            issues.append(
                ComplianceIssue(
                    severity="high",
                    issue="Push message generated for a customer who has not opted into push.",
                    recommendation="Only send push notifications to customers with push_opt_in=true.",
                )
            )

    if len(message.body) > 120:
        issues.append(
            ComplianceIssue(
                severity="medium",
                issue=f"Push notification is long at {len(message.body)} characters.",
                recommendation="Shorten push copy so it is easier to read on mobile lock screens.",
            )
        )

    return issues


def check_email_compliance(message: MessageVariant) -> List[ComplianceIssue]:
    issues = []

    if not message.subject:
        issues.append(
            ComplianceIssue(
                severity="medium",
                issue="Email message is missing a subject line.",
                recommendation="Add a concise, personalized subject line.",
            )
        )

    if message.subject and len(message.subject) > 80:
        issues.append(
            ComplianceIssue(
                severity="low",
                issue=f"Email subject is long at {len(message.subject)} characters.",
                recommendation="Shorten subject line for better inbox readability.",
            )
        )

    return issues


def check_rcs_compliance(message: MessageVariant) -> List[ComplianceIssue]:
    issues = []

    if len(message.body) > 500:
        issues.append(
            ComplianceIssue(
                severity="medium",
                issue=f"RCS message is long at {len(message.body)} characters.",
                recommendation="Make RCS message more concise.",
            )
        )

    return issues


def check_risky_language(message: MessageVariant) -> List[ComplianceIssue]:
    issues = []
    body_lower = message.body.lower()

    for term in RISKY_URGENCY_TERMS:
        if term in body_lower:
            issues.append(
                ComplianceIssue(
                    severity="medium",
                    issue=f"Message uses risky urgency language: '{term}'.",
                    recommendation="Avoid unsupported urgency claims unless inventory or expiration data proves it.",
                )
            )

    return issues


def check_discount_dependency(messages: List[MessageVariant]) -> List[ComplianceIssue]:
    issues = []

    discount_count = 0
    for message in messages:
        body_lower = message.body.lower()
        if any(term in body_lower for term in DISCOUNT_TERMS):
            discount_count += 1

    if discount_count == len(messages) and messages:
        issues.append(
            ComplianceIssue(
                severity="low",
                issue="Every message relies on discount language.",
                recommendation="Create at least one non-discount variant focused on product value, loyalty, or convenience.",
            )
        )

    return issues


def check_compliance(
    messages: List[MessageVariant],
    customer: Customer | None = None,
) -> ComplianceResult:
    all_issues = []

    for message in messages:
        if message.channel == Channel.sms:
            all_issues.extend(check_sms_compliance(message))

        elif message.channel == Channel.email:
            all_issues.extend(check_email_compliance(message))

        elif message.channel == Channel.push:
            all_issues.extend(check_push_compliance(message, customer))

        elif message.channel == Channel.rcs:
            all_issues.extend(check_rcs_compliance(message))

        all_issues.extend(check_risky_language(message))

    all_issues.extend(check_discount_dependency(messages))

    return ComplianceResult(
        passed=len(all_issues) == 0,
        issues=all_issues,
    )
