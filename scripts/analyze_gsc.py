#!/usr/bin/env python3
import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

TOKEN_FILE = 'token.json'
SITE_URL = os.environ.get('GSC_SITE_URL', 'sc-domain:example.com')

import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

def get_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE)
        except Exception:
            pass

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("  (refreshing GSC token...)")
            creds.refresh(Request())
            print("  (token refreshed)")
        else:
            print("  (No valid GSC token found. Opening browser for authorization...)")
            if not os.path.exists('client_secret.json'):
                print("\n❌ Error: Credential file 'client_secret.json' not found.")
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
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', 
                ['https://www.googleapis.com/auth/webmasters.readonly']
            )
            creds = flow.run_local_server(port=0)
            
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            
    return build('searchconsole', 'v1', credentials=creds)

def query_gsc(service, start_date, end_date, dimensions, row_limit=50):
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': dimensions,
        'rowLimit': row_limit
    }
    response = service.searchanalytics().query(siteUrl=SITE_URL, body=request).execute()
    return response.get('rows', [])

def get_latest_date(service):
    # GSC 有数据延迟，查询过去 7 天的按日数据，找出最后一天有数据的日期
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    rows = query_gsc(service, start_date, end_date, ['date'])
    if rows:
        dates = [row['keys'][0] for row in rows]
        dates.sort()
        return datetime.strptime(dates[-1], '%Y-%m-%d')
    # 默认回退 3 天
    return datetime.now() - timedelta(days=3)

def analyze_period(service, title, start_date, end_date):
    print(f"\n[{title}] ({start_date} to {end_date})")
    
    # Overall
    overall = query_gsc(service, start_date, end_date, [])
    if overall:
        row = overall[0]
        clicks = row.get('clicks', 0)
        impr = row.get('impressions', 0)
        ctr = row.get('ctr', 0)
        pos = row.get('position', 0)
        print(f"  📈 Overall: Impressions {impr} | Clicks {clicks} | CTR {ctr:.2%} | Avg Position {pos:.1f}")
    else:
        print("  No data available")
        return

    # Top Queries
    queries = query_gsc(service, start_date, end_date, ['query'], 3)
    if queries:
        print("  🔥 Top 3 Queries:")
        for q in queries:
            print(f"    - {q['keys'][0]}: Impressions {q['impressions']} | Clicks {q['clicks']} (Position {q['position']:.1f})")

def main():
    service = get_service()
    
    # 找到最近一天有数据的日期
    latest_date_obj = get_latest_date(service)
    latest_date_str = latest_date_obj.strftime('%Y-%m-%d')
    
    # 网站上线时间
    launch_date_str = os.environ.get('SITE_LAUNCH_DATE', '2024-01-01')
    launch_date_obj = datetime.strptime(launch_date_str, '%Y-%m-%d')
    
    print(f"=== Traffic Growth Trend Analysis ===")
    print(f"Latest available GSC data date: {latest_date_str}")
    
    # 1. Since Launch
    analyze_period(service, "Since Launch", launch_date_str, latest_date_str)
    
    # 2. Last 7 Days
    start_7 = (latest_date_obj - timedelta(days=6)).strftime('%Y-%m-%d')
    if start_7 < launch_date_str: start_7 = launch_date_str
    analyze_period(service, "Last 7 Days", start_7, latest_date_str)
    
    # 3. Latest 1 Day
    analyze_period(service, "Latest 1 Day", latest_date_str, latest_date_str)

if __name__ == '__main__':
    main()
