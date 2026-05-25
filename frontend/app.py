import json
import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from backend.config import OPENAI_API_KEY, USE_LLM_COPY, MODEL_NAME
from backend.workflows.compiler import compile_workflow


st.set_page_config(
    page_title="AttentiveFlow",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ AttentiveFlow")
st.subheader("Agentic Cross-Channel Marketing Workflow Builder")

st.markdown(
    """
    AttentiveFlow turns ambiguous lifecycle marketing briefs into structured, personalized,
    compliant, and testable workflows across SMS, email, push, and RCS.

    This prototype demonstrates an agent-style marketing automation workflow with:

    - campaign brief parsing
    - audience segmentation
    - LLM-powered or template-based message generation
    - compliance validation
    - A/B test planning
    - campaign scoring
    - automated repair loops
    """
)

llm_status = "Enabled" if USE_LLM_COPY and OPENAI_API_KEY else "Template fallback"
st.caption(f"Message generation mode: **{llm_status}** · Model: `{MODEL_NAME}`")

st.divider()

example_options = {
    "Abandoned Cart": """Create an abandoned cart campaign for customers with cart value above $75.
Use SMS first, email after 24 hours if they do not click, and push if they have the app installed.
Personalize based on first name, cart value, product category, and loyalty tier.""",
    "Winback": """Create a winback campaign for inactive customers who have not purchased in at least 60 days.
Use email first and SMS second for customers who are opted into text messages.
Personalize based on first name, favorite category, last purchase recency, and loyalty tier.""",
    "Product Drop": """Create a product drop campaign for a new limited collection.
Use SMS, RCS, and email.
Prioritize high-value customers and loyalty members.
Personalize based on first name, favorite category, loyalty tier, and lifetime value.""",
}

selected_example = st.selectbox(
    "Choose a demo campaign",
    list(example_options.keys()),
)

brief = st.text_area(
    "Campaign brief",
    value=example_options[selected_example],
    height=180,
)

generate = st.button("Generate Workflow", type="primary")

if generate:
    with st.spinner("Generating workflow..."):
        try:
            workflow_obj = compile_workflow(brief)
            workflow = workflow_obj.model_dump()
            workflow_json = workflow["workflow_json"]
            repair_result = workflow_json["repair_result"]
            repair_summary = repair_result["repair_summary"]

            st.success("Workflow generated")

            st.header("Executive Summary")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Campaign Type",
                    str(workflow["campaign_brief"]["campaign_type"]).replace("CampaignType.", ""),
                )

            with col2:
                st.metric(
                    "Initial Score",
                    workflow["evaluation"]["overall_score"],
                )

            with col3:
                st.metric(
                    "Repaired Score",
                    repair_summary["after_overall_score"],
                    delta=(
                        repair_summary["after_overall_score"]
                        - repair_summary["before_overall_score"]
                    ),
                )

            with col4:
                st.metric(
                    "Matching Customers",
                    workflow_json["audience"]["total_matching_customers"],
                )

            if repair_summary["after_compliance_passed"]:
                st.info(
                    "Automated repair loop succeeded: "
                    f"compliance changed from {repair_summary['before_compliance_passed']} "
                    f"to {repair_summary['after_compliance_passed']}. "
                    f"Removed invalid channels: {repair_summary['removed_channels']}."
                )
            else:
                st.warning(
                    "Repair loop completed, but compliance still needs review."
                )

            st.subheader("Repaired Workflow Preview")

            st.caption(
                "This is the customer-safe workflow after the repair agent removes invalid channel steps."
            )

            for message in repair_result["repaired_messages"]:
                with st.expander(
                    f"Repaired {message['channel'].upper()} Message",
                    expanded=True,
                ):
                    if message.get("subject"):
                        st.write("**Subject:**", message["subject"])

                    st.write("**Message:**")
                    st.write(message["body"])

                    st.write("**CTA:**", message["cta"])

                    personalization_used = message.get("personalization_used", [])
                    if personalization_used:
                        st.write(
                            "**Personalization Used:**",
                            ", ".join(personalization_used),
                        )

            st.divider()

            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
                [
                    "Workflow",
                    "Audience",
                    "Compliance",
                    "Evaluation",
                    "Repair Loop",
                    "JSON Export",
                ]
            )

            with tab1:
                st.header("Initial Generated Workflow Steps")

                st.warning(
                    "These are the initially generated steps before repair. "
                    "The repair agent removes invalid channel steps when customer eligibility fails."
                )

                for step in workflow["steps"]:
                    with st.expander(
                        f"{step['step_id']} — {step['channel'].upper()}",
                        expanded=True,
                    ):
                        st.write("**Delay:**", step["delay"])
                        st.write("**Condition:**", step["condition"])
                        st.write("**Success Metric:**", step["success_metric"])

                        message = step["message"]

                        if message.get("subject"):
                            st.write("**Subject:**", message["subject"])

                        st.write("**Message:**")
                        st.write(message["body"])

                        st.write("**CTA:**", message["cta"])

                        personalization_used = message.get("personalization_used", [])
                        if personalization_used:
                            st.write(
                                "**Personalization Used:**",
                                ", ".join(personalization_used),
                            )

                st.subheader("A/B Test Plan")
                st.json(workflow["experiment_plan"])

            with tab2:
                st.header("Audience Segmentation")

                st.write(workflow["audience_summary"])

                col_a, col_b = st.columns(2)

                with col_a:
                    st.subheader("Audience Rules")
                    st.json(workflow_json["audience"]["rules"])

                with col_b:
                    st.subheader("Channel Eligibility")
                    st.json(workflow_json["audience"]["channel_counts"])

                st.subheader("Sample Customer")
                st.caption(
                    "This customer is used to demonstrate personalization, channel eligibility, compliance checks, and repair."
                )
                st.json(workflow_json["sample_customer"])

            with tab3:
                st.header("Compliance Validation")

                if workflow["compliance"]["passed"]:
                    st.success("Initial workflow passed compliance.")
                else:
                    st.error("Initial workflow failed compliance checks.")

                st.subheader("Initial Compliance Result")
                st.json(workflow["compliance"])

                st.subheader("Repaired Compliance Result")
                if repair_result["repaired_compliance"]["passed"]:
                    st.success("Repaired workflow passed compliance.")
                else:
                    st.error("Repaired workflow still has compliance issues.")

                st.json(repair_result["repaired_compliance"])

            with tab4:
                st.header("Campaign Quality Evaluation")

                evaluation = workflow["evaluation"]
                repaired_evaluation = repair_result["repaired_evaluation"]

                st.subheader("Initial Evaluation")

                score_cols = st.columns(5)

                with score_cols[0]:
                    st.metric("Personalization", evaluation["personalization_score"])
                with score_cols[1]:
                    st.metric("Clarity", evaluation["clarity_score"])
                with score_cols[2]:
                    st.metric("CTA", evaluation["cta_score"])
                with score_cols[3]:
                    st.metric("Compliance", evaluation["compliance_score"])
                with score_cols[4]:
                    st.metric("Channel Fit", evaluation["channel_fit_score"])

                st.write("**Initial Issues:**")
                if evaluation["issues"]:
                    for issue in evaluation["issues"]:
                        st.write(f"- {issue}")
                else:
                    st.write("No issues detected.")

                st.subheader("Repaired Evaluation")
                st.json(repaired_evaluation)

            with tab5:
                st.header("Automated Repair Loop")

                before, after = st.columns(2)

                with before:
                    st.subheader("Before Repair")
                    st.metric(
                        "Compliance Passed",
                        repair_summary["before_compliance_passed"],
                    )
                    st.metric(
                        "Overall Score",
                        repair_summary["before_overall_score"],
                    )
                    st.json(repair_result["original_compliance"])

                with after:
                    st.subheader("After Repair")
                    st.metric(
                        "Compliance Passed",
                        repair_summary["after_compliance_passed"],
                    )
                    st.metric(
                        "Overall Score",
                        repair_summary["after_overall_score"],
                    )
                    st.json(repair_result["repaired_compliance"])

                st.subheader("Repair Summary")
                st.json(repair_summary)

                st.subheader("Repaired Messages")
                for message in repair_result["repaired_messages"]:
                    with st.expander(message["channel"].upper(), expanded=True):
                        if message.get("subject"):
                            st.write("**Subject:**", message["subject"])
                        st.write("**Message:**")
                        st.write(message["body"])
                        st.write("**CTA:**", message["cta"])

            with tab6:
                st.header("Full Workflow JSON")

                st.download_button(
                    label="Download workflow JSON",
                    data=json.dumps(workflow_json, indent=2),
                    file_name="attentiveflow_workflow.json",
                    mime="application/json",
                )

                st.json(workflow_json)

        except Exception as exc:
            st.error(f"Error: {exc}")
