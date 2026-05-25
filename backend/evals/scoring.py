from typing import List

from backend.schemas import (
    Channel,
    ComplianceResult,
    EvaluationScores,
    MessageVariant,
)


def score_personalization(messages: List[MessageVariant]) -> tuple[int, list[str]]:
    issues = []

    if not messages:
        return 0, ["No messages were generated."]

    total_fields = sum(len(message.personalization_used) for message in messages)
    avg_fields = total_fields / len(messages)

    if avg_fields >= 3:
        score = 9
    elif avg_fields >= 2:
        score = 7
    elif avg_fields >= 1:
        score = 5
    else:
        score = 2
        issues.append("Messages do not use meaningful personalization fields.")

    return score, issues


def score_clarity(messages: List[MessageVariant]) -> tuple[int, list[str]]:
    issues = []
    score = 10

    for message in messages:
        body = message.body.strip()

        if len(body) < 20:
            score -= 3
            issues.append(f"{message.channel.value} message is too short to be clear.")

        if message.channel == Channel.sms and len(body) > 300:
            score -= 2
            issues.append("SMS message may be too long for a concise mobile experience.")

        if message.channel == Channel.push and len(body) > 120:
            score -= 2
            issues.append("Push notification may be too long for lock-screen readability.")

        if not body.endswith((".", "!", "?")):
            score -= 1
            issues.append(f"{message.channel.value} message lacks clean punctuation.")

    return max(score, 0), issues


def score_cta(messages: List[MessageVariant]) -> tuple[int, list[str]]:
    issues = []

    if not messages:
        return 0, ["No CTA can be evaluated because no messages were generated."]

    missing_cta_count = sum(1 for message in messages if not message.cta)

    if missing_cta_count == 0:
        score = 9
    elif missing_cta_count < len(messages):
        score = 6
        issues.append("Some messages are missing explicit calls to action.")
    else:
        score = 3
        issues.append("All messages are missing explicit calls to action.")

    weak_ctas = {"click here", "learn more", "open"}
    for message in messages:
        if message.cta and message.cta.lower().strip() in weak_ctas:
            score -= 1
            issues.append(f"{message.channel.value} CTA is generic: {message.cta}")

    return max(score, 0), issues


def score_compliance(compliance: ComplianceResult) -> tuple[int, list[str]]:
    if compliance.passed:
        return 10, []

    score = 10
    issues = []

    for issue in compliance.issues:
        issues.append(issue.issue)

        if issue.severity == "high":
            score -= 4
        elif issue.severity == "medium":
            score -= 2
        else:
            score -= 1

    return max(score, 0), issues


def score_channel_fit(messages: List[MessageVariant]) -> tuple[int, list[str]]:
    issues = []
    score = 10

    channels = [message.channel for message in messages]

    if Channel.sms in channels:
        sms_messages = [message for message in messages if message.channel == Channel.sms]
        for message in sms_messages:
            if "stop" not in message.body.lower():
                score -= 3
                issues.append("SMS message does not include STOP opt-out language.")

    if Channel.email in channels:
        email_messages = [message for message in messages if message.channel == Channel.email]
        for message in email_messages:
            if not message.subject:
                score -= 2
                issues.append("Email message is missing a subject line.")

    if Channel.push in channels:
        push_messages = [message for message in messages if message.channel == Channel.push]
        for message in push_messages:
            if len(message.body) > 120:
                score -= 2
                issues.append("Push notification is too long for the channel.")

    return max(score, 0), issues


def evaluate_campaign(
    messages: List[MessageVariant],
    compliance: ComplianceResult,
) -> EvaluationScores:
    personalization_score, personalization_issues = score_personalization(messages)
    clarity_score, clarity_issues = score_clarity(messages)
    cta_score, cta_issues = score_cta(messages)
    compliance_score, compliance_issues = score_compliance(compliance)
    channel_fit_score, channel_fit_issues = score_channel_fit(messages)

    all_issues = (
        personalization_issues
        + clarity_issues
        + cta_issues
        + compliance_issues
        + channel_fit_issues
    )

    overall_score = round(
        (
            personalization_score
            + clarity_score
            + cta_score
            + compliance_score
            + channel_fit_score
        )
        / 5
    )

    return EvaluationScores(
        personalization_score=personalization_score,
        clarity_score=clarity_score,
        cta_score=cta_score,
        compliance_score=compliance_score,
        channel_fit_score=channel_fit_score,
        overall_score=overall_score,
        issues=all_issues,
    )
