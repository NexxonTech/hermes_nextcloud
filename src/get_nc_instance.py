import os

from nc_py_api import Nextcloud


def get_nc_instance() -> Nextcloud:
    nextcloud_url = os.environ.get("NEXTCLOUD_INSTANCE_URL")
    nextcloud_username = os.environ.get("NEXTCLOUD_USER")
    nextcloud_app_password = os.environ.get("NEXTCLOUD_APP_PASSWORD")

    print(f"Connecting to Nextcloud at {nextcloud_url} with user {nextcloud_username}...")

    return Nextcloud(nextcloud_url=nextcloud_url, nc_auth_user=nextcloud_username, nc_auth_pass=nextcloud_app_password)
