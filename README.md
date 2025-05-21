# 🔥📜 Burn Note
A one-time secret sharing tool

## 🔐 Getting Started

```
make migrate
make start
```

## 🗂️ Overview

This tool encrypts your secret message in the browser and creates a URL for sharing once. The secret is deleted when it is viewed or expired (in 24 hours).

> ⚠️ **Note:** This is a prototype. It should be vetted by a security professional to ensure it is in fact a secure way of sharing secrets before using.

## 🧱 How It Works
### Client-Side Encryption
When a secret message is submitted through the form, a random encryption key is generated and used to encrypt the message using the AES algorithm. The encrypted message is stored to a SQLite database, keyed by a unique token. This token is used to create a shareable URL, while the encryption key is embedded in the URL as a `#fragment`.

The URL fragment is never sent to the server -- it remains entirely on the client side. When someone opens the shared link, the frontend extracts the key from the `#fragment`, sends the token to the server, and receives the encrypted message. The frontend then decrypts the message using the key in the browser.

Once the message is viewed, it is immediately deleted from the database, making the link accessible only once.

## 📚 Learnings

This tool was built in Django as a way for me to experiment with the framework. Django's feature rich framework wasn't strictly necessary for this project. Future improvements might include building a standalone JavaScript frontend for better testability and reusability since encryption is done on the frontend. Additionally, a more robust database such as PostgreSQL might be used.