import json
import requests


def get_open_source_projects():
    response = requests.get(
        'https://api.github.com/search/repositories?q=stars:>10000&sort=stars')
    if response.status_code == 200:
        data = response.json()
        projects = [{"name": item["name"], "url": item["html_url"], "open_issues": item["open_issues_count"], "pull_requests": get_pull_requests_count(item["pulls_url"])}
                    for item in data["items"]]
        return projects
    else:
        return []


def get_pull_requests_count(pulls_url):
    pulls_url = pulls_url.split("{")[0]  # Remove the template part of the URL
    response = requests.get(pulls_url)
    if response.status_code == 200:
        return len(response.json())
    else:
        return 0


def main():
    projects = get_open_source_projects()
    with open('projects.json', 'w') as f:
        json.dump(projects, f, indent=4)


if __name__ == "__main__":
    main()
