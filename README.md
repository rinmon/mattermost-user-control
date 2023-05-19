# Mattermost User Control

## 概要
このプロジェクトは、Mattermostユーザーの管理を行うための一連のスクリプトを提供します。各スクリプトの詳細と使用方法については、以下をご覧ください。

Mattermostについての詳細や、コミュニティとの交流を希望される方は、[ワチャワチャするサイト](https://mattermost.chotto.news/)をご覧ください。

### 1. register_users.py

`register_users.py`は、CSVファイルからユーザー情報を読み取り、新規Mattermostユーザーを作成し、指定されたチームとチャンネルに追加するためのスクリプトです。

**主な機能**：

- CSVファイルからユーザー情報（メール、ユーザーネーム、パスワード、名前、姓）を読み込む
- 新規ユーザーをMattermostに作成する
- ユーザーを指定されたチームに追加する
- ユーザーを指定されたチャンネルに追加する

**使用方法**：

`python register_users.py`

**依存関係**：

- Python 3.x
- requests ライブラリ
- pandas ライブラリ

### 2. mattermost-user-control.py

`mattermost-user-control.py`は、Mattermostのユーザー管理に関連する機能を提供するスクリプトです。

**主な機能**：

- 新規ユーザーの作成
- ユーザーの削除
- ユーザーの権限設定

**使用方法**：

`python mattermost-user-control.py`

**依存関係**：

- Python 3.x
- requests ライブラリ

### 3. mattermost-user-management.py

`mattermost-user-management.py`は、Mattermostのユーザー参加状況と指示内容を管理するためのスクリプトです。

**使用方法**：

`python mattermost-user-management.py`

**依存関係**：

- Python 3.x
- requests ライブラリ
- openpyxl ライブラリ

## 注意事項
このプロジェクトはMITライセンスのもとで提供されています。実行する前に、事前にMattermostの設定ファイル（`config.json`）を正しく設定してください。機密情報（アクセストークンなど）が含まれるため、GitHubなどの公開リポジトリに設定ファイルをアップロードしないでください。

## 連絡先
- 開発者: rinmon
- メール: [info@chotto.news](mailto:info@chotto.news)
