# Web Analytics Agent Skill

<p align="center">
  <img src="https://www.gstatic.com/images/branding/product/1x/search_console_64dp.png" alt="Google Search Console" height="24" /> <strong>Google Search Console</strong><br><br>
  <img src="https://www.gstatic.com/analytics-suite/header/suite/v2/ic_analytics.svg" alt="Google Analytics" height="24" /> <strong>Google Analytics 4</strong><br><br>
  <img src="https://upload.wikimedia.org/wikipedia/commons/e/e9/Bing_logo.svg" alt="Bing Webmaster Tools" height="24" /> <strong>Bing Webmaster</strong>
</p>

[English](./README.md) | [简体中文](./README.zh-CN.md) | [繁體中文](./README.zh-TW.md) | [日本語](./README.ja.md)


A powerful **Agent Skill** and **Python Automation Tool** designed to provide a 360-degree view of your website's search performance. By seamlessly integrating the APIs of **Google Search Console (GSC)**, **Google Analytics 4 (GA4)**, and **Bing Webmaster Tools**, this project empowers your AI Agents (or CI/CD pipelines) to autonomously perform deep **SEO automation**, **traffic diagnosis**, and **cross-platform keyword research**.

**Keywords**: `seo-agent`, `ai-seo`, `web-analytics`, `ga4`, `google-analytics`, `google-search-console`, `agent-skill`, `mcp-server`

## 📥 How to Install (Installation)
For most mainstream AI Agents (such as Cursor, Cline, Claude Code, Antigravity, etc.), the simplest and recommended way is to **directly share this repository URL with the AI** and let it autonomously read and mount this skill.

**You can simply copy and paste this prompt to your AI assistant:**
> "Please read and install this AI Agent Skill: https://github.com/SeoToolkit/web-analytics-agent-skill . Read the `SKILL.md` file carefully to understand how to use it."

Alternatively, if your AI assistant supports reading skills directly from the workspace, simply clone it into your project:
```bash
git clone https://github.com/SeoToolkit/web-analytics-agent-skill.git .skills/web-analytics-agent-skill
```

## 📊 Example Reports

| Google Search Console | Google Analytics 4 | Bing Webmaster Tools |
| :---: | :---: | :---: |
| <img src="./assets/demo1.png" alt="Google Search Console Report"> | <img src="./assets/demo2.png" alt="Google Analytics 4 Report"> | <img src="./assets/demo3.png" alt="Bing Webmaster Tools Report"> |

## 🛠️ Features
- **Google Search Console**: Fetch indexing and keyword ranking data, clicks, and impressions.
- **Google Analytics 4 (GA4)**: Track actual user sessions, bounce rates, and traffic sources.
- **Bing Webmaster Tools**: Pull search stats directly from Bing for cross-engine comparison.

## 📦 Prerequisites & Environment
1. Clone the repository, create a virtual environment, and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and proceed to configure the channels you need.

### Channel 1: Bing Webmaster Tools
- **Auth Method**: API Key (Manual)
- **Setup Steps**:
  1. Go to [Bing Webmaster Tools](https://www.bing.com/webmasters/).
  2. Click the Gear icon (Settings) -> API Access -> API Key.
  3. Generate and copy the API key.
- **Environment Variables** (`.env`):
  - `BING_API_KEY`: Your copied API Key.
  - `BING_SITE_URL`: Your Bing verified domain (e.g., `https://example.com`).

### Channel 2: Google Search Console (GSC)
- **Auth Method**: OAuth 2.0 (Manual `client_secret.json` + Auto Browser Prompt)
- **Setup Steps**:
  1. Go to [Google Cloud Console](https://console.cloud.google.com/) and create a project.
  2. Search for and enable the **Google Search Console API**.
  3. Configure the "OAuth consent screen" (External type, add your email as a test user).
  4. Go to "Credentials" -> "+ Create Credentials" -> "OAuth client ID".
  5. Select "Desktop app", create it, and click download JSON.
  6. Rename it to `client_secret.json` and place it in the project root directory.
  7. *(Automated)* The script will pop up a browser for you to log in on its first run.
  > **💡 Important Note on Permissions**: Make sure the Google account you log in with has read access to your GSC and GA4 properties. You must check the boxes to grant access to Search Console and Analytics data during the popup. If you get a 403 error later, the AI agent will usually catch it and remind you to check your permissions.
- **Environment Variables** (`.env`):
  - `GSC_SITE_URL`: Your exact GSC property URL (e.g., `sc-domain:example.com` or `https://example.com/`).
  - `SITE_LAUNCH_DATE`: (Optional) Your website's launch date for metrics (Format: `YYYY-MM-DD`).

### Channel 3: Google Analytics 4 (GA4)
- **Auth Method**: OAuth 2.0 (Uses the same `client_secret.json` + Auto Browser Prompt)
- **Setup Steps**:
  1. In the same Google Cloud project, search for and enable the **Google Analytics Data API**.
  2. Ensure your `client_secret.json` is in the project root.
  3. *(Automated)* The script will pop up a browser for you to log in on its first run.
- **Environment Variables** (`.env`):
  - `GA4_PROPERTIES`: Your GA4 property ID and label (Format: `PropertyID=Label`, e.g., `123456789=MyWebsite`).

## 📄 Configuration File Examples

Here are the required formats for the files you need to prepare:

### 1. `.env`
Create this file in the project root:
```ini
# Bing Webmaster Tools
BING_API_KEY=your_bing_api_key_here
BING_SITE_URL=https://yourdomain.com

# Google Search Console
GSC_SITE_URL=sc-domain:yourdomain.com
SITE_LAUNCH_DATE=2024-01-01

# Google Analytics 4
GA4_PROPERTIES=123456789=yourdomain.com
```

### 2. `client_secret.json`
This is the file downloaded directly from Google Cloud Console. It should look like this (do not change its structure):
```json
{
  "installed": {
    "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": ["http://localhost"]
  }
}
```

## 🚀 Usage / Agent Instructions
Instruct your AI agent to run the unified execution script. This script automatically handles virtual environment setup, dependencies, and runs all analysis tools sequentially:
```bash
./run_all.sh
```
Or you can run individual scripts manually:
- `scripts/auth_google.py`: A dedicated script to handle Google OAuth 2.0 authorization. Running this explicitly generates the `token.json` file. *(Note: Other scripts will automatically call this flow if the token is missing, so running this manually is optional).*
- `scripts/analyze_gsc.py`: Fetches Google Search Console data.
- `scripts/ga4_both.py`: Fetches Google Analytics 4 data.
- `scripts/bing_webmaster.py`: Fetches Bing Webmaster Tools data.

```bash
source .venv/bin/activate
python3 scripts/auth_google.py
```

## 🤖 Supported AI Agents
Because this skill is built as a standard CLI tool outputting structured text, it is supported out-of-the-box by any AI agent with shell execution capabilities:
- **Claude Code** (Anthropic's CLI agent)
- **Antigravity** (Google DeepMind's agent)
- **Cursor & Windsurf** (IDE-based agents)
- **Open Interpreter**
- **Codex-based Agents & Copilot**
- Any custom agent built with LangChain, AutoGen, or CrewAI

## 💬 Example Prompts for AI Agents
You can paste these directly into Claude, ChatGPT, or your custom Agent:
- *"Run the unified analytics script `./run_all.sh` to check my Google Search Console and GA4 data for the last 7 days, then write a summary report."*
- *"Execute the web analytics skill, compare my Bing search traffic with Google's, and tell me which keywords are performing better on Bing."*
