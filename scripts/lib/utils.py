import sys
from operator import itemgetter

import requests


class ReleaseError(Exception):
    """Custom exception for release related errors."""

    pass


def create_release_notes(issues: list, old_tag: str) -> str:
    notes = "## Features\n\n"
    foot = ""
    for each in issues:
        labels = list(map(lambda x: x["name"].lower(), each["labels"]))
        issue_name = each["title"]
        issue_number = each["number"]
        if "epic" in labels:
            notes += f"- {issue_name}\n"
        foot += f"- #{issue_number} - {issue_name}\n"
    notes += (
        f"\n\n --- These GitHub issues have been addressed since the previous {old_tag} tagged release:\n\n"
        if not old_tag == "v1.0.0"
        else "\n\n --- These Github issues have been addressed in the first release\n\n"
    )
    notes += foot
    return notes


def create_release(release_data: dict, github_api: dict):
    new_tag, release_notes, is_prerelease, target_branch = itemgetter(
        "new_tag", "release_notes", "is_prerelease", "target_branch"
    )(release_data)

    url = f"https://api.github.com/repos/{github_api.owner}/{github_api.repository}/releases"

    repository_name = (
        github_api.repository.replace("-", " ").replace("_", " ").title()
    )

    payload = {
        "tag_name": new_tag,
        "name": repository_name + "\n" + new_tag,
        "body": release_notes,
        "draft": False,
        "prerelease": is_prerelease,
        "target_commitish": target_branch,
    }

    response = requests.post(
        url=url,
        json=payload,
        headers=github_api.headers,
    )

    if response.status_code == 201:
        print(f"Release {new_tag} created successfully!")
        print(f"TAG: {new_tag}")
    else:
        raise ReleaseError(f"Release {new_tag} ERROR !")
