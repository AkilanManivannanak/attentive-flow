from backend.schemas import CampaignBrief, CampaignType, ExperimentPlan


def create_experiment_plan(brief: CampaignBrief) -> ExperimentPlan:
    if brief.campaign_type == CampaignType.abandoned_cart:
        return ExperimentPlan(
            hypothesis=(
                "Personalized cart reminders that mention product category and cart value "
                "will drive higher click-through and checkout completion than generic reminders."
            ),
            variant_a="Value-focused message emphasizing the items left in cart and easy checkout.",
            variant_b="Loyalty-focused message emphasizing customer tier and shopping momentum.",
            primary_metric="conversion_rate",
            secondary_metrics=[
                "click_through_rate",
                "recovered_revenue",
                "unsubscribe_rate",
            ],
        )

    if brief.campaign_type == CampaignType.browse_abandonment:
        return ExperimentPlan(
            hypothesis=(
                "Personalized browse reminders based on favorite category will increase return visits "
                "compared with generic product discovery messages."
            ),
            variant_a="Category-personalized reminder.",
            variant_b="New-arrivals discovery message.",
            primary_metric="click_through_rate",
            secondary_metrics=[
                "site_return_rate",
                "add_to_cart_rate",
                "conversion_rate",
            ],
        )

    if brief.campaign_type == CampaignType.winback:
        return ExperimentPlan(
            hypothesis=(
                "Winback messages that reference customer history and preferred category "
                "will reactivate more inactive customers than generic promotional messages."
            ),
            variant_a="Personalized category-based reactivation message.",
            variant_b="Loyalty/status-based reactivation message.",
            primary_metric="repeat_purchase_rate",
            secondary_metrics=[
                "click_through_rate",
                "recovered_customers",
                "unsubscribe_rate",
            ],
        )

    if brief.campaign_type == CampaignType.product_drop:
        return ExperimentPlan(
            hypothesis=(
                "Early-access product drop messaging for high-value and loyalty customers "
                "will increase launch conversion versus standard announcement messaging."
            ),
            variant_a="Early-access message for loyalty/high-value customers.",
            variant_b="Product-benefit message focused on the new collection.",
            primary_metric="launch_conversion_rate",
            secondary_metrics=[
                "click_through_rate",
                "revenue_per_recipient",
                "sell_through_rate",
            ],
        )

    if brief.campaign_type == CampaignType.loyalty_reward:
        return ExperimentPlan(
            hypothesis=(
                "Reward-focused messages personalized by loyalty tier will increase redemption "
                "compared with generic loyalty reminders."
            ),
            variant_a="Tier-personalized reward reminder.",
            variant_b="Benefit-focused loyalty message.",
            primary_metric="reward_redemption_rate",
            secondary_metrics=[
                "click_through_rate",
                "repeat_purchase_rate",
                "loyalty_engagement_rate",
            ],
        )

    return ExperimentPlan(
        hypothesis="Personalized lifecycle messaging will outperform generic campaign messaging.",
        variant_a="Personalized message.",
        variant_b="Generic message.",
        primary_metric="conversion_rate",
        secondary_metrics=[
            "click_through_rate",
            "revenue_per_recipient",
        ],
    )
