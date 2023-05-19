# Mattermost User Control

## 概要
このプロジェクトは、Mattermostユーザーの管理を行うためのスクリプトです。
ご興味のある方は以下のMattermostサイトに参加してみてください。
# [ワチャワチャするサイト](https://mattermost.chotto.news/)

### register_users.py

概要

`register_users.py`は、CSVファイルからユーザー情報を読み取り、新規Mattermostユーザーを作成し、指定されたチームとチャンネルに追加するためのスクリプトです。

主な機能は以下の通りです：

- CSVファイルからユーザー情報（メール、ユーザーネーム、パスワード、名前、姓）を読み込む
- 新規ユーザーをMattermostに作成する
- ユーザーを指定されたチームに追加する
- ユーザーを指定されたチャンネルに追加する

使用方法

`python register_users.py`

依存関係

- Python 3.x
- requests ライブラリ
- pandas ライブラリ

注意事項

- このスクリプトはconfig.jsonとCSVファイルを読み込む必要があります。config.jsonにはMattermostのURLとトークンを、CSVファイルには作成するユーザーの情報とそのユーザーを追加するチーム名とチャンネル名を含めてください。

## mattermost-user-control.py
### 概要
`mattermost-user-control.py`は、Mattermostのユーザー管理に関連する機能を提供するスクリプトです。具体的な機能については以下の通りです。

- 新規ユーザーの作成
- ユーザーの削除
- ユーザーの権限設定

### 使用方法

python mattermost-user-control.py

### 依存関係
- Python 3.x
- requests ライブラリ

## mattermost-user-management.py
### 概要
`mattermost-user-management.py`は、Mattermostのユーザー参加状況と指示内容を管理するためのスクリプトです。

### 使用方法

python mattermost-user-management.py


### 依存関係
- Python 3.x
- requests ライブラリ
- openpyxl ライブラリ

## 注意事項
- このプロジェクトはMITライセンスのもとで提供されています。
- 実行する前に、事前にMattermostの設定ファイル（`config.json`）を正しく設定してください。
- 機密情報（アクセストークンなど）が含まれるため、GitHubなどの公開リポジトリに設定ファイルをアップロードしないでください。

## 連絡先
- 開発者: [rinmon]
- メール: [info@chotto.news]
