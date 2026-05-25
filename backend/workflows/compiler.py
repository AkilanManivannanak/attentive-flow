from backend.agents.brief_parser import parse_brief
from backend.agents.segmentation_agent import segment_customers
from backend.agents.message_agent import generate_messages
from backend.agents.compliance_agent import check_compliance
from backend.agents.experiment_agent import create_experiment_plan
from backend.agents.repair_agent import repair_campaign
from backend.evals.scoring import evaluate_campaign
from backend.schemas import (
    Customer,
    MarketingWorkflow,
    WorkflowStep,
)


def build_workflow_steps(messages) -> list[WorkflowStep]:
    steps = []

    for index, message in enumerate(messages, start=1):
        if message.channel.value == "sms":
            delay = "1 hour after cart abandonment"
            condition = "customer has sms_opt_in=true"
            success_metric = "sms_click_through_rate"

        elif message.channel.value == "email":
            delay = "24 hours after SMS if no click"
            condition = "customer has email_opt_in=true and previous step did not click"
            success_metric = "email_click_through_rate"

        elif message.channel.value == "push":
            delay = "2 hours after email if no conversion"
            condition = "customer has app_installed=true and push_opt_in=true"
            success_metric = "push_open_rate"

        elif message.channel.value == "rcs":
            delay = "1 hour after campaign trigger"
            condition = "customer has sms_opt_in=true and rcs_supported=true"
            success_metric = "rcs_click_through_rate"

        else:
            delay = "Immediately"
            condition = None
            success_metric = "conversion_rate"

        steps.append(
            WorkflowStep(
                step_id=f"step_{index}",
                channel=message.channel,
                delay=delay,
                condition=condition,
                message=message,
                success_metric=success_metric,
            )
        )

    return steps


def compile_workflow(raw_brief: str) -> MarketingWorkflow:
    brief = parse_brief(raw_brief)
    segment = segment_customers(brief)

    if not segment["sample_customers"]:
        raise ValueError("No eligible customers found for this campaign brief.")

    sample_customer = Customer(**segment["sample_customers"][0])

    messages = generate_messages(brief, sample_customer)
    compliance = check_compliance(messages, sample_customer)
    experiment_plan = create_experiment_plan(brief)
    evaluation = evaluate_campaign(messages, compliance)
    steps = build_workflow_steps(messages)

    repair_result = repair_campaign(messages, sample_customer)

    workflow_json = {
        "campaign_type": brief.campaign_type.value,
        "goal": brief.goal,
        "audience": {
            "summary": segment["audience_summary"],
            "rules": brief.audience_rules,
            "total_matching_customers": segment["total_matching_customers"],
            "channel_counts": segment["channel_counts"],
        },
        "workflow_steps": [
            {
                "step_id": step.step_id,
                "channel": step.channel.value,
                "delay": step.delay,
                "condition": step.condition,
                "message": step.message.model_dump(),
                "success_metric": step.success_metric,
            }
            for step in steps
        ],
        "experiment_plan": experiment_plan.model_dump(),
        "compliance": compliance.model_dump(),
        "evaluation": evaluation.model_dump(),
        "repair_result": repair_result,
        "sample_customer": sample_customer.model_dump(),
    }

    return MarketingWorkflow(
        campaign_brief=brief,
        audience_summary=segment["audience_summary"],
        steps=steps,
        experiment_plan=experiment_plan,
        compliance=compliance,
        evaluation=evaluation,
        workflow_json=workflow_json,
    )
