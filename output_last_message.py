import os
import json
import requests
import sys
import datetime
from urllib.parse import quote

# 設定ファイルを読み込みます。
try:
    with open("config.json") as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"設定ファイルの読み込みに失敗しました: {e}")
    sys.exit(1)

# Mattermost のエンドポイントとアクセストークンを設定します。
url = config["url"]
token = config["token"]
headers = {"Authorization": f"Bearer {token}"}

# 出力ファイルを作成します。
output_file_path = os.path.join(config["excel_dir"], "output_last_message.txt")


def get_all_teams():
    response = requests.get(f"{url}/api/v4/teams", headers=headers)
    response.raise_for_status()
    return response.json()


def get_channels_for_team(team_id):
    public_channels_response = requests.get(
        f"{url}/api/v4/teams/{team_id}/channels", headers=headers
    )
    public_channels_response.raise_for_status()
    private_channels_response = requests.get(
        f"{url}/api/v4/users/me/teams/{team_id}/channels", headers=headers
    )
    private_channels_response.raise_for_status()
    return public_channels_response.json() + private_channels_response.json()


def get_last_message_info(channel_id):
    response = requests.get(
        f"{url}/api/v4/channels/{channel_id}/posts",
        headers=headers,
        params={"page": 0, "per_page": 1},
    )

    response.raise_for_status()

    try:
        posts_data = response.json()
        if not posts_data["order"]:
            print(f"チャンネルID '{channel_id}'にメッセージが見つかりませんでした")
            return None
    except ValueError:
        print(f"チャンネル {channel_id} のJSONデータ解析エラー: {response.text}")
        return None

    last_post_id = posts_data["order"][0]
    last_post = posts_data["posts"][last_post_id]
    last_post_time = datetime.datetime.fromtimestamp(last_post["create_at"] / 1000.0)

    return last_post_time


with open(output_file_path, "w", encoding="utf-8") as output_file:
    for team in get_all_teams():
        output_file.write(f"Team: {team['display_name']} - Team ID: {team['id']}\n")
        for channel in get_channels_for_team(team["id"]):
            last_message_time = get_last_message_info(channel["id"])
            channel_type = "Pub" if channel["type"] == "O" else "Pvt"
            if last_message_time is not None:
                output_file.write(
                    f"{channel_type} Channel: {channel['display_name']} - Channel ID: {channel['id']} - Last message time: {last_message_time}\n"
                )
        output_file.write("\n")

print(f"テキストファイルに処理内容を出力しました: {output_file_path}")
