# 🔮 CyberHoroscope

> **Your Daily Security Fate — Laugh First, Learn to Protect Yourself Second**

CyberHoroscope is a gamified cybersecurity awareness tool disguised as a daily horoscope. Answer 5 quick questions about your online habits, and a serverless Lambda function scores your responses and delivers a personalised horoscope — complete with a Cyber Sign, dimension scores, prophecies, and a roast message if you truly deserve one. The user laughs. Then they learn something. That's the whole trick.

---

## Architecture

```
[Browser]
    │  HTTPS
    ▼
[Amazon CloudFront]  ──serves static assets──  [S3 Bucket]
    │
    │  POST /horoscope   GET /health
    ▼
[Amazon API Gateway — HTTP API]
    │
    ▼
[AWS Lambda — Python 3.12 / arm64 / 128 MB]
    │  Pure in-memory scoring, no DB calls
    ▼
[JSON Response → Browser]
```

**Stack:** AWS SAM · Lambda (Python 3.12, Graviton2) · API Gateway HTTP API · S3 · CloudFront  
**Cost:** $0.00 — entirely within AWS Free Tier at hackathon scale.

---

## Prerequisites

| Tool | Install |
|---|---|
| AWS CLI v2 | [docs.aws.amazon.com/cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) |
| AWS SAM CLI | `pip install aws-sam-cli` |
| Python 3.12 | [python.org](https://www.python.org/downloads/) |
| jq | `brew install jq` / `apt install jq` |

---

## Quick Start

```bash
# 1. Build the Lambda package
sam build

# 2. First-time deploy (guided — sets region, stack name, saves config)
sam deploy --guided
#   stack_name: cyber-horoscope
#   region:     ap-south-1
#   confirm_changeset: Y

# 3. Upload the frontend (injects API URL, uploads to S3, invalidates CloudFront)
chmod +x scripts/deploy_frontend.sh
./scripts/deploy_frontend.sh
```

Your live URL is printed at the end. Open it. Select all the worst answers. Show the judges.

---

## Running Tests Locally

```bash
cd cyber-horoscope
pip install pytest
pytest tests/ -v
```

---

## How Scoring Works

Users answer 5 questions. Each answer carries a risk score. Scores are summed, normalised to 0–100, and mapped to a Cyber Sign:

| Score | Cyber Sign | Emoji | Vibe |
|---|---|---|---|
| 0 – 20 | Firewall Phoenix | 🦅 | Untouchable |
| 21 – 40 | Encryption Wizard | 🧙 | Pretty solid |
| 41 – 60 | Patch Warrior | ⚔️ | Getting there |
| 61 – 80 | Phishing Magnet | 🧲 | Concerning |
| 81 – 100 | Data Breach Influencer | 📢 | Call your bank |

Scores ≥ 70 also trigger a **Roast Message** — a special note from the cybersecurity gods.

---

## Project Structure

```
cyber-horoscope/
├── template.yaml              # SAM infrastructure (Lambda, API GW, S3, CloudFront)
├── samconfig.toml             # SAM deploy config
├── src/
│   ├── handler.py             # Lambda entry point (routing, CORS, error handling)
│   ├── horoscope_engine.py    # Scoring + horoscope generation logic
│   ├── content.py             # All prophecy / roast / charm strings
│   └── validator.py           # Input validation
├── tests/
│   └── test_horoscope_engine.py  # pytest suite
├── frontend/
│   └── index.html             # Single-file SPA (dark mystical UI, no frameworks)
├── scripts/
│   └── deploy_frontend.sh     # S3 upload + CloudFront invalidation helper
└── README.md
```

---

## Demo Tips (for Hackathon Judges)

1. **The worst path is the best demo.** Select all the "bad" answers — one password for everything, no 2FA, never update — and hit Reveal. The roast message alone gets a laugh every time.
2. **Show the score counter animation.** Watch the number tick up to 100. Let it land.
3. **Read one prophecy aloud.** The Cinzel font makes them sound genuinely ominous.
4. **Mention the Lucky Security Charm.** It's always a real, actionable tip. That's the learning moment.
5. **Show the architecture diagram.** 3 AWS services, 0 databases, $0 cost. Judges love it.

---

## Cost Estimate

| Service | Free Tier | Expected Usage | Cost |
|---|---|---|---|
| Lambda | 1M req/mo + 400K GB-s | < 10,000 requests | $0.00 |
| API Gateway | 1M HTTP calls/mo (12 mo) | < 10,000 calls | $0.00 |
| S3 | 5 GB storage, 20K GET | 1 file | $0.00 |
| CloudFront | 1 TB transfer, 10M req/mo | Minimal | $0.00 |
| **Total** | | | **$0.00** |

---

*Built for hackathon. No user data stored. No external API calls. Pure serverless Python comedy.*
