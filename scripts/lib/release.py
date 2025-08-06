import sys

from lib.github_api import GithubAPI
from lib.utils import ReleaseError, create_release, create_release_notes


class Release:
    def __init__(self):
        self.__api = GithubAPI()

    def __get_sames_release_by_tag(self, releases: list, tag: str) -> list:
        same_prerelease = []
        for release in releases[1:]:
            actually_tag = release["tag_name"]
            if actually_tag.split("-")[0] == tag.split("-")[0]:
                same_prerelease.append(release)
            else:
                break
        return same_prerelease

    def __extract_issues_from_body(self, body: str, all_issues: dict) -> list:
        lines = [line.strip() for line in body.splitlines() if line.strip()]
        issues = []
        is_issues_section = False

        for line in lines:
            if "--- These GitHub issues have been" in line:
                is_issues_section = True
                continue

            if not is_issues_section:
                continue

            parts = line.split()
            if len(parts) < 2:
                continue

            issue_number = int(parts[1].replace("#", ""))
            issue = all_issues.get(issue_number)

            if issue:
                issues.append(issue)

        return issues

    def __transform_issues_to_dict_id(self) -> dict:
        issues_by_id = {}
        all_issues = self.__api.get_all_issues_sorted_by_close()

        for each in all_issues:
            if "pull_request" in each:
                continue
            issues_by_id[each["number"]] = each

        return issues_by_id

    def __create_release_notes_from_release(self, releases: list, old_tag: str):
        releases_bodies = [release["body"] for release in releases]
        issue_list = []
        all_issues = self.__transform_issues_to_dict_id()

        for body in releases_bodies:
            issues = self.__extract_issues_from_body(body, all_issues)
            issue_list.extend(issues)

        return create_release_notes(issue_list, old_tag)

    def release(self):
        releases = self.__api.get_releases()

        if len(releases) <= 0:
            raise ReleaseError("There aren't releases")

        last_release = releases[0]
        tag = last_release["tag_name"]
        new_tag = tag.split("-")[0]

        if not "-rc" in tag:
            raise ReleaseError(
                "It is not possible to generate a release directly from another release. A pre-release candidate must be created and promoted to a full release."
            )

        same_prerelease = self.__get_sames_release_by_tag(releases, tag)
        releases_to_include = [last_release] + same_prerelease
        release_notes = self.__create_release_notes_from_release(
            releases_to_include, tag
        )
        release_information = {
            "new_tag": new_tag,
            "release_notes": release_notes,
            "is_prerelease": False,
            "target_branch": "main",
        }
        create_release(release_information, self.__api)
