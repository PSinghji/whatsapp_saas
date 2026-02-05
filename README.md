# WhatsApp Messaging SaaS Platform

## Overview
This project aims to design and generate a production-grade WhatsApp Messaging SaaS Platform. The platform is built using Python with FastAPI for the backend, MongoDB as the primary database, and supports multi-language WhatsApp Web automation. It includes comprehensive modules for user management, billing, messaging campaigns, API management, and more, designed for deployment on a standard Linux server without Docker.

## Features added by Psingh

### Core Architecture
- **Backend Language**: Python 3.10+
- **Web Framework**: FastAPI (REST + WebSocket)
- **Authentication**: JWT + Role-based access control
- **Async Queue**: Celery / Redis (conceptual integration)
- **Real-time Updates**: WebSockets
- **Background Jobs**: Async workers

### Database (MongoDB)
- Collections for users, devices, messages, campaigns, etc.
- Indexes for performance optimization.
- Schema validation using Pydantic.
- DataTables-compatible APIs for pagination, search, and sorting.

### WhatsApp Web Integration
- Multi-language bridges for automation (Python, Node.js).
- QR-based authentication.
- Session persistence and multi-device support.
- Auto-reconnect, ban, and health monitoring.

### Dynamic Message System
- Variable placeholders (e.g., `{{name}}`, `{{order_id}}`).
- Conditional content, media + text, emoji support.
- Retry logic and delivery tracking.

### Complete Module List
- **Dashboard**: Total Users, Active Devices, Messages Sent, Revenue, Credits Used, Server Health, Queue Status.
- **User Management**: Add/Edit/Delete/Suspend User, Login Logs, Role Assignment, Reset Password, Message/Device Limits, KYC.
- **Credit & Wallet**: Add/Deduct Credits, Credit History, Wallet Balance, Auto Credit Rules, Refunds, Credit Expiry, Cost Per Message.
- **Subscription Management**: Create/Edit Plans, Assign Plan, Validity, Pause/Renew, Upgrade/Downgrade, Feature Mapping.
- **Device & QR Management**: Add Device, Generate QR, Reconnect QR, Force Logout, Device Status/Health, Ban Monitor, Session Expiry, IP Lock.
- **Messaging Control**: Global Rate Limit, Retry Rules, Spam Detection, Template Approval, Media Size Limit, Keyword Blocking, Auto Throttling.
- **API Management**: API Key Generator, Token Reset, Usage Limits, IP Whitelisting, API/Error Logs, API Docs, Enable/Disable API per User.
- **Campaign System**: Campaign Approval, Bulk Campaign Monitor, Stop Campaign, Queue Manager, Speed Controller, Duplicate/Blacklist Filter.
- **Reports & Analytics**: User-wise/Device-wise Usage, Delivery Reports, Success/Failure Ratio, Credit Consumption, Revenue/Subscription/API Usage Reports.
- **Billing & Payments**: Payment Gateway Config, Manual Approval, Invoice Generation, GST Settings, Wallet Recharge, Coupons, Payment History, Failed Payments.
- **Support System**: Ticket Management, Live Chat, Categories, Priority, SLA, Ticket Assignment.
- **Security & Compliance**: IP Blocking, Geo Blocking, OTP Login, 2FA, Device Fingerprinting, Message Encryption, GDPR Settings, Consent Logs.
- **System Settings**: Branding, SMTP, SMS Gateway, Webhooks, Retry Timer, Queue Size, File Storage.
- **Logs & Monitoring**: Login Logs, API Logs, Message Logs, Error Logs, Webhook Logs, QR Scan Logs.

### Navigation-Based Chatbot
- Built-in chatbot for dashboard navigation.
- Supports menu-driven interaction.
- Assists users with campaign creation, credit balance, API usage, device status, and error explanations.
- Uses rule-based + optional AI intent matching.

## Getting Started

### Prerequisites
- Ubuntu 20.04+ server
- Python 3.10+
- MongoDB
- Redis

### Installation
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-repo/whatsapp_saas.git
    cd whatsapp_saas
    ```

2.  **Run the deployment script**:
    ```bash
    chmod +x scripts/deploy.sh
    ./scripts/deploy.sh
    ```
    This script will:
    - Update system packages.
    - Install Python, pip, MongoDB, and Redis.
    - Install Python dependencies from `requirements.txt`.

3.  **Manual Setup (if not using deploy.sh)**:
    - Install Python 3.10+, pip, MongoDB, and Redis manually.
    - Install Python dependencies:
        ```bash
        pip install -r requirements.txt
        ```

### Configuration
Edit `app/core/config.py` to set your `SECRET_KEY`, MongoDB URL, and Redis URL.

```python
# app/core/config.py
class Settings(BaseSettings):
    PROJECT_NAME: str = "WhatsApp SaaS Platform"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY"  # **CHANGE THIS IN PRODUCTION**
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "whatsapp_saas"

    REDIS_URL: str = "redis://localhost:6379/0"
```

### Running the Application
To run the FastAPI application (for development/testing):

```bash
cd /home/ubuntu/whatsapp_saas
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

For production, it is recommended to use a WSGI server like Gunicorn with a process manager (e.g., systemd, supervisor) and a reverse proxy (e.g., Nginx).

### Running Celery Workers
In a separate terminal, from the project root directory:

```bash
celery -A app.worker.celery_app worker --loglevel=info
```

## API Documentation
Once the application is running, you can access the interactive API documentation (Swagger UI) at `http://localhost:8000/docs`.

## WhatsApp Bridge Setup (Node.js Example)
To use the Node.js WhatsApp bridge:

1.  **Install Node.js dependencies**:
    ```bash
    cd bridges/nodejs
    npm install
    ```

2.  **Run the Node.js bridge** (e.g., for a specific session):
    ```bash
    node index.js <session_id>
    ```
    This will print a QR code to the console (or a mechanism to send it back to the Python backend in a full implementation). You would then scan this QR code with your WhatsApp mobile app to link the device.

## Project Structure
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
│   │   │   ├── api_mgmt.py
│   │   │   ├── subscriptions.py
│   │   │   ├── billing.py
│   │   │   ├── support.py
│   │   │   └── monitoring.py
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
│   │   │   └── python_bridge.py
│   │   ├── billing.py
│   │   ├── campaign_mgr.py
│   │   ├── chatbot.py
│   │   └── ...
│   ├── main.py             # Entry point
│   └── worker.py           # Background worker
├── bridges/                # Multi-language connectors
│   ├── nodejs/
│   │   ├── package.json
│   │   └── index.js
│   ├── go/                 # Placeholder
│   └── dotnet/             # Placeholder
├── scripts/                # Deployment & Utility scripts
│   └── deploy.sh
├── requirements.txt
└── README.md
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries, please contact [your-email@example.com].
