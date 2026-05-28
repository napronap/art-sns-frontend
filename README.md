# Art SNS

画像投稿SNSの簡単なプロトタイプです。フロントエンドは SvelteKit、バックエンドは FastAPI、データベースは MongoDB Atlas を使います。

## 必要なもの

- Bun
- Python 3

## 初回セットアップ

フロントエンドの依存関係:

```sh
bun install
```

バックエンドの依存関係:

```sh
python -m pip install -r backend/requirements.txt
```

MongoDB の接続先は `backend/app/database/db.py` に設定されています。

## 起動方法

ターミナルを2つ開きます。

### 1. バックエンド

`backend` フォルダに移動して起動します。

```sh
cd backend
python -m uvicorn app.app:app --host 127.0.0.1 --port 8010 --reload
```

確認:

```txt
http://127.0.0.1:8010/api/posts
```

JSON が表示されればバックエンドは動いています。

### 2. フロントエンド

プロジェクトのルートフォルダに戻って起動します。

```sh
bun run dev -- --host 127.0.0.1 --port 5173
```

ブラウザで開きます。

```txt
http://127.0.0.1:5173/
```

## API プロキシ

フロントエンドは `/api` と `/uploads` をバックエンドに転送します。

転送先:

```txt
http://127.0.0.1:8010
```

設定ファイル:

```txt
vite.config.ts
```

## 主なページ

- `/` ホーム。全ユーザーの投稿をグリッド表示します。
- `/profile` プロフィール。現在のユーザー情報と自分の投稿を表示します。

## 投稿作成

画面右上の「アップロード」ボタンから投稿できます。

必要な入力:

- 本文
- 画像
