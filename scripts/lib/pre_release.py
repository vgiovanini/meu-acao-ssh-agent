import sys
from datetime import datetime

from lib.github_api import GithubAPI
from lib.utils import ReleaseError, create_release, create_release_notes


class PreRelease:
    def __init__(self):
        self.__api = GithubAPI()

    def semver_calculate(self, issues: list, old_tag: str) -> str:
        old_tag = old_tag.replace("v", "")
        major, minor, patch = map(int, old_tag.split("."))

        has_enhancement = False
        has_bug = False
        has_breaking_change = False

        for each in issues:
            labels = list(map(lambda x: x["name"].lower(), each["labels"]))

            has_enhancement |= "enhancement" in labels
            has_bug |= "bug" in labels
            has_breaking_change |= "breaking changes" in labels

        if has_breaking_change:
            major += 1
            minor = 0
            patch = 0
        elif has_enhancement:
            minor += 1
            patch = 0
        elif has_bug:
            patch += 1

        return f"v{major}.{minor}.{patch}"

    def __candidate_increment(self, old_candidate: str, prefix: str) -> str:
        tag_rc = old_candidate.split("-")
        rc = "-" + tag_rc[1]
        rc_number = int(rc.split(prefix)[-1]) + 1
        tag_rc = tag_rc[0] + (prefix + str(rc_number))
        return tag_rc

    def __prerelease_candidate_increment(
        self, issues: list, old_tag: str
    ) -> str:
        rc_prefix = "-rc"
        if rc_prefix in old_tag:
            tag_rc = self.__candidate_increment(old_tag, rc_prefix)
        else:
            tag_rc = self.semver_calculate(issues, old_tag)
            tag_rc += "-rc1"
        return tag_rc

    def __filter_closed_issues(self, issues: list, since: datetime) -> list:
        filtered = []
        for issue in issues:

            if "pull_request" in issue:
                continue

            closed_at = datetime.strptime(
                issue["closed_at"], "%Y-%m-%dT%H:%M:%SZ"
            )
            if issue["state"] == "closed" and closed_at >= since:
                filtered.append(issue)
        return filtered

    def __fetch_issues_since_last_release(self) -> tuple:
        old_tag = "v1.0.0"
        filtered_issues = []
        releases = self.__api.get_releases()

        if not releases:
            filtered_issues = self.__api.get_all_issues_sorted_by_close()
        else:
            last_release = releases[0]
            release_date = datetime.strptime(
                last_release["published_at"], "%Y-%m-%dT%H:%M:%SZ"
            )
            issues = self.__api.get_issues_since(release_date)
            filtered_issues = self.__filter_closed_issues(issues, release_date)
            old_tag = last_release["tag_name"]
        return filtered_issues, old_tag

    def pre_release(self):
        issues, old_tag = self.__fetch_issues_since_last_release()

        if len(issues) <= 0:
            raise ReleaseError("No issues to analyze")

        new_tag = self.__prerelease_candidate_increment(issues, old_tag)
        release_notes = create_release_notes(
            issues,
            old_tag,
        )

        release_information = {
            "new_tag": new_tag,
            "release_notes": release_notes,
            "is_prerelease": True,
            "target_branch": "homolog",
        }

        create_release(release_information, self.__api)
