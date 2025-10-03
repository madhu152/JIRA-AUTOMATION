import requests
import json
from requests.auth import HTTPBasicAuth

def create_jira_ticket(email, api_token, project_key, summary, description, issue_type="Task"):
    url = "url"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type}
        }
    }
    
    auth = HTTPBasicAuth(email, api_token)
    
    response = requests.post(url, headers=headers, auth=auth, data=json.dumps(payload), verify=True)
    
    if response.status_code == 201:
        data = response.json()
        print(f"Success! Created Jira issue with key: {data['key']}")
        return data['key']
    else:
        print(f"Failed to create issue. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None


def create_issue_link(email, api_token, inward_issue_key, outward_issue_key, link_type="Relates"):
    url = "jira"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    auth = HTTPBasicAuth(email, api_token)

    payload = {
        "type": {"name": link_type},
        "inwardIssue": {"key": inward_issue_key},
        "outwardIssue": {"key": outward_issue_key}
    }

    response = requests.post(url, headers=headers, auth=auth, json=payload)
    if response.status_code == 201:
        print(f"Successfully linked {inward_issue_key} to {outward_issue_key} with link type '{link_type}'")
        return True
    else:
        print(f"Failed to link issues: {response.status_code} - {response.text}")
        return False


if __name__ == "__main__":
    # Jira auth and project info
    email = "EMIAL.ID"
    api_token = "TOKEN"
    project_key = "PROJECT"
    parent_issue_key = "KEY"  # The existing issue you want to link to

    # New issue details
    summary = "Enhancement request created via API"
    description = "Details about the enhancement and why it's needed..."
    issue_type = "Bug"  # Make sure "Enhancement" is configured in your Jira instance

    # Step 1: Create the new Enhancement issue
    new_issue_key = create_jira_ticket(email, api_token, project_key, summary, description, issue_type)

    # Step 2: Link new issue to existing issue (DELTA-488)
    if new_issue_key:
        linked = create_issue_link(email, api_token, inward_issue_key=parent_issue_key, outward_issue_key=new_issue_key, link_type="Relates")
        if linked:
            print(f"Issue {new_issue_key} successfully linked to {parent_issue_key}")
        else:
            print("Failed to link issues.")
    else:
        print("Issue creation failed; skipping linking.")



