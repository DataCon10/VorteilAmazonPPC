# Amazon Advertising API PPC Automation

This repository contains the initial code for automating interactions with the Amazon Advertising API. The current implementation includes:

- **Token Management:**  
  A script to obtain a new access token using a refresh token (with support for OAuth 2.0).
  
- **Profile & Campaign Data Retrieval:**  
  Functions to fetch your advertising profiles and to retrieve campaign data using the correct region-specific endpoints and headers (including the UK profile).

- **Centralized Configuration:**  
  A `config.py` file that centralizes environment-specific configuration (endpoints, credentials, marketplace selection) for easy management and reuse across scripts.

## Prerequisites

1. **Amazon Developer / Advertising Account:**  
   - Register your application in the [Amazon Developer Console](https://developer.amazon.com/).
   - Set up Login with Amazon (LWA) for your app.
   - Configure your LWA app with a redirect URI (e.g., `http://localhost:5000/callback`).

2. **Environment Setup:**
   - Python 3.7+ installed.
   - [pip](https://pip.pypa.io/en/stable/) for package installation.


