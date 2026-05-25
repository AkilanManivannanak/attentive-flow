from backend.schemas import CampaignBrief, CampaignType, Channel


def infer_campaign_type(brief: str) -> CampaignType:
    text = brief.lower()

    if "abandoned cart" in text or "cart" in text:
        return CampaignType.abandoned_cart

    if "browse" in text or "viewed" in text:
        return CampaignType.browse_abandonment

    if "winback" in text or "win back" in text or "inactive" in text:
        return CampaignType.winback

    if "product drop" in text or "launch" in text or "new collection" in text:
        return CampaignType.product_drop

    if "loyalty" in text or "reward" in text or "vip" in text:
        return CampaignType.loyalty_reward

    return CampaignType.abandoned_cart


def infer_channels(brief: str) -> list[Channel]:
    text = brief.lower()
    channels = []

    if "sms" in text or "text" in text:
        channels.append(Channel.sms)

    if "email" in text:
        channels.append(Channel.email)

    if "push" in text or "notification" in text:
        channels.append(Channel.push)

    if "rcs" in text:
        channels.append(Channel.rcs)

    if not channels:
        channels = [Channel.sms, Channel.email]

    return channels


def infer_goal(campaign_type: CampaignType) -> str:
    goals = {
        CampaignType.abandoned_cart: "Recover abandoned cart revenue",
        CampaignType.browse_abandonment: "Re-engage shoppers who browsed but did not purchase",
        CampaignType.winback: "Reactivate inactive customers and drive repeat purchases",
        CampaignType.product_drop: "Drive awareness and conversion for a new product launch",
        CampaignType.loyalty_reward: "Increase loyalty engagement and reward redemption",
    }

    return goals[campaign_type]


def infer_audience_rules(brief: str) -> dict:
    text = brief.lower()
    rules = {}

    if "cart value" in text or "$75" in text or "above 75" in text:
        rules["cart_value_min"] = 75

    if "high value" in text or "vip" in text:
        rules["lifetime_value_min"] = 500

    if "inactive" in text or "winback" in text:
        rules["last_purchase_days_ago_min"] = 60

    if "app" in text or "push" in text:
        rules["requires_app_installed_for_push"] = True

    if "sms" in text:
        rules["requires_sms_opt_in"] = True

    if "email" in text:
        rules["requires_email_opt_in"] = True

    return rules


def infer_personalization_fields(brief: str) -> list[str]:
    default_fields = [
        "first_name",
        "favorite_category",
        "cart_value",
        "loyalty_tier",
    ]

    text = brief.lower()

    if "lifetime value" in text or "ltv" in text or "high value" in text:
        default_fields.append("lifetime_value")

    if "last purchase" in text or "inactive" in text:
        default_fields.append("last_purchase_days_ago")

    return default_fields


def parse_brief(raw_brief: str) -> CampaignBrief:
    campaign_type = infer_campaign_type(raw_brief)
    channels = infer_channels(raw_brief)

    return CampaignBrief(
        raw_brief=raw_brief,
        campaign_type=campaign_type,
        goal=infer_goal(campaign_type),
        channels=channels,
        audience_rules=infer_audience_rules(raw_brief),
        personalization_fields=infer_personalization_fields(raw_brief),
    )
