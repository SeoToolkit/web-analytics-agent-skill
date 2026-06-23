"""GA4 data via requests"""
import json, requests
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

import os
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

def get_ga4_headers():
    token_path = 'google_analytics_token.json'
    client_secret = os.environ.get('GOOGLE_ANALYTICS_OAUTH_CONFIG_PATH', 'client_secret.json')
    creds = None
    
    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path)
        except Exception:
            pass

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("  (refreshing GA4 token...)")
            creds.refresh(Request())
            print("  (token refreshed)")
        else:
            print("  (No valid GA4 token found. Opening browser for authorization...)")
            if not os.path.exists(client_secret):
                print(f"\n❌ Error: Credential file '{client_secret}' not found.")
                print("\n👉 How to get client_secret.json (Beginner's Guide):")
                print("  1. Visit Google Cloud Console (https://console.cloud.google.com/)")
                print("  2. Create a new project, search for and enable the following APIs:")
                print("     - Google Analytics Data API")
                print("     - Google Search Console API")
                print("  3. Go to 'APIs & Services' -> 'OAuth consent screen' and configure it (choose External, add yourself as test user).")
                print("  4. Go to 'Credentials' -> '+ Create Credentials' -> 'OAuth client ID'.")
                print("  5. Choose 'Desktop app' as Application type, enter a name, and click Create.")
                print("  6. After creation, click the 'Download JSON' button on the popup.")
                print("  7. Rename the downloaded file to 'client_secret.json' and place it in the root directory of this project.")
                print("\nOnce done, re-run the script to authorize automatically!\n")
                exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret, 
                ['https://www.googleapis.com/auth/analytics.readonly']
            )
            creds = flow.run_local_server(port=0)
            
        with open(token_path, 'w') as f:
            f.write(creds.to_json())
            
    return {'Authorization': f'Bearer {creds.token}', 'Content-Type': 'application/json'}

def ga4_report(property_id, start_date, end_date, metrics, dimensions=None, limit=100):
    headers = get_ga4_headers()
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport"
    payload = {
        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
        'metrics': [{'name': m} for m in metrics],
        'limit': limit
    }
    if dimensions:
        payload['dimensions'] = [{'name': d} for d in dimensions]
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()

end_d = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
start_d = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
d14 = (datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d')

props_env = os.environ.get("GA4_PROPERTIES", "")
if not props_env:
    print("Error: GA4_PROPERTIES is not set in .env")
    exit(1)

try:
    properties = [[item.strip() for item in p.split("=")] for p in props_env.split(",")]
except ValueError:
    print("❌ 环境变量 GA4_PROPERTIES 格式错误！正确格式为：PropertyID=Label (例如: 123456789=MySite)")
    exit(1)

for pid, label in properties:
    print(f"\n{'='*60}\n  GA4 - {label} (property: {pid})\n{'='*60}")
    try:
        # 30-day summary
        s = ga4_report(pid, start_d, end_d, ["sessions", "totalUsers", "screenPageViews", "bounceRate", "averageSessionDuration", "engagedSessions"])
        if s.get('rows'):
            mv = s['rows'][0].get('metricValues', [])
            labels = ['Sessions','Users','PV','BounceRate','AvgSessionDur','EngagedSessions']
            print(f"  30-day summary:")
            for lb, m in zip(labels, mv):
                v = float(m['value'])
                if 'Rate' in lb.lower() or 'Bounce' in lb: print(f"    {lb}: {v*100:.1f}%")
                elif 'Dur' in lb: print(f"    {lb}: {v:.1f}s")
                else: print(f"    {lb}: {v:,.0f}")
        else:
            print(f"  No summary data")

        # Daily trend (14 days)
        daily = ga4_report(pid, d14, end_d, ["sessions", "screenPageViews", "totalUsers"], ["date"], 20)
        print(f"  Daily trend (14d):")
        for row in sorted(daily.get('rows', []), key=lambda x: x['dimensionValues'][0]['value']):
            d = row['dimensionValues'][0]['value']
            v = [float(x['value']) for x in row['metricValues']]
            print(f"    {d}: Sess {v[0]:>7,.0f} | PV {v[1]:>7,.0f} | Users {v[2]:>5,.0f}")

        # Traffic sources
        ts = ga4_report(pid, start_d, end_d, ["sessions", "totalUsers"], ["sessionSourceMedium"], 10)
        print(f"  Top traffic sources:")
        for i, row in enumerate(ts.get('rows', [])[:10], 1):
            src = row['dimensionValues'][0]['value']
            v = [float(x['value']) for x in row['metricValues']]
            print(f"    {i:>2}. {src:<45} Sess:{v[0]:>7,.0f} Users:{v[1]:>5,.0f}")

        # Countries
        co = ga4_report(pid, start_d, end_d, ["sessions", "totalUsers"], ["country"], 10)
        print(f"  Top countries:")
        for i, row in enumerate(co.get('rows', [])[:10], 1):
            c = row['dimensionValues'][0]['value']
            v = [float(x['value']) for x in row['metricValues']]
            print(f"    {i:>2}. {c:<30} Sess:{v[0]:>7,.0f} Users:{v[1]:>5,.0f}")

        # Top pages
        tp = ga4_report(pid, start_d, end_d, ["screenPageViews", "sessions"], ["pagePath"], 15)
        print(f"  Top pages:")
        for i, row in enumerate(tp.get('rows', [])[:15], 1):
            p = row['dimensionValues'][0]['value']
            v = [float(x['value']) for x in row['metricValues']]
            print(f"    {i:>2}. {p:<45} PV:{v[0]:>7,.0f} Sess:{v[1]:>5,.0f}")

    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback; traceback.print_exc()

print(f"\n{'='*60}\n  GA4 Report Complete")
