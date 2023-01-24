import requests
import json

# PagerDuty API credentials
pagerduty_api_key = "YOUR_PAGERDUTY_API_KEY"

# Okta API credentials
okta_api_token = "YOUR_OKTA_API_TOKEN"
okta_org_url = "https://your-okta-org.com"

# PagerDuty on-call schedule ID
schedule_id = "YOUR_PAGERDUTY_SCHEDULE_ID"

# Okta group ID for on-call team
okta_group_id = "YOUR_OKTA_GROUP_ID"

# Get current on-call schedule from PagerDuty
schedule_url = f"https://api.pagerduty.com/schedules/{schedule_id}/entries"
schedule_headers = {
    "Accept": "application/vnd.pagerduty+json;version=2",
    "Authorization": f"Token token={pagerduty_api_key}"
}
schedule_response = requests.get(schedule_url, headers=schedule_headers)
schedule_data = schedule_response.json()

# Extract on-call user IDs from schedule
on_call_user_ids = [entry["user"]["id"] for entry in schedule_data["entries"]]

# Get all users from Okta
users_url = f"{okta_org_url}/api/v1/users"
users_headers = {
    "Accept": "application/json",
    "Authorization": f"SSWS {okta_api_token}",
}
users_response = requests.get(users_url, headers=users_headers)
users_data = users_response.json()

# Extract Okta user IDs from all users
okta_user_ids = [user["id"] for user in users_data]

# Add on-call users to Okta group
for user_id in on_call_user_ids:
    if user_id in okta_user_ids:
        group_url = f"{okta_org_url}/api/v1/groups/{okta_group_id}/users/{user_id}"
        group_headers = {
            "Accept": "application/json",
            "Authorization": f"SSWS {okta_api_token}",
            "Content-Type": "application/json"
        }
        requests.put(group_url, headers=group_headers)

