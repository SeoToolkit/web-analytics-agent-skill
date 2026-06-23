#!/usr/bin/env python3
"""
Bing Webmaster API — 获取搜索分析数据
=======================================
API 端点: https://ssl.bing.com/webmaster/api.svc/json/
认证方式: API Key (URL query param)
前提: 目标网站已在 Bing Webmaster Tools 中验证

⚠️ 关键经验:
- 端点名是 GetQueryStats / GetPageStats / GetKeywordStats
- 不要用 GetSiteList / SearchAnalytics (那是错的!)
- API key 通过 URL query param 传入 ?apikey=KEY
- siteUrl 也需要 URL 编码
"""

import requests, json, os, sys
from datetime import datetime, timedelta
from urllib.parse import quote
from collections import defaultdict

# ═══════════════════════════════════════
# 配置
# ═══════════════════════════════════════
API_KEY = os.environ.get("BING_API_KEY")
BASE_URL = "https://ssl.bing.com/webmaster/api.svc/json/"
SITE_URL = os.environ.get("BING_SITE_URL", "https://example.com")

if not API_KEY or API_KEY == "your_bing_api_key_here":
    print("\n❌ Error: Valid BING_API_KEY not found.")
    print("\n👉 How to get Bing API Key (Beginner's Guide):")
    print("  1. Visit Bing Webmaster Tools (https://www.bing.com/webmasters/) and log in.")
    print("  2. Ensure your website is verified in the dashboard.")
    print("  3. Click the Gear icon (Settings) in the top right -> 'API Access'.")
    print("  4. Select the 'API Key' tab, then click 'Generate API Key'.")
    print("  5. Copy the generated long string.")
    print("  6. Copy '.env.example' to '.env' in the project root,")
    print("     and paste the key after 'BING_API_KEY='.")
    print("\nOnce done, re-run the script to fetch data!\n")
    exit(1)

def bing_get(endpoint, params=None):
    """统一的 Bing API GET 请求"""
    if params is None:
        params = {}
    params['apikey'] = API_KEY
    query_string = '&'.join(f'{k}={quote(str(v), safe="")}' for k, v in params.items())
    url = f"{BASE_URL}{endpoint}?{query_string}"
    
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get('d', [])


def fetch_queries():
    """Fetch Query Stats"""
    print(f"\n{'='*60}")
    print(f"Bing Query Stats — {SITE_URL}")
    print(f"{'='*60}")
    
    data = bing_get("GetQueryStats", {'siteUrl': SITE_URL})
    
    kw_agg = defaultdict(lambda: {'c': 0, 'i': 0})
    for row in data:
        kw_agg[row['Query']]['c'] += row['Clicks']
        kw_agg[row['Query']]['i'] += row['Impressions']
    
    print(f"Unique Queries: {len(kw_agg)}")
    for kw, d in sorted(kw_agg.items(), key=lambda x: -x[1]['i'])[:20]:
        print(f"  {kw[:55]:<55} C:{d['c']:>4} I:{d['i']:>6}")
    
    return data


def fetch_pages():
    """Fetch Page Stats"""
    print(f"\n{'='*60}")
    print(f"Bing Page Stats — {SITE_URL}")
    print(f"{'='*60}")
    
    data = bing_get("GetPageStats", {'siteUrl': SITE_URL})
    
    pg_agg = defaultdict(lambda: {'c': 0, 'i': 0})
    for row in data:
        url = row['Query']  # GetPageStats 中 Query 字段是页面 URL
        pg_agg[url]['c'] += row['Clicks']
        pg_agg[url]['i'] += row['Impressions']
    
    total_c = sum(d['c'] for d in pg_agg.values())
    total_i = sum(d['i'] for d in pg_agg.values())
    print(f"Total Clicks: {total_c}  Total Impressions: {total_i}")
    for url, d in sorted(pg_agg.items(), key=lambda x: -x[1]['i'])[:15]:
        short = url.replace(SITE_URL, '')
        print(f"  {short:<50} C:{d['c']:>5} I:{d['i']:>6}")
    
    return data


def fetch_keyword_research(term="free llm api"):
    """Fetch Keyword Stats"""
    print(f"\n{'='*60}")
    print(f"Bing Keyword Research — '{term}'")
    print(f"{'='*60}")
    
    data = bing_get("GetKeywordStats", {
        'country': 'us',
        'language': 'en-US',
        'q': term
    })
    
    if not data:
        print(f"  No data available")
        return data
    
    # 去重取最新月均值
    latest = {}
    for row in data:
        q = row['Query']
        latest[q] = row
    
    for q, row in latest.items():
        broad = row.get('BroadImpressions', 0)
        exact = row.get('Impressions', 0)
        print(f"  {q:<40} Broad:{broad:>6}  Exact:{exact:>6}")
    
    return data


def get_overall_summary():
    """Bing Overall Traffic Summary"""
    print(f"\n{'='*60}")
    print(f"Bing Overall Traffic Summary")
    print(f"{'='*60}")
    
    # Bing data
    pages = bing_get("GetPageStats", {'siteUrl': SITE_URL})
    bing_total_c = sum(r['Clicks'] for r in pages)
    bing_total_i = sum(r['Impressions'] for r in pages)
    
    print(f"""
  Bing Overall: Clicks {bing_total_c:>5}  Impressions {bing_total_i:>6}
  (Tip: Agent can compare these numbers with GSC output for engine ratio analysis)
""")
    
    return {
        'bing_clicks': bing_total_c,
        'bing_impressions': bing_total_i
    }


if __name__ == "__main__":
    fetch_queries()
    fetch_pages()
    # 如果需要查询特定关键词的搜索量，可以取消下方注释并修改占位符
    # fetch_keyword_research("your keyword here")
    get_overall_summary()
