# WhatsApp Messaging SaaS Platform Design

## 1. System Architecture
The platform is built as a modular FastAPI application with a MongoDB backend. It uses a multi-language bridge for WhatsApp automation.

### Components:
- **FastAPI Backend**: Core logic, API endpoints, and authentication.
- **MongoDB**: Primary database for users, devices, messages, and logs.
- **Async Workers**: Background tasks for message sending and campaign management.
- **WhatsApp Bridges**:
    - **Python Bridge**: Playwright-based automation.
    - **Node.js Bridge**: `whatsapp-web.js` integration.
    - **Go/ .NET Bridges**: Optional connectors for specific performance needs.

## 2. Directory Structure
```text
whatsapp_saas/
├── app/
│   ├── api/                # API Routes
│   │   ├── v1/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── devices.py
│   │   │   ├── messages.py
│   │   │   ├── campaigns.py
│   │   │   └── ...
│   ├── core/               # Core configurations
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── models/             # Pydantic & MongoDB Schemas
│   │   ├── user.py
│   │   ├── device.py
│   │   ├── message.py
│   │   └── ...
│   ├── services/           # Business Logic
│   │   ├── whatsapp/       # WhatsApp Bridges
│   │   ├── billing.py
│   │   ├── campaign_mgr.py
│   │   └── ...
│   ├── main.py             # Entry point
│   └── worker.py           # Background worker
├── bridges/                # Multi-language connectors
│   ├── nodejs/
│   ├── go/
│   └── dotnet/
├── scripts/                # Deployment & Utility scripts
├── requirements.txt
└── README.md
```

## 3. Database Schema (MongoDB Collections)
- `users`: User profiles, roles, credits, subscription info.
- `devices`: WhatsApp device sessions, status, health.
- `messages`: Message logs, status (sent, failed, pending), delivery reports.
- `campaigns`: Campaign metadata, schedule, progress.
- `credits_history`: Transaction logs for wallet.
- `subscriptions`: Plan details and user assignments.
- `tickets`: Support tickets and chat history.
- `logs`: System, API, and security logs.

## 4. Key Features
- **QR Authentication**: Real-time QR generation and session persistence.
- **Dynamic Messaging**: Placeholder support (e.g., `{{name}}`).
- **Rate Limiting**: Global and user-level throttling to prevent bans.
- **Navigation Chatbot**: Rule-based bot for dashboard assistance.
