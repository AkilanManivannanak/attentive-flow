from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Channel(str, Enum):
    sms = "sms"
    email = "email"
    push = "push"
    rcs = "rcs"


class CampaignType(str, Enum):
    abandoned_cart = "abandoned_cart"
    browse_abandonment = "browse_abandonment"
    winback = "winback"
    product_drop = "product_drop"
    loyalty_reward = "loyalty_reward"


class Customer(BaseModel):
    user_id: str
    first_name: str
    email: str
    email_opt_in: bool
    sms_opt_in: bool
    push_opt_in: bool
    rcs_supported: bool
    app_installed: bool
    loyalty_tier: str
    cart_value: float
    favorite_category: str
    last_purchase_days_ago: int
    purchase_count: int
    lifetime_value: float


class CampaignBrief(BaseModel):
    raw_brief: str
    campaign_type: CampaignType
    goal: str
    channels: List[Channel]
    audience_rules: Dict[str, Any] = Field(default_factory=dict)
    personalization_fields: List[str] = Field(default_factory=list)


class MessageVariant(BaseModel):
    channel: Channel
    subject: Optional[str] = None
    body: str
    cta: Optional[str] = None
    personalization_used: List[str] = Field(default_factory=list)


class WorkflowStep(BaseModel):
    step_id: str
    channel: Channel
    delay: str
    condition: Optional[str] = None
    message: MessageVariant
    success_metric: str


class ExperimentPlan(BaseModel):
    hypothesis: str
    variant_a: str
    variant_b: str
    primary_metric: str
    secondary_metrics: List[str] = Field(default_factory=list)


class ComplianceIssue(BaseModel):
    severity: str
    issue: str
    recommendation: str


class ComplianceResult(BaseModel):
    passed: bool
    issues: List[ComplianceIssue] = Field(default_factory=list)


class EvaluationScores(BaseModel):
    personalization_score: int = Field(ge=0, le=10)
    clarity_score: int = Field(ge=0, le=10)
    cta_score: int = Field(ge=0, le=10)
    compliance_score: int = Field(ge=0, le=10)
    channel_fit_score: int = Field(ge=0, le=10)
    overall_score: int = Field(ge=0, le=10)
    issues: List[str] = Field(default_factory=list)


class MarketingWorkflow(BaseModel):
    campaign_brief: CampaignBrief
    audience_summary: str
    steps: List[WorkflowStep]
    experiment_plan: ExperimentPlan
    compliance: ComplianceResult
    evaluation: EvaluationScores
    workflow_json: Dict[str, Any] = Field(default_factory=dict)


class WorkflowRequest(BaseModel):
    brief: str


class WorkflowResponse(BaseModel):
    workflow: MarketingWorkflow
