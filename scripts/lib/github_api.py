import os
from datetime import datetime

import requests


class GithubAPI:
    def __init__(self):
        self.credentials = self.load_github_config()
        self.owner = self.credentials["owner"]
        self.repository = self.credentials["repo"]
        self.headers = self.credentials["headers"]

    def load_github_config(self):
        return {
            "owner": os.getenv("GH_OWNER"),
            "repo": os.getenv("GH_REPO"),
            "headers": {
                "Authorization": f"Bearer {os.getenv('GH_TOKEN')}",
                "Accept": "application/vnd.github+json",
            },
        }

    def issue_pagination(
        self, url: str, headers: dict, data: list, params: dict = None
    ) -> list:
        if not data:
            data = []
        response = requests.get(url=url, headers=headers, params=params)
        params = None
        if response.status_code != 200:
            return data

        data.extend(response.json())
        url = response.links.get("next", {}).get("url")

        if not url:
            return data

        return self.issue_pagination(
            url=url, headers=headers, params=params, data=data
        )

    def get_releases(self) -> list:
        url = f"https://api.github.com/repos/{self.owner}/{self.repository}/releases"
        data_response = []
        data_response = self.issue_pagination(
            url=url, headers=self.headers, data=data_response
        )
        return data_response

    def get_all_issues_sorted_by_close(self) -> list:
        url = f"https://api.github.com/repos/{self.owner}/{self.repository}/issues"
        params = {"state": "closed", "per_page": 100}
        data_response = []
        data_response = self.issue_pagination(
            url=url,
            headers=self.headers,
            params=params,
            data=data_response,
        )
        return data_response

    def get_issues_since(self, date: datetime) -> list:
        since = date.strftime("%Y-%m-%dT%H:%M:%SZ")
        url = f"https://api.github.com/repos/{self.owner}/{self.repository}/issues"
        params = {"state": "closed", "since": since, "per_page": 100}
        data_response = []
        data_response = self.issue_pagination(
            url=url,
            headers=self.headers,
            params=params,
            data=data_response,
        )
        return data_response
