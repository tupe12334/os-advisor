import json
import requests
import datetime
from typing import List, Dict, Any


def get_open_source_projects(
    existing_projects_in_file: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    response = requests.get(
        "https://api.github.com/search/repositories?q=stars:>10000&sort=stars"
    )
    if response.status_code != 200:
        print("Failed to fetch data from GitHub API")
        return []
    data = response.json()
    projects = [
        {
            "name": item["name"],
            "url": item["html_url"],
            "open_issues": item["open_issues_count"],
            "pull_requests": get_pull_requests_count(item["pulls_url"]),
            "request_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        for item in data["items"]
    ]
    return projects


def get_pull_requests_count(pulls_url: str) -> int:
    pulls_url = pulls_url.split("{")[0]  # Remove the template part of the URL
    response = requests.get(pulls_url)
    if response.status_code == 200:
        return len(response.json())
    else:
        return 0


def main() -> None:
    projects: List[Dict[str, Any]] = []
    with open("projects.json", "r") as fr:
        projects = json.load(fr)
    projects = get_open_source_projects(projects)
    with open("projects.json", "w") as f:
        json.dump(projects, f, indent=4)


if __name__ == "__main__":
    main()
