import json
import pandas as pd
import requests
from typing import Dict, Optional


# config.json を読み込む関数
def read_config() -> Dict[str, str]:
    try:
        with open("config.json") as f:
            config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("config.json が存在しません")
    return config


# メールアドレスでユーザーを検索する関数
def get_user_by_email(url: str, token: str, email: str) -> Optional[str]:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{url}/api/v4/users/email/{email}", headers=headers)
    if response.status_code == 200:
        return response.json()["id"]
    elif response.status_code == 404:
        print(f"No user with email {email} found")
        return None
    else:
        print(f"Error searching for user with email {email}: {response.text}")
        return None


# ユーザーを作成する関数
def create_user(url: str, token: str, user_data: Dict[str, str]) -> Optional[str]:
    # ユーザーが既に存在するかどうか確認
    existing_user_id = get_user_by_email(url, token, user_data["email"])
    if existing_user_id:
        print(f"User {user_data['email']} already exists")
        return existing_user_id

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
    elif response.status_code == 404:
        print(f"Team {team_name} does not exist")
        return None
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
    elif response.status_code == 404:
        print(f"Channel {channel_name} does not exist")
        return None
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
        print(f"User {user_id} added to channel {channel_id}")
    else:
        print(f"Error adding user {user_id} to channel {channel_id}: {response.text}")


# ユーザーをチームに追加する関数
def add_user_to_team(url: str, token: str, user_id: str, team_id: str) -> None:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(
        f"{url}/api/v4/teams/{team_id}/members",
        headers=headers,
        json={"user_id": user_id, "team_id": team_id},
    )
    if response.status_code == 201:
        print(f"User {user_id} added to team {team_id}")
    else:
        print(f"Error adding user {user_id} to team {team_id}: {response.text}")


def main():
    # config.json の読み込み
    config = read_config()

    # CSVファイルを読み込む
    df = pd.read_csv(config["csv_file"])

    # 各ユーザーを作成し、チームとチャンネルに追加
    for _, row in df.iterrows():
        user_data = {
            "email": row["email"],
            "username": row["username"],
            "password": row["password"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
        }

        # ユーザー作成
        user_id = create_user(config["url"], config["token"], user_data)
        team_id = get_team_id(config["url"], config["token"], row["team_name"])
        if team_id:
            add_user_to_team(
                config["url"], config["token"], user_id, team_id
            )  # ユーザーをチームに追加
            channel_id = get_channel_id(
                config["url"], config["token"], team_id, row["channel_name"]
            )
            if channel_id:
                add_user_to_channel(config["url"], config["token"], user_id, channel_id)


if __name__ == "__main__":
    main()
