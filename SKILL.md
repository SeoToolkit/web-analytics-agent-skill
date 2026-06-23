---
name: web-analytics
description: Analyze web traffic, SEO performance, and search engine trends using Google Search Console, Google Analytics 4, and Bing Webmaster Tools. Use when the user asks to analyze traffic, check SEO, or find keyword opportunities.
---

# Web Analytics Skill

This skill allows the agent to pull and analyze traffic data from Google and Bing to provide deep SEO insights.

## Environment Preparation

The necessary scripts are located in the `scripts/` directory relative to this `SKILL.md` file.
Ensure the following dependencies are installed:
```bash
python3 -m pip install -r scripts/gsc-requirements.txt
```

### Credentials Required & How to Obtain Them
Before executing this skill, ensure the environment is configured. If the user does not have the required credentials, the Agent should instruct the user to obtain them using the following steps:

#### 1. Google OAuth Client Secret (`client_secret.json`)
The agent requires a Desktop OAuth 2.0 Client ID to access Google APIs.
**Instructions for the User:**
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Navigate to **APIs & Services > Library** and enable **Google Search Console API** and **Google Analytics Data API**.
4. Navigate to **APIs & Services > OAuth consent screen** and configure it (you can set user type to "External" and add your own email as a test user).
5. Navigate to **APIs & Services > Credentials**. Click **Create Credentials > OAuth client ID**.
6. Select **Desktop app** as the application type.
7. Click Create, then download the JSON file. Rename it to `client_secret.json` and place it in the `scripts/` directory of this skill.

#### 2. Google OAuth Tokens (`token.json`, `google_analytics_token.json`)
These are generated automatically by the script. 
- *Agent Instruction:* If the script output says `Opening browser for authorization`, tell the user to check their computer for a newly opened browser window and complete the Google OAuth login. The script will automatically save the tokens locally once login is successful.

#### 3. Bing API Key
**Instructions for the User:**
1. Go to [Bing Webmaster Tools](https://www.bing.com/webmasters/).
2. Select your verified website.
3. Click on the **Settings** gear icon in the top right corner.
4. Go to **API Access** -> **API Key**.
5. Click **Generate API Key** (or copy the existing one).
6. Paste it into the `.env` file as `BING_API_KEY=your_key_here`.

## Execution Steps

### 1. Gather Google Search Console (GSC) Data
Run the GSC analysis script to get clicks, impressions, CTR, and average position:
```bash
cd scripts && python3 analyze_gsc.py
```

### 2. Gather Google Analytics 4 (GA4) Data
Run the GA4 script to analyze user sessions, traffic sources, and pageviews:
```bash
cd scripts && python3 ga4_both.py
```

### 3. Gather Bing Webmaster Tools Data
Run the Bing script to compare Bing search performance against Google:
```bash
export BING_API_KEY=$(grep BING_API_KEY ../../.env | cut -d '=' -f2)
cd scripts && python3 bing_webmaster.py
```

### 4. Synthesize Insights
Analyze the combined output and report:
1. **Trend Analysis**: Is overall traffic growing or dropping based on the 14-day view?
2. **Platform Ratio**: What is the proportion of Bing traffic compared to Google?
3. **Keyword & Page Opportunities**: Highlight keywords with high impressions but low CTR, or pages performing well on Bing but not Google.

Provide the final summary to the user using clean Markdown.
