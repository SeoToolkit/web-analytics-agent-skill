# Web Analytics Agent Skill

<p align="center">
  <img src="https://www.gstatic.com/images/branding/product/1x/search_console_64dp.png" alt="Google Search Console" height="24" /> <strong>Google Search Console</strong><br><br>
  <img src="https://www.gstatic.com/analytics-suite/header/suite/v2/ic_analytics.svg" alt="Google Analytics" height="24" /> <strong>Google Analytics 4</strong><br><br>
  <img src="https://upload.wikimedia.org/wikipedia/commons/e/e9/Bing_logo.svg" alt="Bing Webmaster Tools" height="24" /> <strong>Bing Webmaster</strong>
</p>

[English](./README.md) | [简体中文](./README.zh-CN.md) | [繁體中文](./README.zh-TW.md) | [日本語](./README.ja.md)


这是一个强大的 **AI Agent 技能包** 与 **Python 自动化分析脚本**，旨在为您提供网站流量的 360 度全景视图。本项目无缝对接了 **Google Search Console (GSC)**、**Google Analytics 4 (GA4)** 以及 **Bing Webmaster Tools** 的官方 API。无论您是需要让大模型自主进行 **SEO 流量诊断**、**关键词挖掘**，还是搭建日常的**流量监控流水线**，该项目都能开箱即用。

**关键词 / 标签**: `seo-agent`, `ai-seo`, `web-analytics`, `ga4`, `google-analytics`, `google-search-console`, `seo-automation`, `agent-skill`, `mcp-server`

## 📥 如何安装 (Installation)
对于目前主流的 AI 智能体（如 Cursor, Cline, Claude Code, Antigravity 等），最简单且最推荐的安装方式是直接**将本仓库的地址发送给 AI**，让 AI 自主阅读并挂载此技能。

**您可以直接把下面这句话复制发给您的 AI 助手：**
> "Please read and install this AI Agent Skill: https://github.com/SeoToolkit/web-analytics-agent-skill . Read the `SKILL.md` file carefully to understand how to use it."

或者，如果您的 AI 助手支持直接在本地工作区读取技能，您只需将其克隆到项目下：
```bash
git clone https://github.com/SeoToolkit/web-analytics-agent-skill.git .skills/web-analytics-agent-skill
```

## 📊 效果演示 (Example Reports)

| Google Search Console | Google Analytics 4 | Bing Webmaster Tools |
| :---: | :---: | :---: |
| <img src="./assets/demo1.png" alt="Google Search Console Report"> | <img src="./assets/demo2.png" alt="Google Analytics 4 Report"> | <img src="./assets/demo3.png" alt="Bing Webmaster Tools Report"> |

## 🛠️ 核心特性
- **Google Search Console**: 自动获取 Google 搜索排名、曝光与点击转化率。
- **Google Analytics 4 (GA4)**: 追踪真实的用户会话、留存时间及流量来源。
- **Bing Webmaster Tools**: 支持跨搜索引擎的流量比例分析与异常检测。

## 📦 环境准备
1. 创建虚拟环境并安装依赖：
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. 复制 `.env.example` 为 `.env`，然后根据您需要的渠道进行以下配置：

### 渠道 1：Bing Webmaster Tools
- **授权方式**: API 密钥 (手动获取)
- **配置步骤**:
  1. 访问 [Bing Webmaster Tools](https://www.bing.com/webmasters/)。
  2. 点击右上角齿轮图标(设置) -> API 访问 -> API 密钥。
  3. 生成并复制您的 API 密钥。
- **环境变量** (`.env`):
  - `BING_API_KEY`: 您刚才复制的 API 密钥。
  - `BING_SITE_URL`: 您的 Bing 验证域名（例：`https://example.com`）。

### 渠道 2：Google Search Console (GSC)
- **授权方式**: OAuth 2.0 (手动获取 `client_secret.json` + 自动弹窗授权)
- **配置步骤**:
  1. 访问 [Google Cloud Console](https://console.cloud.google.com/) 创建新项目。
  2. 在顶部搜索栏中搜索并启用 **Google Search Console API**。
  3. 配置「OAuth 同意屏幕」（选择外部应用，将您的邮箱添加为测试用户）。
  4. 进入左侧「凭据」菜单 -> 点击顶部「+ 创建凭据」 -> 选择「OAuth 客户端 ID」。
  5. 应用类型选择「桌面应用 (Desktop app)」，创建完毕后下载 JSON 文件。
  6. 将下载的文件重命名为 `client_secret.json`，并把它放在项目根目录下。
  7. *(自动)* 首次运行脚本时，系统会自动弹出浏览器让您登录并授权。
  > **💡 重要提醒**：请确保弹窗登录的 Google 账号**拥有该 GSC/GA4 站点的访问权限**，并在授权界面**手工勾选允许**读取 Search Console 和 Analytics 数据的选框。如果因为漏选或账号不对导致 403 权限错误，AI 智能体在执行时会自动捕获并提醒您检查。
- **环境变量** (`.env`):
  - `GSC_SITE_URL`: Google Search Console 的资源 URL（例：`sc-domain:example.com`）。
  - `SITE_LAUNCH_DATE`: (可选) 您网站的上线日期，用于计算“上线至今”的趋势数据（格式：`YYYY-MM-DD`）。

### 渠道 3：Google Analytics 4 (GA4)
- **授权方式**: OAuth 2.0 (复用 GSC 的 `client_secret.json` + 自动弹窗授权)
- **配置步骤**:
  1. 在刚才的 Google Cloud 项目中，继续搜索并启用 **Google Analytics Data API**。
  2. 确保 `client_secret.json` 文件已经在项目根目录下。
  3. *(自动)* 首次运行脚本时，系统会自动弹出浏览器让您登录并授权。
- **环境变量** (`.env`):
  - `GA4_PROPERTIES`: 您的 GA4 属性 ID 及标签（格式必须为 `ID=标签`，例：`123456789=MyWebsite`）。

## 📄 配置文件格式示例

以下是您需要准备的两个核心配置文件的格式要求：

### 1. `.env`
在项目根目录下创建该文件，按需填写您所需的渠道：
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
这是从 Google Cloud Console 下载下来的原始凭证文件，它的标准格式如下（请勿修改其内部结构）：
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

## 🚀 运行步骤
当 AI 智能体需要进行流量诊断时，最简单的方式是直接执行自动化入口脚本。它会自动创建虚拟环境、安装依赖并依次执行所有分析：
```bash
./run_all.sh
```
或者，您也可以手动激活环境并执行单个脚本：
- `scripts/auth_google.py`: 专门用于处理 Google OAuth 2.0 授权的脚本。独立运行它可以生成 `token.json` 本地授权文件。*（注意：其他脚本在发现缺失 token 时也会自动触发此授权流程，所以手动运行它是可选的）*。
- `scripts/analyze_gsc.py`: 用于获取和分析 Google Search Console 数据。
- `scripts/ga4_both.py`: 用于获取和分析 Google Analytics 4 数据。
- `scripts/bing_webmaster.py`: 用于获取和分析 Bing Webmaster Tools 数据。

```bash
source .venv/bin/activate
python3 scripts/auth_google.py
```

## 🤖 支持的 AI 智能体 (Supported Agents)
由于本技能采用标准 CLI 脚本架构，通过终端标准输出（STDOUT）返回结构化数据，因此**原生支持任何具备终端执行能力的 AI 智能体**，完全无需复杂的接口适配：
- **Claude Code** (Anthropic 官方 CLI 智能体)
- **Antigravity** (Google DeepMind 智能体)
- **Cursor & Windsurf** (具备终端执行能力的 IDE 智能体)
- **Open Interpreter**
- **基于 Codex 的智能体及 Copilot Workspace**
- 任何基于 LangChain, AutoGen 或 CrewAI 构建的自定义 Agent

## 💬 给 AI 的提示词示例 (Example Prompts)
您可以直接将以下提示词复制给您的 AI 助手（如 Claude、ChatGPT 等）：
- *"执行流量诊断脚本 `./run_all.sh`，帮我检查 Google Search Console 和 GA4 近 7 天的数据，并写一份总结报告。"*
- *"调用 web analytics 技能，对比我在 Bing 和 Google 上的搜索流量，告诉我哪些关键词在 Bing 上表现更好。"*
