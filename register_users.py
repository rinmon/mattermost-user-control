import json
import pandas as pd
import requests
from typing import Dict, Optional


# config.json を読み込む関数
def read_config() -> Dict[str, str]:
    with open("config.json") as f:
        config = json.load(f)
    return config


# ユーザーを作成する関数
def create_user(url: str, token: str, user_data: Dict[str, str]) -> Optional[str]:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(f"{url}/api/v4/users", headers=headers, json=user_data)
    if response.status_code == 201:
        print(f"User {user_data['email']} created successfully")
        return response.json()["id"]
    else:
        print(f"Error creating user {user_data['email']}: {response.text}")
        return None


# チームIDを取得する関数
def get_team_id(url: str, token: str, team_name: str) -> Optional[str]:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{url}/api/v4/teams/name/{team_name}", headers=headers)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        print(f"Error getting team ID for {team_name}: {response.text}")
        return None


# チャンネルIDを取得する関数
def get_channel_id(
    url: str, token: str, team_id: str, channel_name: str
) -> Optional[str]:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{url}/api/v4/teams/{team_id}/channels/name/{channel_name}", headers=headers
    )
    if response.status_code == 200:
        return response.json()["id"]
    else:
        print(f"Error getting channel ID for {channel_name}: {response.text}")
        return None


# ユーザーをチャンネルに追加する関数
def add_user_to_channel(url: str, token: str, user_id: str, channel_id: str) -> None:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(
        f"{url}/api/v4/channels/{channel_id}/members",
        headers=headers,
        json={"user_id": user_id},
    )
    if response.status_code == 201:
        print(f"User ID {user_id} added to channel ID {channel_id}")
    else:
        print(
            f"Error adding user ID {user_id} to channel ID {channel_id}: {response.text}"
        )


def main():
    config = read_config()
    url, token = config["url"], config["token"]
    excel_file = config["excel_dir"] + config["excel_file"]

    # Excel ファイルからユーザーリストを読み込む
    users_df = pd.read_excel(excel_file)

    # Mattermost API を使ってユーザーを登録する
    for _, row in users_df.iterrows():
        user_data = {
            "email": row["email"],
            "username": row["username"],
            "password": row["password"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
        }
        user_id = create_user(url, token, user_data)
        if (
            user_id
            and not pd.isna(row["team_name"])
            and not pd.isna(row["channel_name"])
        ):
            team_id = get_team_id(url, token, row["team_name"])
            channel_id = get_channel_id(url, token, team_id, row["channel_name"])
            if channel_id:
                add_user_to_channel(url, token, user_id, channel_id)


if __name__ == "__main__":
    main()
