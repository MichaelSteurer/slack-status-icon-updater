import json
import os
import requests
import sys
import urllib
import yaml

URL = None
ICONS = [":slightly_smiling_face:", ":upside_down_face:"]


def set_credentials():
    token = ""
    root_directory = os.path.dirname(os.path.realpath(__file__))
    with open(root_directory + "/credentials.yaml", 'r') as ymlfile:
        token = yaml.load(ymlfile).get("token")
    if not token:
        print "ERROR: Token not set (see credentials.yaml)"
        sys.exit(1)
    global URL
    URL = "https://slack.com/api/{method}?token=" + token

    authenticated = check_authentication()
    if not authenticated:
        print "ERROR: Token '{}' is wrong (see credentials.yaml)".format(token)
        sys.exit(1)


def main():
    set_credentials()
    current_icon = get_status_icon()

    current_index = ICONS.index(current_icon) if current_icon in ICONS else 0
    next_index = (current_index + 1) % len(ICONS)
    next_icon = ICONS[next_index]

    set_status_icon(next_icon)


def check_authentication():
    url = URL.format(method="auth.test")
    response = requests.get(url)
    content = json.loads(response.content)
    return content.get("ok")


def set_status_icon(icon):
    url = URL.format(method="users.profile.set")
    profile = {
        "status_emoji": icon
    }
    url += '&profile=' + urllib.quote(json.dumps(profile))

    requests.get(url)
    return get_status_icon()


def get_status_icon():
    url = URL.format(method="users.profile.get")
    response = requests.get(url)
    response = json.loads(response.content)
    return response.get("profile", {}).get("status_emoji")


if __name__ == "__main__":
    main()
