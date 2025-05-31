# 🔥📜 Burn Note
A one-time secret sharing tool

## 🔐 Getting Started

### Running With Docker
To spin up the entire stack using Docker, run:
```
make start-docker
```

### Running Locally
Alternatively, you can spin up the backend and frontend locally.

#### Backend (FastAPI)
From the root of the project:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the FastAPI server:
```
make start-api
```
By default, it runs on http://localhost:8000.

#### Frontend (ViteJS)
From the root folder, run:
```
cd web && npm install
```

Start the Vite dev server:
```
make start-web
```

The app will be available at http://localhost:5173.

## 🗂️ Overview

This tool encrypts your secret message in the browser and creates a URL for sharing once. The secret is deleted when it is viewed or expired (in 24 hours).

> ⚠️ **Note:** This is a prototype. It should be vetted by a security professional to ensure it is in fact a secure way of sharing secrets before using.

## 🧱 How It Works

### Client-Side Encryption

When a secret message is submitted through the form, a random encryption key is generated and used to encrypt the message using the AES-GCM algorithm. The encrypted message is stored to a PostgreSQL database, keyed by a unique token. This token is used to create a shareable URL, while the encryption key is embedded in the URL as a `#fragment`.

The URL fragment is never sent to the server -- it remains entirely on the client side. When someone opens the shared link, the frontend extracts the key from the `#fragment`, sends the token to the server, and receives the encrypted message. The frontend then decrypts the message using the key in the browser.

Once the message is viewed, it is immediately deleted from the database, making the link accessible only once.

## 🔮 Future Work

- A cron job to delete unread and expired messages
- Improve styling