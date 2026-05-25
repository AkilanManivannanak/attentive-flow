
# ⚡ AttentiveFlow

Python FastAPI Streamlit Pydantic Marketing Automation Agentic Workflows Compliance Repair Evaluation JSON Export

🎬 Video Demo  |  📸 Screenshots  |  🐙 GitHub  |  📖 Architecture  |  🧪 Workflow Evaluation

Agentic cross-channel marketing workflow builder — campaign brief parsing, ecommerce audience segmentation, SMS/email/push/RCS message generation, channel eligibility checks, compliance validation, A/B testing plans, campaign scoring, and automated repair loops.

AttentiveFlow converts ambiguous lifecycle marketing requests into structured, testable, customer-safe workflows for ecommerce marketing teams.

Built by Akilan Manivannan

---

## 🎯 System Goal

Goal: Help lifecycle marketers move from a messy campaign idea to a structured, compliant, testable marketing workflow across SMS, email, push, and RCS.

Example marketer request:

```text
Create an abandoned cart campaign for customers with cart value above $75.
Use SMS first, email after 24 hours if they do not click, and push if they have the app installed.
Personalize based on first name, cart value, product category, and loyalty tier.
````

AttentiveFlow produces:

* campaign type and goal
* audience segmentation rules
* channel eligibility counts
* personalized SMS/email/push/RCS messages
* workflow step timing and conditions
* A/B testing plan
* compliance result
* campaign quality scores
* automated repair output
* downloadable workflow JSON

---

## ✅ Current MVP Results

The current demo runs locally with FastAPI + Streamlit and synthetic ecommerce customer data.

| Capability                        | Status        |
| --------------------------------- | ------------- |
| Brief-to-workflow parsing         | ✅ Implemented |
| Audience segmentation             | ✅ Implemented |
| SMS/email/push/RCS workflow steps | ✅ Implemented |
| Channel eligibility checks        | ✅ Implemented |
| Compliance validation             | ✅ Implemented |
| A/B test planning                 | ✅ Implemented |
| Campaign quality scoring          | ✅ Implemented |
| Automated repair loop             | ✅ Implemented |
| Workflow JSON export              | ✅ Implemented |
| Streamlit UI                      | ✅ Implemented |
| FastAPI endpoint                  | ✅ Implemented |
| Public deployment                 | ⏳ Planned     |
| LLM-powered copy generation       | ⏳ Planned     |

Demo repair result:

| Metric                  | Before Repair | After Repair |
| ----------------------- | ------------: | -----------: |
| Compliance passed       |       `false` |       `true` |
| Overall score           |           `8` |         `10` |
| Invalid channel removed |        `push` |            ✅ |

---

## 🎬 Demo

### Local Demo

Run the backend:

```bash
uvicorn backend.main:app --reload
```

Run the frontend in a second terminal:

```bash
streamlit run frontend/app.py
```

Open:

```text
http://localhost:8501
```

### Demo Links

| Asset              | Link                                                                                                         |
| ------------------ | ------------------------------------------------------------------------------------------------------------ |
| Video walkthrough  | Add Loom link here                                                                                           |
| GitHub repo        | [https://github.com/AkilanManivannanak/attentive-flow](https://github.com/AkilanManivannanak/attentive-flow) |
| Screenshots        | Add screenshots below after uploading                                                                        |
| Sample output JSON | `examples/sample_output.json`                                                                                |

---

## 📸 Screenshots

Add screenshots to:

```text
screenshots/executive-summary.png
screenshots/repaired-workflow.png
screenshots/workflow-steps.png
```

Then uncomment these after adding files:

```md
![Executive Summary](screenshots/executive-summary.png)

![Repaired Workflow](screenshots/repaired-workflow.png)

![Workflow Steps](screenshots/workflow-steps.png)
```

---

## 📐 Architecture & Data Flow

```text
Marketing Brief
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit UI                             │
│       campaign input · executive summary · workflow tabs    │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP POST /generate-workflow
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Serving Layer                    │
│       /health · /generate-workflow · typed response models  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  Agentic Workflow Pipeline                  │
│                                                             │
│  ① Brief Parser Agent                                       │
│     messy text → campaign_type, goal, channels, rules       │
│                                                             │
│  ② Segmentation Agent                                       │
│     synthetic customers → eligible audience + counts        │
│                                                             │
│  ③ Message Agent                                            │
│     SMS/email/push/RCS messages with personalization        │
│                                                             │
│  ④ Compliance Agent                                         │
│     opt-in checks, channel checks, STOP language, risk      │
│                                                             │
│  ⑤ Experiment Agent                                         │
│     hypothesis, variants, primary/secondary metrics         │
│                                                             │
│  ⑥ Evaluation Scorer                                        │
│     personalization, clarity, CTA, compliance, channel fit  │
│                                                             │
│  ⑦ Repair Agent                                             │
│     remove invalid steps, fix message issues, rescore       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Compiled Workflow JSON                    │
│       steps · messages · compliance · evaluation · repair   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔁 Workflow Pipeline

Input → Parse → Segment → Generate → Validate → Score → Repair → Export

| Stage      | What happens                                   | Implementation          |
| ---------- | ---------------------------------------------- | ----------------------- |
| Input      | Marketer enters campaign brief                 | Streamlit text area     |
| Parse      | Infer campaign type, channels, audience rules  | `brief_parser.py`       |
| Segment    | Filter synthetic ecommerce customers           | `segmentation_agent.py` |
| Generate   | Create SMS/email/push/RCS message variants     | `message_agent.py`      |
| Validate   | Check opt-ins, channel eligibility, risky copy | `compliance_agent.py`   |
| Experiment | Create A/B test hypothesis and metrics         | `experiment_agent.py`   |
| Score      | Evaluate quality and reliability               | `evals/scoring.py`      |
| Repair     | Remove invalid channel steps and rescore       | `repair_agent.py`       |
| Export     | Compile structured workflow JSON               | `workflows/compiler.py` |

---

## 🤖 Agent Responsibilities

| Agent              | Input                            | Output                               | Current Approach          |
| ------------------ | -------------------------------- | ------------------------------------ | ------------------------- |
| Brief Parser Agent | Raw marketing brief              | Campaign type, goal, channels, rules | Rule-based parser         |
| Segmentation Agent | Campaign rules + customers       | Matching audience + channel counts   | Deterministic filtering   |
| Message Agent      | Campaign brief + sample customer | SMS/email/push/RCS messages          | Template-based generation |
| Compliance Agent   | Messages + customer profile      | Pass/fail + issues                   | Deterministic checks      |
| Experiment Agent   | Campaign type                    | A/B test plan                        | Rule-based strategy       |
| Evaluation Scorer  | Messages + compliance result     | Quality scores 0–10                  | Heuristic scoring         |
| Repair Agent       | Messages + compliance issues     | Safe repaired messages               | Channel removal + fixes   |
| Workflow Compiler  | All intermediate outputs         | Final workflow JSON                  | Typed Pydantic models     |

---

## 🛡️ Compliance & Channel Safety Layer

AttentiveFlow includes a lightweight compliance and eligibility layer.

Checks currently implemented:

| Check                  | Example                                                 |
| ---------------------- | ------------------------------------------------------- |
| SMS opt-out language   | Requires `Reply STOP to opt out.`                       |
| SMS length             | Flags long SMS copy                                     |
| Email subject          | Flags missing subject line                              |
| Push eligibility       | Requires `app_installed=true` and `push_opt_in=true`    |
| RCS eligibility        | Requires `sms_opt_in=true` and `rcs_supported=true`     |
| Risky urgency language | Flags unsupported urgency claims                        |
| Discount dependency    | Flags campaigns where every message relies on discounts |

Example compliance failure:

```json
{
  "passed": false,
  "issues": [
    {
      "severity": "high",
      "issue": "Push message generated for a customer without the app installed.",
      "recommendation": "Only send push notifications to customers with app_installed=true."
    },
    {
      "severity": "high",
      "issue": "Push message generated for a customer who has not opted into push.",
      "recommendation": "Only send push notifications to customers with push_opt_in=true."
    }
  ]
}
```

---

## 🔧 Automated Repair Loop

The repair loop is the key reliability feature.

Initial workflow:

```text
SMS → Email → Push
```

Selected sample customer:

```json
{
  "sms_opt_in": true,
  "email_opt_in": true,
  "push_opt_in": false,
  "app_installed": false
}
```

Problem:

```text
Push is invalid for this customer.
```

Repair:

```text
Remove Push step.
Keep SMS + Email.
Re-run compliance.
Re-score workflow.
```

Result:

```json
{
  "removed_channels": ["push"],
  "before_overall_score": 8,
  "after_overall_score": 10,
  "before_compliance_passed": false,
  "after_compliance_passed": true
}
```

This demonstrates an agentic feedback loop:

```text
Generate → Validate → Detect Issue → Repair → Re-evaluate
```

---

## 🧪 Evaluation Scoring

Every generated campaign is scored across five dimensions:

| Metric          | What it measures                                    |
| --------------- | --------------------------------------------------- |
| Personalization | Number and relevance of customer attributes used    |
| Clarity         | Message readability and channel-appropriate length  |
| CTA             | Whether the message has a clear call to action      |
| Compliance      | Whether compliance checks pass                      |
| Channel Fit     | Whether messages fit SMS/email/push/RCS constraints |

Example evaluation:

```json
{
  "personalization_score": 9,
  "clarity_score": 10,
  "cta_score": 9,
  "compliance_score": 2,
  "channel_fit_score": 10,
  "overall_score": 8,
  "issues": [
    "Push message generated for a customer without the app installed.",
    "Push message generated for a customer who has not opted into push."
  ]
}
```

After repair:

```json
{
  "personalization_score": 9,
  "clarity_score": 10,
  "cta_score": 9,
  "compliance_score": 10,
  "channel_fit_score": 10,
  "overall_score": 10,
  "issues": []
}
```

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone git@github.com:AkilanManivannanak/attentive-flow.git
cd attentive-flow
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate synthetic data

```bash
python3 backend/data/generate_synthetic_data.py
```

### 5. Start the API

```bash
uvicorn backend.main:app --reload
```

API runs at:

```text
http://127.0.0.1:8000
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the UI

In a second terminal:

```bash
streamlit run frontend/app.py
```

UI runs at:

```text
http://localhost:8501
```

---

## 🔌 API Usage

Health check:

```bash
curl http://127.0.0.1:8000/
```

Generate workflow:

```bash
curl -X POST "http://127.0.0.1:8000/generate-workflow" \
  -H "Content-Type: application/json" \
  -d '{
    "brief": "Create an abandoned cart campaign for customers with cart value above $75. Use SMS first, email after 24 hours if they do not click, and push if they have the app installed."
  }'
```

---

## 🧰 Tech Stack & Trade-offs

| Layer       | Technology                        | Rationale                                 |
| ----------- | --------------------------------- | ----------------------------------------- |
| API         | FastAPI                           | Typed, fast local API with automatic docs |
| UI          | Streamlit                         | Fast demo UI for workflow visualization   |
| Data models | Pydantic                          | Structured outputs and validation         |
| Data        | Synthetic JSON ecommerce profiles | No private customer data required         |
| Agents      | Python modules                    | Lightweight, inspectable, easy to extend  |
| Evaluation  | Heuristic scoring                 | Deterministic and explainable             |
| Repair      | Rule-based workflow correction    | Reliable MVP feedback loop                |
| Storage     | Local JSON                        | Simple, zero-infra demo setup             |

Key trade-offs:

* Local-first and simple: optimized for fast iteration.
* Rule-based before LLM: deterministic behavior is easier to debug.
* Synthetic data: avoids privacy concerns while showing realistic ecommerce behavior.
* JSON output: easy to plug into downstream workflow systems later.
* Streamlit UI: fast product demo, not a production frontend.

---

## 📦 Synthetic Ecommerce Data

Each synthetic customer includes:

```json
{
  "user_id": "u_0001",
  "first_name": "Sam",
  "email_opt_in": true,
  "sms_opt_in": true,
  "push_opt_in": false,
  "rcs_supported": false,
  "app_installed": false,
  "loyalty_tier": "silver",
  "cart_value": 163.44,
  "favorite_category": "men's fashion",
  "last_purchase_days_ago": 23,
  "purchase_count": 9,
  "lifetime_value": 1235.03
}
```

Synthetic event types:

```text
product_viewed
cart_abandoned
purchase_completed
browse_abandoned
email_clicked
sms_clicked
push_opened
price_drop
back_in_stock
```

Generate data:

```bash
python3 backend/data/generate_synthetic_data.py
```

Default output:

```text
1000 customers
5000 events
```

---

## 💬 Demo Flow

1. Open Streamlit UI.
2. Select `Abandoned Cart`.
3. Click `Generate Workflow`.
4. Review executive summary:

   * campaign type
   * initial score
   * repaired score
   * matching customers
5. Review repaired workflow preview.
6. Open `Workflow` tab to see initial generated steps.
7. Open `Compliance` tab to see why the initial workflow failed.
8. Open `Repair Loop` tab to see before/after repair.
9. Download workflow JSON.

---

## 🧱 Project Structure

```text
attentive-flow/
├── backend/
│   ├── __init__.py
│   ├── main.py                     # FastAPI entry point
│   ├── schemas.py                  # Pydantic models
│   ├── config.py                   # Paths and environment config
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── brief_parser.py         # Raw brief → structured campaign brief
│   │   ├── segmentation_agent.py   # Audience filtering + channel counts
│   │   ├── message_agent.py        # SMS/email/push/RCS message generation
│   │   ├── compliance_agent.py     # Compliance + eligibility checks
│   │   ├── experiment_agent.py     # A/B test plan generation
│   │   ├── repair_agent.py         # Repair invalid workflow steps
│   │   └── critic_agent.py         # Reserved for future LLM critic
│   ├── data/
│   │   ├── generate_synthetic_data.py
│   │   ├── synthetic_customers.json
│   │   └── synthetic_events.json
│   ├── evals/
│   │   ├── __init__.py
│   │   └── scoring.py              # Campaign quality scoring
│   └── workflows/
│       ├── __init__.py
│       └── compiler.py             # Full workflow orchestration
├── frontend/
│   └── app.py                      # Streamlit UI
├── examples/
│   ├── abandoned_cart_input.txt
│   ├── winback_input.txt
│   ├── product_drop_input.txt
│   ├── sample_output.json
│   └── demo_script.md
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🗺️ Reusable Campaign Playbooks

Current examples:

| Playbook       | Description                                     |
| -------------- | ----------------------------------------------- |
| Abandoned Cart | Recover cart revenue using SMS → email → push   |
| Winback        | Re-engage inactive customers                    |
| Product Drop   | Launch a new collection to high-value customers |

Example files:

```text
examples/abandoned_cart_input.txt
examples/winback_input.txt
examples/product_drop_input.txt
```

---

## 🛠 Development Commands

Compile check:

```bash
python3 -m py_compile \
backend/main.py \
backend/schemas.py \
backend/config.py \
backend/agents/brief_parser.py \
backend/agents/segmentation_agent.py \
backend/agents/message_agent.py \
backend/agents/compliance_agent.py \
backend/agents/experiment_agent.py \
backend/agents/repair_agent.py \
backend/evals/scoring.py \
backend/workflows/compiler.py \
frontend/app.py
```

Regenerate sample output:

```bash
python3 - << 'PY'
from pathlib import Path
from backend.workflows.compiler import compile_workflow

brief_text = """
Create an abandoned cart campaign for customers with cart value above $75.
Use SMS first, email after 24 hours if they do not click, and push if they have the app installed.
Personalize based on first name, cart value, product category, and loyalty tier.
"""

workflow = compile_workflow(brief_text)
Path("examples/sample_output.json").write_text(workflow.model_dump_json(indent=2))
print("Saved examples/sample_output.json")
PY
```

---

## 🔮 Planned Improvements

| Improvement                    | Why it matters                                                  |
| ------------------------------ | --------------------------------------------------------------- |
| LLM-powered message generation | More flexible brand-aware copy                                  |
| Prompt-chain version of agents | Closer to production agent workflows                            |
| Brand voice controls           | Generate messages for luxury, playful, urgent, minimalist tones |
| Simulated campaign performance | Estimate CTR, conversion, recovered revenue                     |
| Public deployment              | Easier for reviewers to test                                    |
| Docker setup                   | One-command reproducible run                                    |
| CI checks                      | Prevent broken commits                                          |
| Screenshot docs                | Stronger GitHub presentation                                    |
| Additional playbooks           | More reusable lifecycle templates                               |

---

## 🧠 System Design Q&A

### “Why use deterministic rules instead of calling an LLM everywhere?”

For the MVP, deterministic logic makes compliance, channel eligibility, and scoring easier to inspect and debug. LLM generation can be added later for richer copy, but safety-critical checks should stay deterministic or have deterministic fallbacks.

### “Where would LLM agents fit?”

LLM agents would improve:

* campaign brief parsing
* brand-aware message generation
* campaign critique
* repair recommendations
* experiment ideation

The current system already has the pipeline structure needed to plug in LLM calls.

### “How would this scale to real customer data?”

The synthetic JSON layer could be replaced with a warehouse or CDP source. Audience rules would compile into SQL or workflow conditions. Channel eligibility would read consent and device state from production customer profiles.

### “How would this integrate with a marketing platform?”

The compiled workflow JSON could be translated into a journey builder format:

```json
{
  "trigger": "cart_abandoned",
  "audience": {...},
  "steps": [...],
  "conditions": [...],
  "metrics": [...]
}
```

That output could be passed to a workflow engine, campaign API, or human review queue.

### “What are the safety constraints?”

Marketing automation must respect:

* channel consent
* opt-out rules
* unsupported urgency claims
* frequency limits
* customer eligibility
* deliverability constraints
* brand trust

AttentiveFlow models a small but important subset of these constraints.

---

## 📌 Current Status

This is an MVP prototype optimized for fast iteration and hiring signal.

Implemented:

* working FastAPI backend
* working Streamlit UI
* synthetic ecommerce dataset
* structured campaign workflow generation
* compliance validation
* evaluation scoring
* automated repair loop
* workflow JSON export
* reusable campaign examples

Not yet implemented:

* public deployment
* Docker
* CI
* Prometheus
* LLM-powered copy generation
* real integrations
* persistent database

---

## Footer

© 2026 Akilan Manivannan — All Rights Reserved

AttentiveFlow · FastAPI · Streamlit · Pydantic · Python · Marketing Automation · Agentic Workflows · Compliance Repair

GitHub: [https://github.com/AkilanManivannanak/attentive-flow](https://github.com/AkilanManivannanak/attentive-flow)
