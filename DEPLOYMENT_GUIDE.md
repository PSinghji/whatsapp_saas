# Comprehensive CI/CD Guide for WhatsApp SaaS Platform

This guide provides a step-by-step process to establish a robust Continuous Integration/Continuous Deployment (CI/CD) pipeline for your WhatsApp SaaS Platform. You will learn how to manage your project locally on your MacBook, push changes to a GitHub repository, and automatically deploy those changes to your production Linux server.

## 1. Local Development Environment Setup (MacBook)

This section guides you through setting up your project on your local MacBook, initializing a Git repository, and making your first commit to GitHub.

### 1.1 Install Git
If you don't already have Git installed on your MacBook, you can install it using Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install git
```

### 1.2 Prepare Your Project Directory
Assuming your project files are in a directory (e.g., `whatsapp_saas`) on your MacBook, navigate into it.

```bash
cd /path/to/your/whatsapp_saas
```

### 1.3 Initialize Local Git Repository
Initialize a new Git repository in your project directory. If you received a zip file from me, it already contains a `.gitignore` file and the `.github/workflows/deploy.yml` file. If not, you will need to create them (refer to the previous output for their content).

```bash
git init
git add .
git commit -m "Initial project commit"
```

### 1.4 Create a GitHub Repository
1.  Go to [GitHub](https://github.com/) and log in to your account.
2.  Click the `+` sign in the top right corner and select `New repository`.
3.  Give your repository a name (e.g., `whatsapp_saas`), choose whether it's public or private, and **do not initialize it with a README, .gitignore, or license** (as you already have these locally).
4.  Click `Create repository`.

### 1.5 Link Local Repository to GitHub
After creating the repository on GitHub, you will be given instructions to link your local repository. It will look something like this:

```bash
git branch -M main
git remote add origin https://github.com/your_github_username/whatsapp_saas.git # Use the HTTPS URL provided by GitHub
git push -u origin main
```

Replace `your_github_username/whatsapp_saas.git` with the actual URL of your GitHub repository. After executing these commands, your local project will be pushed to GitHub.

## 2. Production Server Setup

This section details how to prepare your Linux production server for automated deployments.

### 2.1 Server Prerequisites
Ensure your server has the necessary software installed. You can use the provided `scripts/deploy.sh` (which is part of your project) or install them manually.

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3.10 python3-pip git mongodb redis-server

# Start and enable services
sudo systemctl start mongodb
sudo systemctl enable mongodb
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### 2.2 Create Project Directory and Set Permissions
Create the directory where your application will reside and ensure the deployment user has appropriate permissions. Replace `ubuntu` with your actual deployment username if different.

```bash
sudo mkdir -p /var/www/whatsapp_saas
sudo chown -R ubuntu:ubuntu /var/www/whatsapp_saas
```

### 2.3 Initial Clone of Repository on Server
Perform an initial clone of your GitHub repository to the server. This sets up the `.git` directory and initial files.

```bash
cd /var/www/whatsapp_saas
git clone https://github.com/your_github_username/whatsapp_saas.git .
```

### 2.4 Install Python Dependencies on Server
Install the Python dependencies required by your project.

```bash
cd /var/www/whatsapp_saas
pip install -r requirements.txt
```

### 2.5 Configure Gunicorn and Systemd Service (Recommended for Production)
For robust production deployment, run your FastAPI application using Gunicorn and manage it with `systemd`. This ensures automatic restarts and proper process management.

1.  **Install Gunicorn**:
    ```bash
    pip install gunicorn
    ```

2.  **Create a Gunicorn start script** (e.g., `/var/www/whatsapp_saas/start_gunicorn.sh`):
    ```bash
    #!/bin/bash
    cd /var/www/whatsapp_saas
    # Ensure the virtual environment is activated if you are using one
    # source /path/to/your/venv/bin/activate
    /usr/bin/python3 -m gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
    ```
    Make it executable:
    ```bash
    chmod +x /var/www/whatsapp_saas/start_gunicorn.sh
    ```

3.  **Create a systemd service file** (e.g., `/etc/systemd/system/whatsapp_saas.service`):
    ```ini
    [Unit]
    Description=WhatsApp SaaS FastAPI Application
    After=network.target

    [Service]
    User=ubuntu # Your deployment user
    Group=ubuntu # Your deployment user
    WorkingDirectory=/var/www/whatsapp_saas
    ExecStart=/var/www/whatsapp_saas/start_gunicorn.sh
    Restart=always
    RestartSec=10
    StandardOutput=syslog
    StandardError=syslog
    SyslogIdentifier=whatsapp_saas

    [Install]
    WantedBy=multi-user.target
    ```

4.  **Enable and start the service**:
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start whatsapp_saas.service
    sudo systemctl enable whatsapp_saas.service
    ```

5.  **Check service status**:
    ```bash
    sudo systemctl status whatsapp_saas.service
    ```

## 3. GitHub Actions for Automated Deployment

This section explains how to configure GitHub Actions to automatically deploy your code to the production server upon every push to the `main` branch.

### 3.1 Generate SSH Key Pair for GitHub Actions
**Do not use your personal SSH key.** Generate a new SSH key pair specifically for GitHub Actions to access your server. This should be done on your local machine or a secure environment.

```bash
ssh-keygen -t rsa -b 4096 -C "github-actions-deploy-key"
```
When prompted, save the key to a file (e.g., `~/.ssh/github-actions-deploy-key`). **Do not set a passphrase.**

### 3.2 Add Public Key to Your Server
Copy the content of `~/.ssh/github-actions-deploy-key.pub` (the public key) to your server's `~/.ssh/authorized_keys` file for the user that GitHub Actions will log in as (e.g., `ubuntu`).

```bash
cat ~/.ssh/github-actions-deploy-key.pub | ssh ubuntu@your_server_ip "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```
Replace `ubuntu@your_server_ip` with your actual server user and IP address.

### 3.3 Configure GitHub Secrets
GitHub Actions needs secure access to your server. You will store sensitive information as GitHub Secrets.

1.  Go to your GitHub repository on the web.
2.  Navigate to `Settings` > `Secrets and variables` > `Actions`.
3.  Click `New repository secret`.
4.  Create the following secrets:
    -   `SSH_HOST`: Your server's IP address or hostname (e.g., `your_server_ip`).
    -   `SSH_USERNAME`: The username on your server (e.g., `ubuntu`).
    -   `SSH_PRIVATE_KEY`: The **entire content** of your private SSH key file (`~/.ssh/github-actions-deploy-key`), including the `-----BEGIN OPENSSH PRIVATE KEY-----` and `-----END OPENSSH PRIVATE KEY-----` lines.

### 3.4 GitHub Actions Workflow File (`.github/workflows/deploy.yml`)

This file, already provided in your project, defines the automated deployment process. Ensure it's present in your GitHub repository.

```yaml
name: Deploy to Production

on: 
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install dependencies (for workflow runner, optional)
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SSH_HOST }}
        username: ${{ secrets.SSH_USERNAME }}
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        script: |
          cd /var/www/whatsapp_saas
          git pull origin main
          pip install -r requirements.txt # Re-install dependencies in case they changed
          sudo systemctl restart whatsapp_saas.service # Restart your application service
```

**Important**: Notice the `sudo systemctl restart whatsapp_saas.service` command. This assumes you have set up the `systemd` service as described in Section 2.5. This is the correct way to restart your application in a production environment.

## 4. Final Steps and Workflow

Now that everything is configured, here's your development and deployment workflow:

1.  **Develop Locally**: Make changes to your project files on your MacBook.

2.  **Commit Changes**: Save your changes and commit them to your local Git repository.
    ```bash
    git add .
    git commit -m "Your descriptive commit message"
    ```

3.  **Push to GitHub**: Push your committed changes to your `main` branch on GitHub.
    ```bash
    git push origin main
    ```

4.  **Automated Deployment**: GitHub Actions will automatically detect the push to `main`, trigger the `deploy.yml` workflow, and execute the deployment script on your production server. This will pull the latest code, update dependencies, and restart your FastAPI application.

5.  **Monitor Deployment**: Go to your GitHub repository, click on the `Actions` tab, and monitor the `Deploy to Production` workflow run. You can see the logs and ensure the deployment was successful.

By following this workflow, any changes you make locally and push to GitHub will be automatically deployed to your production server, streamlining your development process.
