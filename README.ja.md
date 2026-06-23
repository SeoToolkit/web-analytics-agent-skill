# Web Analytics Agent Skill

<p align="center">
  <img src="https://www.gstatic.com/images/branding/product/1x/search_console_64dp.png" alt="Google Search Console" height="24" /> <strong>Google Search Console</strong><br><br>
  <img src="https://www.gstatic.com/analytics-suite/header/suite/v2/ic_analytics.svg" alt="Google Analytics" height="24" /> <strong>Google Analytics 4</strong><br><br>
  <img src="https://upload.wikimedia.org/wikipedia/commons/e/e9/Bing_logo.svg" alt="Bing Webmaster Tools" height="24" /> <strong>Bing Webmaster</strong>
</p>

[English](./README.md) | [简体中文](./README.zh-CN.md) | [繁體中文](./README.zh-TW.md) | [日本語](./README.ja.md)


ウェブサイトの検索パフォーマンスを360度見渡すことができる、強力な**AIエージェントスキル**および**Python自動化ツール**です。**Google Search Console (GSC)**、**Google Analytics 4 (GA4)**、**Bing Webmaster Tools**のAPIをシームレスに統合し、AIエージェント（またはCI/CDパイプライン）が自律的に**SEO自動化**、**トラフィック診断**、**クロスプラットフォームのキーワード調査**を実行できるようにします。

**キーワード / タグ**: `seo-agent`, `ai-seo`, `web-analytics`, `ga4`, `google-analytics`, `google-search-console`, `seo-automation`, `agent-skill`, `mcp-server`

## 📥 インストール方法 (Installation)
現在主流の AI エージェント（Cursor、Cline、Claude Code、Antigravity など）にとって、最も簡単で推奨されるインストール方法は、**このリポジトリの URL を AI に直接送信し**、AI に自律的に読み込ませてこのスキルをマウントさせることです。

**以下のプロンプトをコピーして、お使いの AI アシスタントに直接送信してください：**
> "Please read and install this AI Agent Skill: https://github.com/SeoToolkit/web-analytics-agent-skill . Read the `SKILL.md` file carefully to understand how to use it."

または、AI アシスタントがローカル ワークスペースから直接スキルを読み込むことをサポートしている場合は、プロジェクト内にクローンするだけです：
```bash
git clone https://github.com/SeoToolkit/web-analytics-agent-skill.git .skills/web-analytics-agent-skill
```

## 📊 サンプルレポート (Example Reports)

| Google Search Console | Google Analytics 4 | Bing Webmaster Tools |
| :---: | :---: | :---: |
| <img src="./assets/demo1.png" alt="Google Search Console Report"> | <img src="./assets/demo2.png" alt="Google Analytics 4 Report"> | <img src="./assets/demo3.png" alt="Bing Webmaster Tools Report"> |

## 🛠️ 主な特徴
- **Google Search Console**: 検索順位、インプレッション、クリック率を自動で取得します。
- **Google Analytics 4 (GA4)**: 実際のユーザーセッション、直帰率、トラフィックソースを追跡します。
- **Bing Webmaster Tools**: Bingからの検索統計を直接取得し、Googleと比較分析します。

## 📦 環境構築
1. 仮想環境を作成し、依存関係をインストールします:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. `.env.example` を `.env` にコピーし、必要なチャネルを設定します。

### チャネル 1：Bing Webmaster Tools
- **認証方法**: API キー (手動取得)
- **セットアップ手順**:
  1. [Bing Webmaster Tools](https://www.bing.com/webmasters/) にアクセスします。
  2. 右上の歯車アイコン(設定) -> API アクセス -> API キーをクリックします。
  3. APIキーを生成してコピーします。
- **環境変数** (`.env`):
  - `BING_API_KEY`: コピーしたAPIキー。
  - `BING_SITE_URL`: Bingで確認されたドメイン（例：`https://example.com`）。

### チャネル 2：Google Search Console (GSC)
- **認証方法**: OAuth 2.0 (手動 `client_secret.json` + 自動ブラウザプロンプト)
- **セットアップ手順**:
  1. [Google Cloud Console](https://console.cloud.google.com/) にアクセスし、プロジェクトを作成します。
  2. **Google Search Console API** を検索して有効にします。
  3. 「OAuth 同意画面」を構成します（外部を選択し、自分のメールをテストユーザーとして追加します）。
  4. 左側のメニュー「認証情報」->「+ 認証情報の作成」->「OAuth クライアント ID」をクリックします。
  5. アプリケーションの種類として「デスクトップ アプリ (Desktop app)」を選択し、作成して JSON ファイルをダウンロードします。
  6. ダウンロードしたファイルの名前を `client_secret.json` に変更し、プロジェクトのルートディレクトリに配置します。
  7. *(自動)* 初回実行時に、スクリプトがログイン用のブラウザを自動的にポップアップします。
  > **💡 重要な注意事項**: ログインするGoogleアカウントが、GSCおよびGA4プロパティへのアクセス権を持っていることを確認してください。ポップアップ表示時に、Search ConsoleとAnalyticsデータへのアクセスを許可するチェックボックスを必ずオンにしてください。権限不足で403エラーが発生した場合、通常AIエージェントがエラーを検知して注意を促します。
- **環境変数** (`.env`):
  - `GSC_SITE_URL`: あなたのGSCプロパティURL（例：`sc-domain:example.com`）。
  - `SITE_LAUNCH_DATE`: (オプション) 「開始以降」のメトリクスに使用されるウェブサイトの公開日（形式：`YYYY-MM-DD`）。

### チャネル 3：Google Analytics 4 (GA4)
- **認証方法**: OAuth 2.0 (GSCと同じ `client_secret.json` を使用 + 自動ブラウザプロンプト)
- **セットアップ手順**:
  1. 同じGoogle Cloudプロジェクトで、**Google Analytics Data API** を検索して有効にします。
  2. `client_secret.json` がプロジェクトのルートにあることを確認します。
  3. *(自動)* 初回実行時に、スクリプトがログイン用のブラウザを自動的にポップアップします。
- **環境変数** (`.env`):
  - `GA4_PROPERTIES`: GA4プロパティIDとラベル（形式は `ID=ラベル` である必要があります。例：`123456789=MyWebsite`）。

## 📄 設定ファイルのフォーマット例

準備する必要がある2つの主要な設定ファイルのフォーマットです：

### 1. `.env`
プロジェクトのルートディレクトリにこのファイルを作成し、必要なチャネルを設定します。
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
これはGoogle Cloud Consoleから直接ダウンロードした認証情報ファイルです。標準フォーマットは以下のようになります（内部構造は変更しないでください）。
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

## 🚀 実行手順
トラフィック分析が必要な場合、最も簡単な方法は統合スクリプトを実行することです。これにより、仮想環境の作成、依存関係のインストール、すべての分析が自動的に実行されます。
```bash
./run_all.sh
```
または、環境を手動でアクティブ化し、個々のスクリプトを実行することもできます。
- `scripts/auth_google.py`: Google OAuth 2.0 認証を処理するための専用スクリプトです。これを実行すると、ローカルの `token.json` ファイルが生成されます。*（注：他のスクリプトは、トークンがない場合に自動的にこのフローを呼び出すため、手動での実行はオプションです）*。
- `scripts/analyze_gsc.py`: Google Search Console のデータを取得して分析します。
- `scripts/ga4_both.py`: Google Analytics 4 のデータを取得して分析します。
- `scripts/bing_webmaster.py`: Bing Webmaster Tools のデータを取得して分析します。

```bash
source .venv/bin/activate
python3 scripts/auth_google.py
```

## 🤖 サポートされている AI エージェント (Supported Agents)
このスキルは標準のCLIスクリプトアーキテクチャを採用しており、標準出力（STDOUT）を介して構造化データを返すため、**シェル実行機能を持つすべての AI エージェントをネイティブにサポート**します。複雑なプラグインの適応は必要ありません。
- **Claude Code** (Anthropicの公式CLIエージェント)
- **Antigravity** (Google DeepMindのエージェント)
- **Cursor & Windsurf** (IDEベースのエージェント)
- **Open Interpreter**
- **CodexベースのエージェントとCopilot Workspace**
- LangChain、AutoGen、またはCrewAIで構築されたカスタムエージェント

## 💬 AIエージェントへのプロンプト例 (Example Prompts)
以下のプロンプトをClaude、ChatGPT、またはカスタムエージェントに直接貼り付けることができます：
- *"統合分析スクリプト `./run_all.sh` を実行して、過去7日間のGoogle Search ConsoleとGA4のデータを確認し、サマリーレポートを作成してください。"*
- *"web analytics スキルを実行して、BingとGoogleの検索トラフィックを比較し、Bingでより良いパフォーマンスを示しているキーワードを教えてください。"*
