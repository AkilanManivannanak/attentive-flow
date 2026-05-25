
<div align="center">

# ⚡ AttentiveFlow

<img src="https://readme-typing-svg.demolab.com?font=Inter&weight=700&size=28&pause=1000&center=true&vCenter=true&width=900&lines=Agentic+Marketing+Workflow+Builder;SMS+%E2%86%92+Email+%E2%86%92+Push+%E2%86%92+RCS+Automation;Compliance+Validation+%2B+Repair+Loop;LLM-Powered+Copy+Generation+with+Safe+Fallback" alt="Typing SVG" />

<br />

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Live_Demo-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-Typed_Models-E92063?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/OpenAI-Optional_LLM_Copy-412991?style=for-the-badge&logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Deployed-success?style=for-the-badge)

<br />

### Agentic cross-channel lifecycle marketing automation  
**Brief → Audience → Messages → Compliance → Scoring → Repair → Workflow JSON**

<br />

[🚀 Live Demo](https://attentive-flow-4gl3ne52akjjjy3eyl6cun.streamlit.app)
&nbsp;•&nbsp;
[🐙 GitHub](https://github.com/AkilanManivannanak/attentive-flow)
&nbsp;•&nbsp;
[📦 Sample Output](examples/sample_output.json)
&nbsp;•&nbsp;
[🎬 Demo Script](examples/demo_script.md)

<br />

Built by **Akilan Manivannan**

</div>

---

## 🧠 What Is AttentiveFlow?

**AttentiveFlow** is an agentic marketing workflow builder for ecommerce lifecycle campaigns.

It takes an ambiguous marketer request like:

```text
Create an abandoned cart campaign for customers with cart value above $75.
Use SMS first, email after 24 hours if they do not click, and push if they have the app installed.
Personalize based on first name, cart value, product category, and loyalty tier.
````

and turns it into a structured workflow containing:

* audience segmentation rules
* channel eligibility counts
* SMS, email, push, and RCS message variants
* A/B test plan
* compliance validation
* campaign quality scoring
* automated repair loop
* downloadable workflow JSON

The core idea is simple:

> Lifecycle marketers should be able to move from campaign idea to compliant, testable workflow faster — without manually reasoning through every audience rule, consent constraint, channel condition, and message variant.

---

## 🎯 System Goal

Goal: **help lifecycle marketing teams generate structured, compliant, testable cross-channel workflows from messy campaign briefs.**

AttentiveFlow is designed around problems that marketing automation teams actually face:

| Problem                                      | AttentiveFlow Response                                           |
| -------------------------------------------- | ---------------------------------------------------------------- |
| Campaign briefs are ambiguous                | Parse them into structured campaign objects                      |
| Customers have different channel permissions | Check SMS, email, push, and RCS eligibility                      |
| Marketing copy can violate rules             | Run compliance checks                                            |
| Generated workflows may contain unsafe steps | Repair invalid workflow steps                                    |
| Campaign quality is subjective               | Score personalization, CTA, clarity, compliance, and channel fit |
| Teams need portable outputs                  | Export workflow JSON                                             |

---

## ✅ Current Deployed Capabilities

| Capability                               | Status        |
| ---------------------------------------- | ------------- |
| Public Streamlit deployment              | ✅ Live        |
| Brief-to-workflow parsing                | ✅ Implemented |
| Synthetic ecommerce customer data        | ✅ Implemented |
| Audience segmentation                    | ✅ Implemented |
| SMS/email/push/RCS workflow steps        | ✅ Implemented |
| Optional LLM-powered copy generation     | ✅ Implemented |
| Template fallback when no API key exists | ✅ Implemented |
| Channel eligibility checks               | ✅ Implemented |
| Compliance validation                    | ✅ Implemented |
| A/B test planning                        | ✅ Implemented |
| Campaign quality scoring                 | ✅ Implemented |
| Automated repair loop                    | ✅ Implemented |
| Workflow JSON export                     | ✅ Implemented |
| FastAPI backend                          | ✅ Implemented |
| Streamlit UI                             | ✅ Implemented |

---

## 🚀 Live Demo

<div align="center">

### [Launch AttentiveFlow](https://attentive-flow-4gl3ne52akjjjy3eyl6cun.streamlit.app)

</div>

The deployed app runs directly on Streamlit Cloud and calls the workflow engine in-process.
It no longer depends on a local `localhost:8000` FastAPI server for the public demo.

Message generation mode:

| Mode                              | Behavior                                        |
| --------------------------------- | ----------------------------------------------- |
| `USE_LLM_COPY=true` + OpenAI key  | Uses OpenAI for channel-specific marketing copy |
| No API key / `USE_LLM_COPY=false` | Falls back to deterministic templates           |
| LLM returns invalid JSON          | Falls back to templates automatically           |

---

## 📸 Screenshots

Add your screenshots to:

```text
screenshots/executive-summary.png
screenshots/repaired-workflow.png
screenshots/workflow-steps.png
screenshots/repair-loop.png
```

Then uncomment:

```md
![Executive Summary](screenshots/executive-summary.png)

![Repaired Workflow](screenshots/repaired-workflow.png)

![Workflow Steps](screenshots/workflow-steps.png)

![Repair Loop](screenshots/repair-loop.png)
```

---

## 🧬 Core Demo Result

The demo intentionally shows a realistic failure and repair case.

### Initial workflow

```text
SMS → Email → Push
```

### Sample customer

```json
{
  "sms_opt_in": true,
  "email_opt_in": true,
  "push_opt_in": false,
  "app_installed": false
}
```

### Problem

The workflow includes a push notification, but the selected customer:

* does not have the app installed
* has not opted into push notifications

### Repair

The repair agent removes the invalid push step and keeps the safe workflow:

```text
SMS → Email
```

### Result

| Metric                  | Before Repair | After Repair |
| ----------------------- | ------------: | -----------: |
| Compliance passed       |       `false` |       `true` |
| Overall score           |           `8` |         `10` |
| Invalid channel removed |        `push` |            ✅ |

```json
{
  "removed_channels": ["push"],
  "before_overall_score": 8,
  "after_overall_score": 10,
  "before_compliance_passed": false,
  "after_compliance_passed": true
}
```

This is the key agentic loop:

```text
Generate → Validate → Detect Issue → Repair → Re-evaluate
```

---

## 📐 Architecture

```text
Marketing Brief
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                       Streamlit UI                          │
│  campaign input · executive summary · workflow tabs · JSON  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Workflow Compiler                        │
│  orchestrates parser, segmentation, messages, eval, repair  │
└──────────────────────────┬──────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────────┐
│ Brief Parser   │ │ Segmentation   │ │ Message Generator  │
│ Agent          │ │ Agent          │ │ LLM or Template    │
└───────┬────────┘ └───────┬────────┘ └─────────┬──────────┘
        │                  │                    │
        ▼                  ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                 Compliance + Evaluation Layer               │
│  channel consent · STOP language · risky copy · scoring     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                       Repair Agent                          │
│  removes invalid channel steps · fixes SMS opt-out issues   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Compiled Workflow JSON                    │
│  audience · steps · messages · tests · compliance · scores  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔁 Workflow Pipeline

| Stage      | What Happens                                       | Implementation          |
| ---------- | -------------------------------------------------- | ----------------------- |
| Input      | Marketer enters campaign brief                     | Streamlit               |
| Parse      | Infer campaign type, goal, channels, and rules     | `brief_parser.py`       |
| Segment    | Filter synthetic ecommerce customers               | `segmentation_agent.py` |
| Generate   | Produce SMS/email/push/RCS messages                | `message_agent.py`      |
| Validate   | Check opt-ins, channel eligibility, and copy risks | `compliance_agent.py`   |
| Experiment | Create A/B test plan and metrics                   | `experiment_agent.py`   |
| Score      | Evaluate quality across five dimensions            | `evals/scoring.py`      |
| Repair     | Remove invalid steps and fix message issues        | `repair_agent.py`       |
| Export     | Compile structured workflow JSON                   | `workflows/compiler.py` |

---

## 🤖 Multi-Agent System

| Agent              | Input                      | Output                             | Fallback Behavior       |
| ------------------ | -------------------------- | ---------------------------------- | ----------------------- |
| Brief Parser Agent | Raw campaign brief         | Structured campaign brief          | Rule-based parser       |
| Segmentation Agent | Campaign rules + customers | Matching audience + channel counts | Deterministic filtering |
| Message Agent      | Campaign + customer        | SMS/email/push/RCS messages        | Template fallback       |
| Compliance Agent   | Messages + customer        | Pass/fail + issues                 | Deterministic rules     |
| Experiment Agent   | Campaign type              | A/B test plan                      | Rule-based strategy     |
| Evaluation Scorer  | Messages + compliance      | Quality scores 0–10                | Heuristic scoring       |
| Repair Agent       | Messages + issues          | Repaired safe workflow             | Channel removal + fixes |
| Workflow Compiler  | All intermediate outputs   | Final workflow JSON                | Typed Pydantic models   |

---

## 🧠 LLM-Powered Copy Generation

AttentiveFlow supports optional LLM-powered copy generation.

If an OpenAI API key is configured, the message agent asks the model to generate channel-specific marketing copy as JSON.

If the key is missing, disabled, or the model returns invalid JSON, the system falls back to deterministic templates.

```text
LLM available?
   │
   ├── yes → Generate JSON messages with OpenAI
   │          │
   │          ├── valid JSON → use LLM messages
   │          └── invalid JSON → fallback templates
   │
   └── no  → use deterministic templates
```

Why this matters:

* richer brand-aware message generation
* safer deterministic fallback
* no hard dependency on external APIs
* deployment works even without an API key

Configuration:

```env
OPENAI_API_KEY=
MODEL_NAME=gpt-4o-mini
USE_LLM_COPY=true
```

---

## 🛡️ Compliance & Channel Safety Layer

Marketing automation cannot ignore consent and channel rules.

AttentiveFlow checks:

| Check                  | Example                                                 |
| ---------------------- | ------------------------------------------------------- |
| SMS opt-out language   | Requires `Reply STOP to opt out.`                       |
| SMS length             | Flags overly long SMS copy                              |
| Email subject          | Flags missing subject line                              |
| Push eligibility       | Requires `app_installed=true` and `push_opt_in=true`    |
| RCS eligibility        | Requires `sms_opt_in=true` and `rcs_supported=true`     |
| Risky urgency language | Flags unsupported claims like `only 1 left`             |
| Discount dependency    | Flags campaigns where every message relies on discounts |

Example compliance issue:

```json
{
  "severity": "high",
  "issue": "Push message generated for a customer without the app installed.",
  "recommendation": "Only send push notifications to customers with app_installed=true."
}
```

---

## 🧪 Campaign Evaluation

Each generated campaign is scored across five dimensions:

| Metric          | What It Measures                                 |
| --------------- | ------------------------------------------------ |
| Personalization | Use of customer-specific fields                  |
| Clarity         | Message readability and length                   |
| CTA             | Strength and presence of call to action          |
| Compliance      | Whether safety checks pass                       |
| Channel Fit     | Whether copy fits SMS/email/push/RCS constraints |

Example initial score:

```json
{
  "personalization_score": 9,
  "clarity_score": 10,
  "cta_score": 9,
  "compliance_score": 2,
  "channel_fit_score": 10,
  "overall_score": 8
}
```

Example repaired score:

```json
{
  "personalization_score": 9,
  "clarity_score": 10,
  "cta_score": 9,
  "compliance_score": 10,
  "channel_fit_score": 10,
  "overall_score": 10
}
```

---

## 🧰 Tech Stack & Trade-offs

| Layer             | Technology               | Rationale                                   |
| ----------------- | ------------------------ | ------------------------------------------- |
| UI                | Streamlit                | Fast public demo and workflow visualization |
| Public Deployment | Streamlit Cloud          | Simple GitHub-based deployment              |
| API               | FastAPI                  | Local API + Swagger docs                    |
| Models            | Pydantic                 | Typed structured workflow objects           |
| LLM Copy          | OpenAI optional          | Richer message generation                   |
| Fallback Copy     | Python templates         | Reliable no-key execution                   |
| Data              | Synthetic ecommerce JSON | No private customer data                    |
| Evaluation        | Heuristic scoring        | Explainable and deterministic               |
| Repair            | Rule-based correction    | Reliable safety improvement                 |
| Export            | JSON                     | Portable workflow representation            |

Key decisions:

* **Local-first, cloud-ready**: works locally and on Streamlit Cloud.
* **LLM optional**: no API key required to demo.
* **Deterministic safety path**: compliance and repair logic do not depend on an LLM.
* **Synthetic data**: realistic enough for demo, no privacy risk.
* **JSON workflow output**: easy to adapt to a journey builder or campaign API.

---

## 📦 Synthetic Ecommerce Dataset

Each generated customer includes:

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

Default generation:

```text
1000 customers
5000 events
```

---

## 🚀 Quick Start

### Option 1 — Public Demo

Open:

```text
https://attentive-flow-4gl3ne52akjjjy3eyl6cun.streamlit.app
```

---

### Option 2 — Local Streamlit

```bash
git clone git@github.com:AkilanManivannanak/attentive-flow.git
cd attentive-flow

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python3 backend/data/generate_synthetic_data.py

streamlit run frontend/app.py
```

UI:

```text
http://localhost:8501
```

---

### Option 3 — Local FastAPI

```bash
uvicorn backend.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
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

## 🗺️ Reusable Campaign Playbooks

| Playbook       | Description                                        |
| -------------- | -------------------------------------------------- |
| Abandoned Cart | Recover abandoned cart revenue with SMS/email/push |
| Winback        | Re-engage inactive customers                       |
| Product Drop   | Launch a new collection to high-value customers    |

Example files:

```text
examples/abandoned_cart_input.txt
examples/winback_input.txt
examples/product_drop_input.txt
```

---

## 💬 Demo Flow

1. Open the live Streamlit app.
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
│   ├── main.py                     # FastAPI entry point
│   ├── schemas.py                  # Pydantic data models
│   ├── config.py                   # Env + Streamlit secrets support
│   ├── agents/
│   │   ├── brief_parser.py         # Brief → campaign object
│   │   ├── segmentation_agent.py   # Audience filtering
│   │   ├── message_agent.py        # LLM/template message generation
│   │   ├── compliance_agent.py     # Compliance checks
│   │   ├── experiment_agent.py     # A/B test planning
│   │   ├── repair_agent.py         # Automated repair loop
│   │   └── critic_agent.py         # Reserved for future critic agent
│   ├── data/
│   │   ├── generate_synthetic_data.py
│   │   ├── synthetic_customers.json
│   │   └── synthetic_events.json
│   ├── evals/
│   │   └── scoring.py              # Campaign quality scoring
│   └── workflows/
│       └── compiler.py             # End-to-end orchestration
├── frontend/
│   └── app.py                      # Streamlit public UI
├── examples/
│   ├── abandoned_cart_input.txt
│   ├── winback_input.txt
│   ├── product_drop_input.txt
│   ├── sample_output.json
│   └── demo_script.md
├── .streamlit/
│   └── config.toml
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
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

## 🔮 Roadmap

| Improvement                    | Why It Matters                                                |
| ------------------------------ | ------------------------------------------------------------- |
| Brand voice controls           | Generate luxury, playful, urgent, minimalist, or premium tone |
| Simulated campaign performance | Estimate CTR, conversion, recovered revenue                   |
| Frequency capping              | Avoid over-messaging customers                                |
| Real CDP integration           | Replace synthetic JSON with customer profile source           |
| Workflow builder export        | Convert JSON into journey-builder-ready format                |
| CI checks                      | Prevent broken commits                                        |
| Docker support                 | One-command reproducible local run                            |
| Screenshot docs                | Stronger GitHub presentation                                  |
| More lifecycle playbooks       | Welcome series, back-in-stock, loyalty rewards, replenishment |

---

## 🧠 System Design Q&A

### Why not call an LLM for everything?

Because compliance and channel eligibility should be deterministic. LLMs are useful for creative copy, but opt-in logic, app-install checks, and repair rules must be predictable.

### What happens if OpenAI is unavailable?

The message agent falls back to deterministic templates. The demo still works.

### How would this scale to real customer data?

The synthetic JSON dataset could be replaced with a CDP, warehouse, or customer profile API. Audience rules could compile into SQL or workflow-engine conditions.

### How would this integrate with a real marketing platform?

The workflow JSON could become an intermediate representation for a journey builder:

```json
{
  "trigger": "cart_abandoned",
  "audience": {
    "cart_value_min": 75
  },
  "steps": [
    {
      "channel": "sms",
      "delay": "1 hour",
      "condition": "sms_opt_in=true"
    }
  ]
}
```

### What makes this agentic?

The system is not just one generation call. It chains specialized modules:

```text
Brief Parser → Segmentation → Message Generation → Compliance → Evaluation → Repair
```

The repair step closes the loop by taking evaluation/compliance failures and producing a safer workflow.

---

## 📌 Current Status

Implemented:

* deployed Streamlit app
* optional OpenAI message generation
* deterministic template fallback
* FastAPI backend
* Streamlit frontend
* synthetic ecommerce customer/event data
* structured campaign workflow generation
* compliance validation
* campaign scoring
* automated repair loop
* workflow JSON export
* reusable campaign examples

Not yet implemented:

* real customer data integration
* persistent database
* Docker
* CI
* Prometheus metrics
* production authentication
* full campaign performance simulator

---

## Footer

© 2026 Akilan Manivannan — All Rights Reserved

**AttentiveFlow** · FastAPI · Streamlit · Pydantic · OpenAI · Python · Marketing Automation · Agentic Workflows · Compliance Repair

GitHub: [https://github.com/AkilanManivannanak/attentive-flow](https://github.com/AkilanManivannanak/attentive-flow)

Live Demo: [https://attentive-flow-4gl3ne52akjjjy3eyl6cun.streamlit.app](https://attentive-flow-4gl3ne52akjjjy3eyl6cun.streamlit.app)
