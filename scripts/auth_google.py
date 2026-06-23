#!/usr/bin/env python3
"""
Standalone script to get and refresh Google OAuth 2.0 tokens for GSC and GA4.
"""

import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/webmasters.readonly',
    'https://www.googleapis.com/auth/analytics.readonly'
]
CLIENT_SECRET_FILE = 'client_secret.json'
TOKEN_FILE = 'token.json'

def main():
    print("=== Google APIs OAuth 2.0 Token Setup ===")
    
    if not os.path.exists(CLIENT_SECRET_FILE):
        print(f"\n❌ Error: Credential file '{CLIENT_SECRET_FILE}' not found.")
        print("\n👉 How to get client_secret.json (Beginner's Guide):")
        print("  1. Visit Google Cloud Console (https://console.cloud.google.com/)")
        print("  2. Create a new project, search for and enable the following APIs:")
        print("     - Google Search Console API")
        print("     - Google Analytics Data API")
        print("  3. Go to 'APIs & Services' -> 'OAuth consent screen' and configure it (choose External, add yourself as test user).")
        print("  4. Go to 'Credentials' -> '+ Create Credentials' -> 'OAuth client ID'.")
        print("  5. Choose 'Desktop app' as Application type, enter a name, and click Create.")
        print("  6. After creation, click the 'Download JSON' button on the popup.")
        print("  7. Rename the downloaded file to 'client_secret.json' and place it in the root directory of this project.")
        print("\nOnce done, re-run the script to authorize automatically!\n")
        exit(1)

    creds = None
    if os.path.exists(TOKEN_FILE):
        print(f"📄 Found existing '{TOKEN_FILE}'. Validating...")
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception as e:
            print(f"⚠️ Warning: Could not read '{TOKEN_FILE}' correctly. Might be an old version. Re-authenticating...")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Token expired. Refreshing...")
            try:
                creds.refresh(Request())
                print("✅ Token refreshed successfully!")
            except Exception as e:
                print(f"⚠️ Refresh failed: {e}. Re-authenticating...")
                creds = None

        if not creds:
            print("🌐 Opening browser to request authorization (GSC & GA4)...")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            print("✅ Authorization successful!")
            
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            print(f"💾 Token saved to '{TOKEN_FILE}'.")
            
        # Copy token.json to google_analytics_token.json to ensure compatibility 
        # with ga4 scripts
        with open('google_analytics_token.json', 'w') as token_copy:
            token_copy.write(creds.to_json())
            print(f"💾 Token also copied to 'google_analytics_token.json'.")
    else:
        print("✅ Token is valid and ready to use.")

    print("\n🎉 Token generation and verification complete! You can now run the analysis scripts.")

if __name__ == '__main__':
    main()
