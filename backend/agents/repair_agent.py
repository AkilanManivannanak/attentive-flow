from typing import List

from backend.agents.compliance_agent import check_compliance
from backend.evals.scoring import evaluate_campaign
from backend.schemas import (
    Channel,
    ComplianceResult,
    Customer,
    EvaluationScores,
    MessageVariant,
)


def customer_can_receive_channel(customer: Customer, channel: Channel) -> bool:
    if channel == Channel.sms:
        return customer.sms_opt_in

    if channel == Channel.email:
        return customer.email_opt_in

    if channel == Channel.push:
        return customer.app_installed and customer.push_opt_in

    if channel == Channel.rcs:
        return customer.sms_opt_in and customer.rcs_supported

    return False


def repair_messages_for_customer(
    messages: List[MessageVariant],
    customer: Customer,
) -> List[MessageVariant]:
    repaired_messages = []

    for message in messages:
        if customer_can_receive_channel(customer, message.channel):
            repaired_messages.append(message)

    return repaired_messages


def repair_sms_opt_out(messages: List[MessageVariant]) -> List[MessageVariant]:
    repaired_messages = []

    for message in messages:
        if message.channel == Channel.sms:
            body_lower = message.body.lower()

            if "stop" not in body_lower and "opt out" not in body_lower:
                message = message.model_copy(
                    update={
                        "body": f"{message.body.rstrip()} Reply STOP to opt out."
                    }
                )

        repaired_messages.append(message)

    return repaired_messages


def repair_campaign(
    messages: List[MessageVariant],
    customer: Customer,
) -> dict:
    original_compliance = check_compliance(messages, customer)
    original_evaluation = evaluate_campaign(messages, original_compliance)

    repaired_messages = repair_messages_for_customer(messages, customer)
    repaired_messages = repair_sms_opt_out(repaired_messages)

    repaired_compliance = check_compliance(repaired_messages, customer)
    repaired_evaluation = evaluate_campaign(repaired_messages, repaired_compliance)

    removed_channels = [
        message.channel.value
        for message in messages
        if message.channel not in [repaired.channel for repaired in repaired_messages]
    ]

    return {
        "original_compliance": original_compliance.model_dump(),
        "original_evaluation": original_evaluation.model_dump(),
        "repaired_messages": [message.model_dump() for message in repaired_messages],
        "repaired_compliance": repaired_compliance.model_dump(),
        "repaired_evaluation": repaired_evaluation.model_dump(),
        "repair_summary": {
            "removed_channels": removed_channels,
            "before_overall_score": original_evaluation.overall_score,
            "after_overall_score": repaired_evaluation.overall_score,
            "before_compliance_passed": original_compliance.passed,
            "after_compliance_passed": repaired_compliance.passed,
        },
    }
