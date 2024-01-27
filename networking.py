import os

import requests
from dotenv import load_dotenv


class DatabaseConnection:
    def __init__(self):
        load_dotenv()
        self.base_url = os.environ.get("API_URL")
        self.session = requests.Session()
        self.acces_token = None
        self.get_acces_token()

    def get_acces_token(self):
        self.acces_token = requests.post(
            f"{self.base_url}/auth/signin",
            data={
                "email": os.environ.get("EMAIL"),
                "password": os.environ.get("PASSWORD"),
            },
        ).json()["access_token"]

    def create_build(self, build_json):
        # Create build
        data = requests.post(
            f"{self.base_url}/build",
            data={
                "title": build_json["title"],
                "description": build_json["description"],
                "race": "TERRAN",
                "v_race": "TERRAN",
                "user_id": "1",
            },
            headers={
                "Authorization": f"Bearer {self.acces_token}",
            },
        )

        # Add all steps
        for index, row in enumerate(build_json["data"]):
            total_seconds = 0
            if row["timer"]:
                minutes, seconds = map(int, row["timer"].split(":"))
                total_seconds = minutes * 60 + seconds

            requests.post(
                f"{self.base_url}/step",
                data={
                    "description": row["description"],
                    "build_id": str(data.json()["id"]),
                    "position": str(index + 1),
                    "timer": str(total_seconds),
                    "population": row["population"],
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Bearer {self.acces_token}",
                },
            )
