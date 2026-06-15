# 自動生成Podcast「おはようトリビア・カフェ」

Google TrendsのニュースとGoogle Gemini、Google Cloud TTSを使用して、毎日のポッドキャスト（音声＋RSSフィード）を完全自動で生成・公開するシステムです。

## セットアップ手順

### 1. GitHubリポジトリの準備
1. このコード一式をGitHubのパブリックリポジトリにプッシュします。
2. リポジトリの `Settings` > `Pages` から、Sourceを「GitHub Actions」または「Branch: main (root)」に設定して、GitHub Pagesを有効化します。
3. `src/update_rss.py` を開き、`BASE_URL` をあなたのGitHub PagesのURL（例: `https://username.github.io/reponame/`）に変更してください。

### 2. フリーBGMの準備
`assets` フォルダ内に `bgm.mp3` という名前で、著作権フリーのBGMファイル（DOVA-SYNDROMEなどでダウンロード可能）を配置してコミットしてください。これが番組の背景音楽になります。

### 3. APIキーの取得と設定（GitHub Secrets）
GitHubの自動実行（Actions）でAPIを利用するために、以下の2つのシークレットキーをGitHubリポジトリの `Settings` > `Secrets and variables` > `Actions` に登録します。

#### ① GEMINI_API_KEY
- **取得元**: [Google AI Studio](https://aistudio.google.com/)
- **内容**: `AIzaSy...` のような文字列のAPIキー。

#### ② GCP_CREDENTIALS
- **取得元**: [Google Cloud Console](https://console.cloud.google.com/)
- **手順**:
  1. 新しいプロジェクトを作成。
  2. 「Cloud Text-to-Speech API」を有効化。
  3. 「IAMと管理」>「サービスアカウント」から新しいサービスアカウントを作成。
  4. そのサービスアカウントの「キー」タブから新しい鍵（JSON）を作成してダウンロード。
- **内容**: ダウンロードしたJSONファイルの中身をすべてコピーして貼り付けます。

### 4. 自動化の開始
設定が完了すると、日本時間の毎日**朝6:00**にGitHub Actionsが起動し、自動でニュースの取得・台本生成・音声合成・RSS更新が行われます。

### 5. Podcast配信プラットフォームへの登録
一度GitHub Actionsが成功すると、`https://<あなたのGitHubユーザー名>.github.io/<リポジトリ名>/feed.xml` というURLでRSSが公開されます。
このURLを、以下のプラットフォームの「RSSを送信する」画面から登録してください。
- Apple Podcasts Connect
- Spotify for Podcasters
- Amazon Music for Podcasters

初回の登録が完了すれば、以後はGitHub Actionsが動くたびに各アプリに新着エピソードが自動配信されます！
